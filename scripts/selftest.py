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
EXPECTED_DAYS = 56
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
    ".gitignore", ".cursor/rules/bodymd.mdc", ".github/copilot-instructions.md",
    "templates/profile.md", "templates/daily-log.md", "templates/report.md",
    "workflows/01-meal-log.md", "workflows/02-training-log.md",
    "workflows/03-daily-report.md", "workflows/04-weekly-review.md",
    "docs/testing.md", "docs/dev-guide.md", "docs/user-guide.md",
    "docs/run-with-any-model.md", "docs/zh-CN/run-with-any-model.md",
    "docs/byok-setup.md", "docs/faq.md", "docs/why-local-data.md",
    "scripts/validate_log.py", "scripts/parse_log.py", "scripts/selftest.py",
    "examples/sample-week.md", "examples/fixtures/README.md",
    "examples/fixtures/personas.md",
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


def main(argv: list) -> int:
    verbose = "--verbose" in argv or "-v" in argv
    rep = Report(verbose)

    print("bodymd self-test")
    print("=" * 68)

    # --- T1 结构完整 -------------------------------------------------------
    missing = [p for p in REQUIRED_FILES if not (ROOT / p).exists()]
    rep.check("T1 必需文件齐全（30 项）", not missing, f"缺失：{missing}")

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

    return rep.summary()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
