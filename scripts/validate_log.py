# -*- coding: utf-8 -*-
"""bodymd 数据契约校验器。

用途：
    校验 log/YYYY-MM-DD.md 是否符合 SKILL.md §3 定义的数据契约。

契约版本：
    v1.0（见 SKILL.md §3）

设计约束：
    1. 仅依赖 Python 标准库（用户可能没有 pip 环境）
    2. 能降级为警告的，绝不当致命错误 —— 用户的记录不完整是常态，
       校验器的职责是提示，不是拒绝
    3. 错误信息必须可操作，要指出是哪一行、哪个字段、怎么改

退出码：
    0 = 全部通过
    1 = 存在致命错误
    2 = 仅存在警告
"""

import re
import sys
from pathlib import Path

# 合法的数据来源。契约要求：每条营养/训练记录必须来自其中之一。
VALID_SOURCES = {"photo", "voice", "manual", "wearable", "video+voice", "estimated"}

# 时间格式：24 小时制 HH:MM
TIME_PATTERN = re.compile(r"^\d{2}:\d{2}$")

# 从 "520 kcal" 这类字符串里抽出数字
KCAL_PATTERN = re.compile(r"([\d.]+)\s*kcal")

FATAL = "FATAL"
WARN = "WARN"
INFO = "INFO"


class Issue:
    """一条校验问题。level 决定它是致命错误、警告，还是提示。"""

    def __init__(self, level: str, lineno: int, message: str):
        self.level = level
        self.lineno = lineno
        self.message = message

    def __str__(self) -> str:
        return f"  [{self.level}] 第 {self.lineno} 行：{self.message}"


def split_fields(line: str) -> list:
    """把一行记录按 | 拆成字段，并去掉两侧空白。

    输入形如：
        08:20 | breakfast | 520 kcal | P42 C48 F16 | source: photo | edited: none
    返回：
        ["08:20", "breakfast", "520 kcal", "P42 C48 F16", "source: photo", "edited: none"]
    """
    return [part.strip() for part in line.split("|")]


def kv_of(fields: list) -> dict:
    """把含 "key: value" 的字段抽成字典。

    只有带冒号的字段会被收录；不带冒号的（如 "08:20"、"breakfast"）用于位置取值。
    这样即使以后契约在行尾新增字段，旧解析逻辑也不会崩。
    """
    result = {}
    for field in fields:
        if ":" in field:
            key, _, value = field.partition(":")
            result[key.strip().lower()] = value.strip()
    return result


def check_meal_line(line: str, lineno: int, issues: list) -> None:
    """校验一行餐食记录。

    契约要求（SKILL.md §3.3）：
        时间 | 餐次 | 热量 | 宏量 | ... | source: <来源> | edited: <说明或 none>
    """
    fields = split_fields(line)
    kv = kv_of(fields)

    # V1：字段数不足 —— 致命
    if len(fields) < 6:
        issues.append(Issue(FATAL, lineno, f"餐食记录字段数不足（{len(fields)} < 6），请检查是否漏了 | 分隔"))
        return

    # V2 / V3：source 必须存在且合法 —— 致命
    if "source" not in kv:
        issues.append(Issue(FATAL, lineno, "缺少 source 字段。每条营养记录都必须标注来源"))
    elif kv["source"] not in VALID_SOURCES:
        issues.append(Issue(
            FATAL, lineno,
            f"source 非法：{kv['source']!r}。合法取值为 {sorted(VALID_SOURCES)}"
        ))

    # V4：edited 字段 —— 警告（旧记录可能没有）
    if "edited" not in kv:
        issues.append(Issue(WARN, lineno, "缺少 edited 字段。人工修改过的估算应记录改动内容；未修改填 none"))

    # V5：热量必须是数字或显式 unknown —— 致命
    if not KCAL_PATTERN.search(line) and "unknown" not in line.lower():
        issues.append(Issue(FATAL, lineno, "未找到热量数值，且未显式标注 unknown"))

    # V8：时间格式 —— 警告
    if fields and not TIME_PATTERN.match(fields[0]):
        issues.append(Issue(WARN, lineno, f"时间格式应为 HH:MM，实际为 {fields[0]!r}"))


def check_training_line(line: str, lineno: int, issues: list) -> None:
    """校验一行训练记录。

    契约要求：
        exercise: <动作> | set: n | reps: n | load_kg: <数字/bodyweight/unknown> | ...
    特例：session_burn_kcal 是一行独立的汇总，不走本函数。
    """
    kv = kv_of(split_fields(line))

    # V6：动作与次数 —— 致命
    if "exercise" not in kv:
        issues.append(Issue(FATAL, lineno, "训练记录缺少 exercise 字段"))
    if "reps" not in kv:
        issues.append(Issue(FATAL, lineno, "训练记录缺少 reps 字段"))

    # V7：重量 —— 警告
    # 契约明确允许 unknown（视频读不出重量时用户不知道具体数值）
    if "load_kg" not in kv:
        issues.append(Issue(WARN, lineno, "训练记录缺少 load_kg 字段。无法确认时填 unknown，徒手动作填 bodyweight"))


def check_file(path: Path) -> list:
    """校验单个日志文件，返回问题列表。"""
    issues = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [Issue(FATAL, 0, "文件不是 UTF-8 编码，无法解析")]
    except OSError as exc:
        return [Issue(FATAL, 0, f"读取失败：{exc}")]

    section = None
    has_meals = False
    has_training = False

    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()

        # 段落切换
        if line.startswith("## "):
            title = line[3:].strip().lower()
            if "meal" in title:
                section = "meals"
                has_meals = True
            elif "training" in title:
                section = "training"
                has_training = True
            else:
                section = None
            continue

        if not line.startswith("- "):
            continue

        body = line[2:].strip()
        if section == "meals":
            check_meal_line(body, lineno, issues)
        elif section == "training":
            # session_burn_kcal 是汇总行，不是训练组，跳过
            if "session_burn" in body.lower():
                continue
            check_training_line(body, lineno, issues)

    # V9：段落缺失 —— 提示（不阻断）
    if not has_meals:
        issues.append(Issue(INFO, 0, "未找到 ## Meals 段落"))
    if not has_training:
        issues.append(Issue(INFO, 0, "未找到 ## Training 段落（休息日可接受）"))

    return issues


def main(argv: list) -> int:
    targets = [Path(a) for a in argv[1:]] or [Path("log")]
    files = []
    for target in targets:
        if target.is_dir():
            files.extend(sorted(target.rglob("*.md")))
        elif target.is_file():
            files.append(target)

    if not files:
        print("未找到任何 .md 文件。用法：python3 scripts/validate_log.py <目录或文件>")
        return 1

    fatal_total = 0
    warn_total = 0

    for path in files:
        issues = check_file(path)
        fatal = [i for i in issues if i.level == FATAL]
        warn = [i for i in issues if i.level == WARN]
        info = [i for i in issues if i.level == INFO]
        fatal_total += len(fatal)
        warn_total += len(warn)

        if fatal:
            print(f"\n[不合格] {path}")
        elif warn:
            print(f"\n[有警告] {path}")
        else:
            print(f"\n[通过]   {path}")

        for issue in fatal + warn + info:
            print(issue)

    print("\n" + "-" * 56)
    print(f"检查 {len(files)} 个文件：致命 {fatal_total} 项，警告 {warn_total} 项")

    if fatal_total:
        print("提示：致命项必须修复。契约定义见 SKILL.md §3。")
        return 1
    if warn_total:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
