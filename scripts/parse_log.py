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
    日明细 + 平均缺口 / 蛋白记录天数 / 训练天数
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

    is_day_file = DATE_PATTERN.search(path.stem) is not None
    if is_day_file:
        try:
            label = path.parent.resolve().name or path.stem
        except OSError:
            label = path.parent.name or path.stem
    else:
        label = path.stem

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


def _fmt(value) -> str:
    """统一数字格式化：None 显示为 ——，其余取整显示。"""
    if value is None:
        return "——"
    return f"{value:,.0f}"


def main(argv: list) -> int:
    target = Path(argv[1]) if len(argv) > 1 else Path("log")
    files = sorted(target.rglob("*.md")) if target.is_dir() else [target]

    records = []
    for path in files:
        records.extend(parse_file(path))
    records.sort(key=lambda r: (r.label, r.day))

    if not records:
        print(f"未在 {target} 找到可解析的日志。")
        print("用法：python3 scripts/parse_log.py <目录>")
        print("格式：见 templates/daily-log.md")
        return 1

    print(f"\nbodymd 聚合 —— {len(records)} 天 / {len({r.label for r in records})} 个档案")
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

    print("-" * 76)

    # 按档案分组汇总
    from collections import defaultdict
    grouped = defaultdict(list)
    for r in records:
        grouped[r.label].append(r)

    for label, items in grouped.items():
        deficits = [r.deficit for r in items if r.deficit is not None]
        training_days = sum(1 for r in items if r.training_sets > 0)
        avg = f"{sum(deficits) / len(deficits):,.0f} kcal/天" if deficits else "——"
        print(f"{label[:20]:<22} 天数 {len(items):>2}   平均缺口 {avg:<16} 训练 {training_days} 天")

    print("\n提示：蛋白达标天数需与 profile.md 的 protein_target_g 比对后计算。")
    print("重算规则见 workflows/04-weekly-review.md。")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
