# -*- coding: utf-8 -*-
"""bodymd 自检（self-test）。

用途：
    一条命令证明整个仓库是完好的 —— 结构完整、契约可校验、聚合结果确定、
    合成档案符合文档承诺。发布前跑一次，改动脚本后跑一次。

契约版本：
    v1.0（见 SKILL.md §3）

设计约束：
    1. 仅依赖 Python 标准库
    2. 复用 validate_log.py 与 parse_log.py —— 测试的不是"另一个实现"，是同一个实现
    3. **每一条断言都对应 docs/testing.md 里写下的承诺**；不接受"大概对了"

用法：
    python3 scripts/selftest.py
    python3 scripts/selftest.py --verbose

退出码：
    0 = 全部通过
    1 = 存在失败项
"""

import sys
import importlib.util
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "examples" / "fixtures"

# 期望值 —— 全部来自 docs/testing.md 与 examples/fixtures/personas.md 的公开承诺。
EXPECTED_PERSONAS = 8
# CN-01 是两周（09-07..09-13 + 09-14..09-20），其余 7 人是 09-14..09-20 一周
EXPECTED_DAYS = 63
EXPECTED_WARNING_FILES = {"MX-01.md"}   # 只有这个档案带故意的警告
# Totals 缺 intake_kcal、由脚本逐餐累加的天。两种成因都算：
#   a) 填了 Totals 但漏了 intake   → 摄入可重算，消耗也有 → 缺口算得出
#   b) 完全没有 Totals 段落         → 摄入可重算，消耗没记 → 缺口必须是 unknown
EXPECTED_COMPUTED_DAYS = {
    ("CN-01", "2026-09-18"),   # a
    ("CN-02", "2026-09-18"),   # a
    ("IN-01", "2026-09-17"),   # a
    ("US-02", "2026-09-16"),   # a
    ("UK-01", "2026-09-20"),   # a
    ("US-02", "2026-09-19"),   # b —— 唯一一天完全没有 Totals
}
# 无 Totals 段落 → 摄入能重算、缺口必须是 unknown（None），绝不能被当成 0
EXPECTED_UNKNOWN_DEFICIT = ("US-02", "2026-09-19")
EXPECTED_RECOMPUTED_INTAKE = 2180     # 上一条那天的逐餐累加值
# 严重蛋白缺失的样本日
EXPECTED_PROTEIN = {("MX-01", "2026-09-17"): 48}
# Totals 的 intake_kcal 与逐餐累加值的允许偏差
INTAKE_TOLERANCE = 0.05

REQUIRED_FILES = [
    "SKILL.md", "README.md", "README.zh.md", "LICENSE.md", "PRD.md", "AGENTS.md",
    ".gitattributes", ".gitignore",
    ".cursor/rules/bodymd.mdc", ".github/copilot-instructions.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml", ".github/ISSUE_TEMPLATE/question.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    "templates/profile.md", "templates/daily-log.md", "templates/report.md",
    "workflows/01-meal-log.md", "workflows/02-training-log.md",
    "workflows/03-daily-report.md", "workflows/04-weekly-review.md",
    "prompts/meal-analysis.md", "prompts/report-generator.md", "prompts/training-coach.md",
    "docs/testing.md", "docs/dev-guide.md", "docs/user-guide.md",
    "docs/troubleshooting.md", "docs/zh-CN/troubleshooting.md",
    "docs/run-with-any-model.md", "docs/zh-CN/run-with-any-model.md",
    "docs/zh-CN/user-guide.md",
    "docs/byok-setup.md", "docs/faq.md", "docs/why-local-data.md",
    "scripts/validate_log.py", "scripts/parse_log.py", "scripts/selftest.py",
    "examples/walkthrough.md", "docs/zh-CN/walkthrough.md",
    "examples/sample-week.md", "examples/fixtures/README.md",
    "examples/fixtures/personas.md", "examples/fixtures/CYCLE.md",
]

