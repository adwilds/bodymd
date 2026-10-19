# -*- coding: utf-8 -*-
"""bodymd 日志聚合脚本。

用途：
    把日志解析成周聚合，供周复盘（workflows/04-weekly-review.md）使用。

契约版本：
    v1.0（见 SKILL.md §3）

支持的两种文件布局：
    A) 一天一文件，日期在文件名里      —— log/2026-10-12.md
       身份标签取**目录名**（log / people/alice …），不是日期
    B) 一档案多天，用 "# YYYY-MM-DD" 分隔 —— examples/fixtures/CN-01.md
       身份标签取**文件名**（persona 名）

设计约束：
    1. 仅依赖标准库
    2. 优先读取 ## Totals 段（用户或 AI 已算好）；缺失时自行累加，并标注来源
    3. 未知字段忽略，不中断 —— 保证契约向后兼容
    4. 未知段落忽略，不中断 —— 所以 order_ok / ## Body / ## Supplements
       这类可选扩展不会让旧解析器崩

输出：
    日明细 + **按 ISO 周**的三大聚合（正好是周复盘的三个变量）：
        ① 平均缺口      —— 当周每天缺口的均值，回答"计划对得上现实吗"
        ② 体重趋势      —— 当周 7 天体重均值 − 上一周 7 天体重均值，**唯一的地面真相**
        ③ 蛋白达标天数  —— 达到目标 90% 的天数 / 当周记录天数，回答"摄入侧被执行了吗"

为什么要按周、而不是按档案：
    workflows/04-weekly-review.md 的每一条重算规则都建立在「这一周 vs 上一周」上 ——
    「平台期连续两周」「比上周掉得快」。把两周混成一个平均数，体重趋势就永远是 ——，
    而"连续两周持平"这条规则就永远无法被触发。**周是这套系统的计量单位，不是档案。**
"""

import re
import sys
from datetime import date
from pathlib import Path

KCAL_PATTERN = re.compile(r"([\d.]+)\s*kcal")
PROTEIN_PATTERN = re.compile(r"[Pp]([\d.]+)")
DATE_PATTERN = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
# 多天文件里的日分隔标题：# 2026-09-14
DAY_HEADING = re.compile(r"^#\s+(\d{4}-\d{2}-\d{2})\s*$")


def kv_of(line: str) -> dict:
    """把含 "key: value" 的片段抽成字典，行为与 validate_log.py 保持一致。"""
    result = {}
    for part in line.split("|"):
        part = part.strip()
        if ":" in part:
            key, _, value = part.partition(":")
            result[key.strip().lower()] = value.strip()
    return result


def _to_float(value: str):
    """把字符串转成 float；转不了就返回 None（例如 unknown）。"""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


class DayRecord:
    """一天的解析结果。数值为 None 表示当天没有相应数据。"""

    def __init__(self, day: date, label: str = ""):
        self.day = day
        self.label = label          # 用于输出的身份标签（多档案模式下为 persona 名）
        self.intake_kcal = None
        self.protein_g = None
        self.expenditure_kcal = None   # 全天消耗，只来自 ## Totals
        self.deficit_kcal = None
        self.weight_kg = None          # ## Body 里的当天体重；缺测就是 None
        self.training_sets = 0
        self.session_burn_kcal = None  # 单次训练消耗，**不等于**全天消耗
        self.source_note = "totals"  # totals | computed

    def finalize(self, computed_intake: float, computed_protein: float) -> None:
        """Totals 段缺失时，用逐餐累加值兜底，并标注数据来源。"""
        if self.intake_kcal is None and computed_intake > 0:
            self.intake_kcal = computed_intake
            self.source_note = "computed"
        if self.protein_g is None and computed_protein > 0:
            self.protein_g = computed_protein

    @property
    def deficit(self):
        """缺口：优先用显式记录值，否则用 消耗 − 摄入 计算。"""
        if self.deficit_kcal is not None:
            return self.deficit_kcal
        if self.intake_kcal is not None and self.expenditure_kcal is not None:
            return self.expenditure_kcal - self.intake_kcal
        return None