# 文档里出现的日志示例行也要符合契约 —— 见 T16。
# 这份清单就是"哪些文件里的话会被用户照抄"。少一个文件，这类缺陷就会漏一个。
SAMPLE_SOURCE_DOCS = [
    "SKILL.md", "AGENTS.md",
    "README.md", "README.zh.md",
    "templates/daily-log.md",
    "workflows/01-meal-log.md", "workflows/03-daily-report.md",
    "prompts/training-coach.md",
    "examples/walkthrough.md", "docs/zh-CN/walkthrough.md",
    "docs/troubleshooting.md", "docs/zh-CN/troubleshooting.md",
    "docs/user-guide.md", "docs/dev-guide.md",
    "docs/zh-CN/user-guide.md",
    "examples/fixtures/CYCLE.md",
]

PERSONA_IDS = ["CN-01", "CN-02", "US-01", "US-02", "UK-01", "MX-01", "NG-01", "IN-01"]


class Report:
    """收集断言结果并打印一张表。"""

    def __init__(self, verbose: bool = False):
        self.rows = []
        self.verbose = verbose

    def check(self, name: str, passed: bool, detail: str = "") -> bool:
        self.rows.append((name, passed, detail))
        mark = "PASS" if passed else "FAIL"
        line = f"[{mark}] {name}"
        if detail and (not passed or self.verbose):
            line += f"  —— {detail}"
        print(line)
        return passed

    def summary(self) -> int:
        failed = [r for r in self.rows if not r[1]]
        print("\n" + "-" * 68)
        print(f"共 {len(self.rows)} 项：通过 {len(self.rows) - len(failed)}，失败 {len(failed)}")
        if failed:
            print("\n失败项：")
            for name, _, detail in failed:
                print(f"  - {name}: {detail}")
            return 1
        print("结论：仓库自检全部通过。")
        return 0


def load_module(path: Path, name: str):
    """按文件路径加载模块（脚本名不是合法包名，不能直接 import）。"""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sum_meals(path: Path):
    """逐天累加 ## Meals 段里的热量与蛋白，返回 {(档案, 日期): (kcal, protein)}。

    这是独立于 parse_log 的一次实现，专门用来交叉验证 Totals 是否与明细自洽
    —— 如果两处都错，说明是同一处笔误；如果只有一处错，说明是解析器有 bug。
    """
    import re
    kc = re.compile(r"([\d.]+)\s*kcal")
    pr = re.compile(r"[Pp]([\d.]+)")
    heading = re.compile(r"^#\s+(\d{4}-\d{2}-\d{2})\s*$")

    text = path.read_text(encoding="utf-8")
    out = {}
    day = None
    section = None
    kcal = protein = 0.0

    def flush():
        if day is not None:
            out[(path.stem, day)] = (kcal, protein)

    for raw in text.splitlines():
        line = raw.strip()
        m = heading.match(line)
        if m:
            flush()
            day, section, kcal, protein = m.group(1), None, 0.0, 0.0
            continue
        if line.startswith("## "):
            title = line[3:].strip().lower()
            section = "meals" if "meal" in title else None
            continue
        if section != "meals" or not line.startswith("- "):
            continue
        body = line[2:]
        hit = kc.search(body)
        if hit:
            kcal += float(hit.group(1))
        hit = pr.search(body)
        if hit:
            protein += float(hit.group(1))

    flush()
    return out


def fenced_source_tokens(path: Path):
    """从围栏代码块里抽出所有 `source` 后面跟的取值。

    为什么不能只看 `- ` 开头、带 `|` 的行：
        某些文档把记录渲染成**对齐的字段列表**，不是管道分隔的单行 ——
        `workflows/02-training-log.md` 里的
            reps      12
            source    video
        就是这样。`video` 不是合取值，但没有哪个只看管道行的检查会发现它。
    """
    import re
    fence = re.compile(r"^\s*```")
    token_re = re.compile(r"\bsource\b\s*:?\s*([A-Za-z][A-Za-z+\-]*)")
    out = []
    inside = False
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if fence.match(raw):
            inside = not inside
            continue
        if not inside:
            continue
        for m in token_re.finditer(raw):
            out.append((lineno, m.group(1)))
    return out


def sample_log_lines(path: Path):
    """从文档的围栏代码块里抽出"会被用户照抄"的日志行。

    为什么要专门做这个：
        仓库里最贵的缺陷不是脚本算错，而是**文档给出的示例本身就违反契约**。
        用户第一次照抄就失败，而且失败的是他第一天唯一的一次尝试。
        本函数的产出被 T16 拿去跑同一个校验器 —— 文档示例和用户日志用同一把尺子。

    只认两种情况：
        餐食行 —— 首字段形如 HH:MM
        训练行 —— 含 exercise: / session_burn
    含 <placeholder> 或 [placeholder] 的行不算样本（它们是字段说明，不是数据）。
    `prompts/training-coach.md` 里那种粘贴模板（`- exercise: [name]`）就靠这一条排除：
    它用的是另一套字段名，本来就不是日志行。
    """
    import re
    fence = re.compile(r"^\s*```")
    time_re = re.compile(r"^\d{2}:\d{2}$")
    out = []
    inside = False
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if fence.match(raw):
            inside = not inside
            continue
        if not inside:
            continue
        line = raw.strip()
        if not line.startswith("- ") or "<" in line or "[" in line:
            continue
        body = line[2:].strip()
        fields = [f.strip() for f in body.split("|")]
        if time_re.match(fields[0]):
            out.append(("meal", lineno, body, fields))
        elif "exercise:" in body or "session_burn" in body:
            out.append(("training", lineno, body, fields))
    return out