def parse_text_block(lines: list, day: date, label: str) -> DayRecord:
    """解析属于同一天的若干行，返回一条 DayRecord。"""
    record = DayRecord(day, label)
    section = None
    computed_intake = 0.0
    computed_protein = 0.0

    for line in lines:
        line = line.strip()

        if line.startswith("## "):
            title = line[3:].strip().lower()
            if "meal" in title:
                section = "meals"
            elif "training" in title:
                section = "training"
            elif "totals" in title:
                section = "totals"
            elif "body" in title:
                # ## Body 是可选扩展；不认它的解析器必须照旧工作，
                # 所以这里只是"认了它"，而不是"要求它存在"。
                section = "body"
            else:
                section = None
            continue

        if not line.startswith("- "):
            continue
        body = line[2:].strip()

        if section == "meals":
            kcal = KCAL_PATTERN.search(body)
            protein = PROTEIN_PATTERN.search(body)
            if kcal:
                computed_intake += float(kcal.group(1))
            if protein:
                computed_protein += float(protein.group(1))

        elif section == "training":
            if "session_burn" in body.lower():
                # 记录单次训练消耗。**不要**把它当成全天消耗 —— 它是全天消耗的一个
                # 组成部分，拿它当分母会把缺口算错一个数量级。
                value = kv_of(body).get("session_burn_kcal")
                burn = _to_float(value) if value is not None else None
                if burn is None:
                    # 兼容 "- 275 kcal" 这类把数字写在 kcal 前面的写法
                    hit = KCAL_PATTERN.search(body)
                    burn = float(hit.group(1)) if hit else None
                if burn is not None:
                    record.session_burn_kcal = burn
            elif "exercise" in body.lower():
                record.training_sets += 1

        elif section == "totals":
            kv = kv_of(body)
            if "intake_kcal" in kv:
                record.intake_kcal = _to_float(kv["intake_kcal"])
            if "protein_g" in kv:
                record.protein_g = _to_float(kv["protein_g"])
            if "expenditure_kcal" in kv:
                record.expenditure_kcal = _to_float(kv["expenditure_kcal"])
            if "deficit_kcal" in kv:
                record.deficit_kcal = _to_float(kv["deficit_kcal"])

        elif section == "body":
            kv = kv_of(body)
            if "weight_kg" in kv:
                record.weight_kg = _to_float(kv["weight_kg"])

    record.finalize(computed_intake, computed_protein)
    return record