def main(argv: list) -> int:
    verbose = "--verbose" in argv or "-v" in argv
    rep = Report(verbose)

    print("bodymd self-test")
    print("=" * 68)

    # --- T1 结构完整 -------------------------------------------------------
    missing = [p for p in REQUIRED_FILES if not (ROOT / p).exists()]
    rep.check(f"T1 必需文件齐全（{len(REQUIRED_FILES)} 项）", not missing, f"缺失：{missing}")

    # --- T2 SKILL.md 头部 --------------------------------------------------
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    has_name = "name: bodymd" in skill
    has_desc = "description:" in skill
    rep.check("T2 SKILL.md 有 name 与 description 头", has_name and has_desc,
              f"name={has_name} description={has_desc}")

    # --- T3 适配文件都指向 SKILL.md ---------------------------------------
    adapters = {
        "AGENTS.md": "SKILL.md",
        ".cursor/rules/bodymd.mdc": "SKILL.md",
        ".github/copilot-instructions.md": "SKILL.md",
    }
    bad = [f for f, token in adapters.items() if token not in (ROOT / f).read_text(encoding="utf-8")]
    rep.check("T3 三个适配文件均指向 SKILL.md", not bad, f"未指向：{bad}")

    # --- T4 合成档案带 SYNTHETIC 标记 -------------------------------------
    unmarked = [pid for pid in PERSONA_IDS
                if not (FIXTURES / f"{pid}.md").read_text(encoding="utf-8")
                .lstrip().startswith("# SYNTHETIC")]
    rep.check("T4 8 个合成档案均带 SYNTHETIC 标记", not unmarked, f"未标记：{unmarked}")

    # --- 加载被测模块 ------------------------------------------------------
    validate_log = load_module(ROOT / "scripts" / "validate_log.py", "validate_log")
    parse_log = load_module(ROOT / "scripts" / "parse_log.py", "parse_log")

    # --- T5 契约校验：致命 0 ----------------------------------------------
    fatal_files, warn_files = [], []
    for pid in PERSONA_IDS:
        issues = validate_log.check_file(FIXTURES / f"{pid}.md")
        if any(i.level == validate_log.FATAL for i in issues):
            fatal_files.append(pid)
        if any(i.level == validate_log.WARN for i in issues):
            warn_files.append(f"{pid}.md")
    rep.check("T5 契约校验：0 个致命错误", not fatal_files, f"有致命项：{fatal_files}")

    # --- T6 警告只来自预期档案（证明"降级为警告"这条设计成立）-------------
    rep.check("T6 警告仅出现在 MX-01（故意留的 2 条）",
              set(warn_files) == EXPECTED_WARNING_FILES,
              f"实际：{warn_files}，预期：{sorted(EXPECTED_WARNING_FILES)}")

    # --- T7 聚合规模 ------------------------------------------------------
    records = []
    for pid in PERSONA_IDS:
        records.extend(parse_log.parse_file(FIXTURES / f"{pid}.md"))
    labels = {r.label for r in records}
    rep.check(f"T7 聚合得到 {EXPECTED_DAYS} 天 / {EXPECTED_PERSONAS} 个档案",
              len(records) == EXPECTED_DAYS and len(labels) == EXPECTED_PERSONAS,
              f"实际 {len(records)} 天 / {len(labels)} 个档案")

    index = {(r.label, r.day.isoformat()): r for r in records}

    # --- T8 Totals 缺 intake 的天必须走 computed 路径 ---------------------
    computed = {(r.label, r.day.isoformat()) for r in records if r.source_note == "computed"}
    rep.check("T8 缺 Totals 的天正确回退为逐餐累加（computed）",
              computed == EXPECTED_COMPUTED_DAYS,
              f"实际 {sorted(computed)}")

    # --- T9 无 Totals → 摄入可重算、缺口必须是 unknown --------------------
    key = EXPECTED_UNKNOWN_DEFICIT
    rec = index.get(key)
    ok9 = (rec is not None
           and rec.deficit is None
           and rec.intake_kcal == EXPECTED_RECOMPUTED_INTAKE)
    rep.check("T9 无 Totals 日：摄入可重算、缺口为 unknown（不是 0）", ok9,
              f"{key} intake={None if rec is None else rec.intake_kcal} "
              f"(期望 {EXPECTED_RECOMPUTED_INTAKE}) "
              f"deficit={None if rec is None else rec.deficit} (期望 None)")

    # --- T10 逐天 Totals 与明细自洽（±5%）--------------------------------
    drift = []
    for pid in PERSONA_IDS:
        sums = sum_meals(FIXTURES / f"{pid}.md")
        for (label, day), (kcal, _p) in sums.items():
            rec = index.get((label, day))
            if rec is None or rec.intake_kcal is None:
                continue
            if abs(rec.intake_kcal - kcal) > INTAKE_TOLERANCE * max(kcal, 1):
                drift.append(f"{label} {day}: totals={rec.intake_kcal} 明细={kcal}")
    rep.check("T10 Totals 与逐餐累加自洽（±5%）", not drift,
              f"{len(drift)} 天不一致：{drift[:3]}")

    # --- T11 关键样本值（防止解析器悄悄算错）-----------------------------
    bad_samples = []
    for (label, day), expected in EXPECTED_PROTEIN.items():
        rec = index.get((label, day))
        got = None if rec is None else rec.protein_g
        if got != expected:
            bad_samples.append(f"{label} {day}: 蛋白 {got} != {expected}")
    rep.check("T11 MX-01 严重蛋白缺失日 = 48g", not bad_samples, "; ".join(bad_samples))

    # --- T12 解析确定性（同输入两次结果一致）------------------------------
    def fingerprint():
        rows = []
        for pid in PERSONA_IDS:
            for r in parse_log.parse_file(FIXTURES / f"{pid}.md"):
                rows.append((r.label, r.day.isoformat(), r.intake_kcal, r.protein_g,
                             r.expenditure_kcal, r.deficit, r.training_sets, r.source_note))
        return sorted(rows, key=lambda x: (x[0], x[1]))

    rep.check("T12 聚合结果确定（两次运行完全一致）", fingerprint() == fingerprint())

    # --- T13 每条餐食/训练行都带 source -----------------------------------
    # ⚠️ 教训：本检查的第一版只看「行首是不是 HH:MM」，结果把 ## Notes 里
    #    "22:30 的炸鸡不是饿，是习惯" 这种备注误判成餐食行，报了 2 个假阳性。
    #    → 校验必须**先看段落上下文**，再看行内容。格式测试自己也要遵守格式。
    missing_fields = []
    for pid in PERSONA_IDS:
        section = None
        lines = (FIXTURES / f"{pid}.md").read_text(encoding="utf-8").splitlines()
        for lineno, raw in enumerate(lines, 1):
            line = raw.strip()
            if line.startswith("## "):
                title = line[3:].strip().lower()
                if "meal" in title:
                    section = "meals"
                elif "training" in title:
                    section = "training"
                else:
                    section = None
                continue
            if line.startswith("# ") or not line.startswith("- "):
                continue
            body = line[2:].strip()
            if section == "meals" and "source:" not in body:
                missing_fields.append(f"{pid}:{lineno} 餐食缺 source")
            if (section == "training" and "exercise:" in body
                    and "source:" not in body and "session_burn" not in body):
                missing_fields.append(f"{pid}:{lineno} 训练缺 source")
    rep.check("T13 所有餐食与训练行均带 source 字段", not missing_fields,
              f"{len(missing_fields)} 处：{missing_fields[:3]}")

    # --- T14 一天一文件布局：身份取目录名，不取日期 ------------------------
    # 动机：一个真人存成 7 个日文件，输出却写 "7 天 / 7 个档案"。
    # 文件名只是日期，目录才是身份。
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        daydir = Path(tmp) / "log"
        daydir.mkdir()
        for name in ("2026-10-12.md", "2026-10-13.md"):
            (daydir / name).write_text(
                "# sample\n\n## Meals\n"
                "- 08:20 | breakfast | 燕麦 + 鸡蛋 | 520 kcal | P42 C48 F16"
                " | photo: p.jpg | source: photo | edited: none\n\n"
                "## Totals\n- intake_kcal: 1850\n- protein_g: 148\n"
                "- expenditure_kcal: 2330\n- deficit_kcal: 480\n",
                encoding="utf-8",
            )
        flat = []
        for p in sorted(daydir.glob("*.md")):
            flat.extend(parse_log.parse_file(p))
        day_labels = {r.label for r in flat}
        day_count = len(flat)
    rep.check("T14 一天一文件布局：标签取目录名（1 个档案，不是 7 个）",
              day_count == 2 and day_labels == {"log"},
              f"实际 {day_count} 天 / 标签 {sorted(day_labels)}")

    # --- T15 可选扩展字段不破坏任何东西 -----------------------------------
    # order_ok / ## Body / ## Supplements 是刻意设计的"可忽略扩展"。
    # 如果它们让校验器报错，这个契约就不敢长大 —— 而不敢长大的契约会死。
    with tempfile.TemporaryDirectory() as tmp:
        opt = Path(tmp) / "2026-10-12.md"
        opt.write_text(
            "## Meals\n"
            "- 08:20 | breakfast | 燕麦 + 鸡蛋 | 520 kcal | P42 C48 F16"
            " | photo: p.jpg | source: photo | edited: none | order_ok: yes\n\n"
            "## Body\n- weight_kg: 74.8 | source: scale | time: 07:10\n\n"
            "## Supplements\n- item: creatine | dose_g: 5 | source: manual\n\n"
            "## Totals\n- intake_kcal: 1850\n- protein_g: 148\n"
            "- expenditure_kcal: 2330\n- deficit_kcal: 480\n",
            encoding="utf-8",
        )
        opt_issues = validate_log.check_file(opt)
        opt_fatal = [i for i in opt_issues if i.level == validate_log.FATAL]
        opt_recs = parse_log.parse_file(opt)
        opt_rec = opt_recs[0] if opt_recs else None
    rep.check("T15 可选字段（order_ok / Body / Supplements）既不报错也不丢数据",
              not opt_fatal and opt_rec is not None
              and opt_rec.intake_kcal == 1850 and opt_rec.deficit == 480,
              f"fatal={[str(i) for i in opt_fatal]} rec={opt_rec}")

    # --- T16 文档里的示例日志行必须过契约 ---------------------------------
    # 本仓库最贵的一类缺陷：**示例本身违反自己定义的契约**。
    # 用户照抄第一次就失败，而那是他唯一的一次尝试。
    # 已经真的发生过 5 次（缺 source、source 值非法、字段不足、休息日写法、
    # README 首页示例块）。文档示例和用户日志，必须用同一把尺子。
    bad_samples = []
    scanned = 0
    for rel in SAMPLE_SOURCE_DOCS:
        path = ROOT / rel
        if not path.exists():
            bad_samples.append(f"{rel}: 文件不存在")
            continue
        for kind, lineno, body, fields in sample_log_lines(path):
            scanned += 1
            where = f"{rel}:{lineno}"
            if kind == "meal":
                issues = []
                validate_log.check_meal_line(body, lineno, issues)
                bad_samples.extend(
                    f"{where} 餐食行：{i.message}"
                    for i in issues if i.level == validate_log.FATAL
                )
                # 位置字段是 time | meal | 菜品描述 | kcal。
                # 第 3 位一旦是热量，说明这一行漏了菜品描述。
                if len(fields) >= 3 and "kcal" in fields[2].lower():
                    bad_samples.append(f"{where} 餐食行缺少菜品描述字段（第 3 位是热量）")
            else:
                if "session_burn" in body:
                    if "source:" not in body:
                        bad_samples.append(
                            f"{where} session_burn_kcal 缺 source（§5.3 要求标注 estimated）"
                        )
                    continue
                issues = []
                validate_log.check_training_line(body, lineno, issues)
                bad_samples.extend(
                    f"{where} 训练行：{i.message}"
                    for i in issues if i.level == validate_log.FATAL
                )
    rep.check(f"T16 文档示例日志行符合契约（扫描 {scanned} 行）", not bad_samples,
              f"{len(bad_samples)} 处：{bad_samples[:4]}")

    # --- T16b 文档里出现的每个 source 取值都必须是公布过的 -----------------
    # 动机：文档曾公布 6 个取值，仓库里实际用了 15 个；`wearable` 公布了却 0 次使用，
    # `scale` / `tape` / `self-report` / `video` 用了却没公布。
    # 一份"合法取值"清单如果和真实用法不一致，它就不是契约，是装饰。
    PUBLISHED = {
        "photo", "voice", "manual", "wearable", "video+voice", "estimated",   # 餐食
        "scale", "tape", "none",                                              # ## Body
        "oura", "whoop", "garmin", "fitbit", "band", "watch", "phone",        # ## Sleep
        "self-report", "product-label",                                       # Sleep / 补剂
    }
    unknown_sources = []
    tokens_seen = 0
    for rel in SAMPLE_SOURCE_DOCS:
        path = ROOT / rel
        if not path.exists():
            continue
        for lineno, token in fenced_source_tokens(path):
            tokens_seen += 1
            if token not in PUBLISHED:
                unknown_sources.append(f"{rel}:{lineno} source={token}")
    rep.check(f"T16b 文档中的 source 取值全部已公布（{tokens_seen} 处）",
              not unknown_sources,
              f"未公布：{unknown_sources[:4]}")

    # --- T17 单次训练消耗 ≠ 全天消耗 --------------------------------------
    # 动机：旧实现把 "session_burn_kcal" 也算进了 expenditure_kcal。
    # 这两个数差一个数量级（260 vs 2650），一旦被当成同一个，缺口会错到毫无意义。
    # 而"全天消耗只能来自 ## Totals"这条，正是 T9「无 Totals → 缺口必须是 unknown」
    # 的前提 —— 两处必须一致。
    burn = index.get(("CN-01", "2026-09-14"))
    ok17 = (burn is not None
            and burn.session_burn_kcal == 260        # ## Training 里的 session_burn_kcal
            and burn.expenditure_kcal == 2650        # ## Totals 里的 expenditure_kcal
            and burn.session_burn_kcal != burn.expenditure_kcal)
    no_totals = index.get(EXPECTED_UNKNOWN_DEFICIT)
    ok17 = ok17 and no_totals is not None and no_totals.expenditure_kcal is None
    rep.check("T17 单次训练消耗与全天消耗是两个字段，不互相污染", ok17,
              f"CN-01 09-14 burn={None if burn is None else burn.session_burn_kcal} "
              f"expenditure={None if burn is None else burn.expenditure_kcal}；"
              f"无 Totals 日 expenditure={None if no_totals is None else no_totals.expenditure_kcal}")

    # --- T18 周是计量单位：两周必须分成两行，且趋势可算 --------------------
    # 动机：全部 fixture 曾经只有一周，所以「这一周 vs 上一周」这条路径零覆盖 ——
    # 而 workflows/04-weekly-review.md 的每一条重算规则都建立在它上面。
    # 旧实现按「档案」聚合，两周被混成一个平均数，体重趋势永远是「——」，
    # 于是"平台期连续两周"这条规则永远无法被触发。聚合粒度错了，规则就是装饰。
    label_weeks = {}
    for path in sorted(FIXTURES.glob("*.md")):
        for rec in parse_log.parse_file(path):
            label_weeks.setdefault(rec.label, set()).add(parse_log.iso_week_of(rec.day))

    weeks_cn01 = sorted(label_weeks.get("CN-01", set()))
    others_single = all(
        len(weeks) == 1 for lab, weeks in label_weeks.items() if lab != "CN-01"
    )

    rows18 = parse_log.weekly_rows(records, {})
    cn01_rows = [r for r in rows18 if r["label"] == "CN-01"]
    trend = cn01_rows[-1]["trend"] if len(cn01_rows) == 2 else None
    first_trend_none = bool(cn01_rows) and cn01_rows[0]["trend"] is None

    ok18 = (len(weeks_cn01) == 2
            and others_single
            and len(cn01_rows) == 2
            and first_trend_none
            and trend is not None
            and abs(trend - (-0.71)) < 0.02)
    rep.check("T18 两周分成两个 ISO 周，体重趋势按 7 天均值算出", ok18,
              f"CN-01 周={weeks_cn01} 趋势={trend} 首周趋势=None?{first_trend_none} "
              f"其余档案均为单周={others_single}")

    # --- T19 蛋白达标按 90% 阈值、且逐档案用自己的目标 ----------------------
    # 动机：旧实现根本不计算这项，只打印「提示：需与 protein_target_g 比对后计算」——
    # 把三个聚合里最容易被忽略、也最能证伪"我在执行"的那一个，推回给了用户。
    # 两个容易错的地方：① 用 100% 而不是 90%（会系统性低估执行率）
    #                  ② 所有档案共用一个目标（170cm 的女生按 178cm 男生的标准判）
    targets19 = {}
    for path in sorted(FIXTURES.glob("*.md")):
        lab = parse_log.label_for(path)
        tgt = parse_log.header_protein_target(path)
        if tgt:
            targets19[lab] = tgt

    rows19 = parse_log.weekly_rows(records, targets19)

    # 独立重算一遍（不调用 weekly_rows 的分组逻辑），交叉验证
    grouped19 = {}
    for rec in records:
        key = (rec.label, parse_log.iso_week_of(rec.day))
        grouped19.setdefault(key, []).append(rec)
    expected19 = {}
    for (lab, week), items in grouped19.items():
        tgt = targets19.get(lab)
        if not tgt:
            continue
        hit = sum(1 for r in items if r.protein_g is not None and r.protein_g >= 0.9 * tgt)
        expected19[(lab, week)] = f"{hit}/{len(items)}"

    mismatch19 = [
        f"{r['label']} {r['week']}: {r['adherence']}≠{expected19[(r['label'], r['week'])]}"
        for r in rows19
        if (r["label"], r["week"]) in expected19
        and r["adherence"] != expected19[(r["label"], r["week"])]
    ]

    # 阈值边界：目标 150g → 135.0 必须算达标，134.9 必须不算。
    # 这条单独拎出来，是因为把 90% 改成 100% 时，上面的交叉验证会一起跟着错，
    # 只有边界探针能发现。
    probe = parse_log.DayRecord(date(2026, 9, 14), "CN-01")
    probe.weight_kg = 82.4
    probe.protein_g = 135.0
    at_boundary = parse_log.weekly_rows([probe], {"CN-01": 150})[0]["adherence"] == "1/1"
    probe.protein_g = 134.9
    below_boundary = parse_log.weekly_rows([probe], {"CN-01": 150})[0]["adherence"] == "0/1"

    # 逐档案目标确实不同：8 个目标值不应全相同
    distinct_targets = len({v for v in targets19.values() if v}) >= 6

    ok19 = (not mismatch19
            and len(expected19) == 9
            and at_boundary
            and below_boundary
            and distinct_targets)
    rep.check("T19 蛋白达标按 90% 阈值、且逐档案用自己的目标", ok19,
              f"档案-周数={len(expected19)} 边界135g={at_boundary} 134.9g={below_boundary} "
              f"目标各不相同={distinct_targets} 不一致={mismatch19[:3]}")

    return rep.summary()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