def parse_file(path: Path) -> list:
    """解析一个文件，返回其中所有天的记录。

    先尝试按文件内的 "# YYYY-MM-DD" 标题切分（模式 B）；
    若无任何标题，则回退到用文件名中的日期（模式 A）。

    身份标签（label）的取值规则 —— 看的是**文件名**，不是内部结构：

        文件名就是日期（log/2026-10-12.md）—— 这是一天一文件的布局，
            标签取**目录名**（log / people/alice …）
        文件名不是日期（examples/fixtures/CN-01.md）—— 这是一档案多天的布局，
            标签取**文件名**（persona 名）

    为什么要这样分：一天一文件时，文件名就是日期。若拿它当标签，一周 7 个文件会被
    算成 7 个"档案"，周汇总输出 "7 天 / 7 个档案" —— 明明是 1 个人。目录才是身份的
    载体。反过来，多天档案的文件名是人名，才是真正的身份。
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []

    label = label_for(path)

    lines = text.splitlines()
    records = []

    current_day = None
    buffer = []

    for line in lines:
        heading = DAY_HEADING.match(line.strip())
        if heading:
            # 收尾上一天
            if current_day is not None:
                records.append(parse_text_block(buffer, current_day, label))
            current_day = date.fromisoformat(heading.group(1))
            buffer = []
            continue
        buffer.append(line)

    if current_day is not None:
        records.append(parse_text_block(buffer, current_day, label))
    elif buffer:
        # 没有任何日期标题：回退到用文件名里的日期
        match = DATE_PATTERN.search(path.stem)
        if match:
            y, m, d = (int(g) for g in match.groups())
            records.append(parse_text_block(buffer, date(y, m, d), label))

    return records


def label_for(path: Path) -> str:
    """身份标签的取值规则 —— 看的是**文件名**，不是内部结构。

        文件名就是日期（log/2026-10-12.md）—— 一天一文件的布局，标签取**目录名**
        文件名不是日期（examples/fixtures/CN-01.md）—— 一档案多天的布局，标签取**文件名**

    完整理由见 parse_file 的文档字符串。抽成独立函数，是因为 main() 也要用它把
    protein 目标绑到正确的档案上 —— 两处规则必须一致，否则目标会串档案。
    """
    if DATE_PATTERN.search(path.stem) is not None:
        try:
            return path.parent.resolve().name or path.stem
        except OSError:
            return path.parent.name or path.stem
    return path.stem


# fixture 头部注释里的写法：# ... protein target 150 g ...
HEADER_PROTEIN = re.compile(r"protein\s*target\s*([\d.]+)\s*g", re.I)
# profile.md 里的写法：protein_target_g: 145
PROFILE_PROTEIN = re.compile(r"^\s*protein_target_g\s*:\s*([\d.]+)")
# workflows/04-weekly-review.md：达到目标的 90% 即记为达标，不是 100%
ADHERENCE_RATIO = 0.90

# 一周里至少要称过这么多天，才允许把均值写成「7 天均值」。
# 为什么是 4：一周 7 天，3 个或更少的读数就不再是采样，而是两个孤立点 ——
# 一次周末火锅后的偏高读数、一次早上空腹的偏低读数，相减出来的差值方向由水分决定，
# 却会被周复盘当成「这一周掉了多少」。缺测是常态，编出来的趋势不是数据。
MIN_WEIGH_INS = 4


def header_protein_target(path: Path):
    """从文件头部注释块里读 protein target（fixture 的写法）。

    只扫前 20 行，避免把正文里偶然出现的字样当成目标 —— 一个读错的目标值
    会让"达标天数"整列都错，而且错得很安静。读不到就返回 None：
    **不知道就写 unknown，不猜一个数。**
    """
    try:
        head = path.read_text(encoding="utf-8").splitlines()[:20]
    except (UnicodeDecodeError, OSError):
        return None
    for line in head:
        if not line.lstrip().startswith("#"):
            continue
        match = HEADER_PROTEIN.search(line)
        if match:
            return float(match.group(1))
    return None


def profile_protein_target(path: Path):
    """从 profile.md 读 protein_target_g。读不到返回 None。"""
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None
    for line in text.splitlines():
        match = PROFILE_PROTEIN.match(line)
        if match:
            return float(match.group(1))
    return None


def iso_week_of(day: date):
    """ISO 周键 (year, week)。

    用 ISO 周而不是自然周：周复盘的输出写的是 `YYYY-WW`，两者必须是同一套编号，
    否则报告上的"第 41 周"和脚本里的"第 41 周"能指不同的 7 天。
    """
    year, week, _ = day.isocalendar()
    return (year, week)


def _mean(values):
    """忽略 None 的均值；全为 None 时返回 None（不是 0）。"""
    clean = [v for v in values if v is not None]
    return sum(clean) / len(clean) if clean else None


def weekly_rows(records: list, targets: dict) -> list:
    """把记录按 (档案, ISO 周) 分组，算出周复盘的三个聚合。

    体重趋势用**7 天均值**而不是某一天的体重，也不是首尾两天 ——
    日间波动主要是水分，首尾相减等于让两天的水分决定一整周的结论。

    但「7 天均值」要求这一周真的有 7 天的读数（至少 MIN_WEIGH_INS 天）。
    读数不够时 weight_mean 返回 None，趋势随之变成 None —— 打印成「——」。
    这条规则是被数据逼出来的：CN-02 的 2026-W39 只有 2 个读数，旧的实现照样
    算出均值 64.25 kg 并与上周相减得出 −0.33 kg，看上去完全正常。
    """
    from collections import defaultdict

    grouped = defaultdict(list)
    for record in records:
        grouped[(record.label, iso_week_of(record.day))].append(record)

    rows = []
    for label in sorted({r.label for r in records}):
        weeks = sorted(week for (lab, week) in grouped if lab == label)
        previous_mean = None
        for week in weeks:
            items = sorted(grouped[(label, week)], key=lambda r: r.day)
            weigh_ins = [r.weight_kg for r in items if r.weight_kg is not None]
            weight_mean = _mean(weigh_ins) if len(weigh_ins) >= MIN_WEIGH_INS else None

            target = targets.get(label)
            if target:
                hit = sum(
                    1 for r in items
                    if r.protein_g is not None and r.protein_g >= ADHERENCE_RATIO * target
                )
                adherence = f"{hit}/{len(items)}"
            else:
                adherence = "——"

            rows.append({
                "label": label,
                "week": week,
                "days": len(items),
                "weigh_ins": len(weigh_ins),
                "avg_deficit": _mean([r.deficit for r in items]),
                "weight_mean": weight_mean,
                "trend": (weight_mean - previous_mean)
                         if (weight_mean is not None and previous_mean is not None) else None,
                "adherence": adherence,
                "target": target,
                "training_days": sum(1 for r in items if r.training_sets > 0),
            })
            if weight_mean is not None:
                previous_mean = weight_mean
    return rows


def _fmt(value) -> str:
    """统一数字格式化：None 显示为 ——，其余取整显示。"""
    if value is None:
        return "——"
    return f"{value:,.0f}"


def main(argv: list) -> int:
    protein_arg = None
    positional = []
    for arg in argv[1:]:
        if arg.startswith("--protein="):
            protein_arg = _to_float(arg.split("=", 1)[1])
        elif arg.startswith("--"):
            print(f"未知参数：{arg}")
            print("用法：python3 scripts/parse_log.py <目录> [--protein=150]")
            return 2
        else:
            positional.append(arg)

    target = Path(positional[0]) if positional else Path("log")
    files = sorted(target.rglob("*.md")) if target.is_dir() else [target]

    records = []
    per_file_label = {}
    for path in files:
        parsed = parse_file(path)
        if parsed:
            per_file_label[path] = parsed[0].label
            records.extend(parsed)
    records.sort(key=lambda r: (r.label, r.day))

    if not records:
        print(f"未在 {target} 找到可解析的日志。")
        print("用法：python3 scripts/parse_log.py <目录> [--protein=150]")
        print("格式：见 templates/daily-log.md")
        return 1

    # ---- protein 目标的来源，按优先级：命令行 > profile.md > 文件头注释 ----
    # 优先级是刻意的：显式指定的永远赢；profile.md 是"这个人自己的目标"；
    # 文件头注释只用于 fixture 这种没有 profile 的测试数据。
    profile_path = (target / "profile.md") if target.is_dir() else (target.parent / "profile.md")
    profile_value = profile_protein_target(profile_path) if profile_path.exists() else None

    labels = {r.label for r in records}
    targets = {}
    for path, label in per_file_label.items():
        if label not in labels:
            continue
        if protein_arg is not None:
            targets[label] = protein_arg
        elif profile_value is not None:
            targets[label] = profile_value
        else:
            targets[label] = header_protein_target(path)

    print(f"\nbodymd 聚合 —— {len(records)} 天 / {len(labels)} 个档案")
    print("=" * 76)
    print(f"{'档案':<12}{'日期':<13}{'摄入':>8}{'蛋白':>7}{'消耗':>8}{'缺口':>8}{'训练组':>7}  来源")
    print("-" * 76)

    for r in records:
        print(
            f"{r.label[:11]:<12}{r.day.isoformat():<13}"
            f"{_fmt(r.intake_kcal):>8}{_fmt(r.protein_g):>7}"
            f"{_fmt(r.expenditure_kcal):>8}{_fmt(r.deficit):>8}"
            f"{r.training_sets:>7}  {r.source_note}"
        )

    # ---- 周聚合：周复盘真正要的三个变量 ----
    print()
    print("按 ISO 周聚合（周复盘的三个变量）")
    print("=" * 84)
    print(
        f"{'档案':<10}{'ISO 周':<11}{'天':>3}{'平均缺口':>13}"
        f"{'体重均值':>11}{'趋势':>11}{'蛋白达标':>13}{'训练':>7}"
    )
    print("-" * 84)

    rows = weekly_rows(records, targets)
    for row in rows:
        year, week = row["week"]
        deficit = f"{row['avg_deficit']:,.0f} kcal" if row["avg_deficit"] is not None else "——"
        mean = f"{row['weight_mean']:.2f} kg" if row["weight_mean"] is not None else "——"
        trend = f"{row['trend']:+.2f} kg" if row["trend"] is not None else "——"
        adherence = row["adherence"]
        if row["target"]:
            adherence = f"{adherence} @{row['target']:.0f}g"
        print(
            f"{row['label'][:9]:<10}{year}-W{week:02d}   {row['days']:>2}  "
            f"{deficit:>13}{mean:>11}{trend:>11}{adherence:>13}{row['training_days']:>4} 天"
        )

    print()
    print("读法：")
    print(f"  · 体重趋势 = 当周 7 天体重均值 − 上一周 7 天体重均值。首周显示「——」是正常的。")
    print(f"  · 一周称重少于 {MIN_WEIGH_INS} 天时，体重均值与趋势同样是「——」："
          f"均值不成立，趋势也就无从谈起。")
    print(f"  · 蛋白达标按目标的 {ADHERENCE_RATIO:.0%} 计（不是 100%），见 workflows/04-weekly-review.md。")
    print("  · 只有一周数据时，周对周规则无法判定 —— 这不是脚本的缺陷，是数据的缺陷。")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
