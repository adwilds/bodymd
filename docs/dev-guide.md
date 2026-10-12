# 开发手册（Dev Guide）

> 面向：维护 bodymd 仓库的人（目前是一个人）。
> 原则：**任何改动都必须让数据契约的破坏性变更最小化。**

---

## 一、架构总览

```
用户 / AI 代理
      │
      ▼
┌─────────────────────────────────┐
│  工作流层  workflows/*.md        │  ← 定义"怎么做"，人类可读
├─────────────────────────────────┤
│  契约层    SKILL.md §3           │  ← 定义"数据长什么样"，最稳定的一层
├─────────────────────────────────┤
│  模板层    templates/*.md        │  ← 契约的具体实例
├─────────────────────────────────┤
│  数据层    profile.md / log/     │  ← 用户自己的文件夹（不进仓库）
└─────────────────────────────────┘
      ▲
      │
┌─────────────────────────────────┐
│  工具层    scripts/*.py          │  ← 可选：校验与聚合
└─────────────────────────────────┘
```

⭐ **分层规则**：
- **契约层最稳定**，改动需要版本号
- **工作流层可以高频迭代**，因为它只是"怎么用契约"的说明书
- **工具层永远可选** —— 删掉 scripts/ 整个目录，产品依然完整可用

**这条规则的意义**：工具不是产品，契约才是。任何时候，用户不装 Python 也应该能用。

---

## 二、目录职责

| 目录 | 职责 | 变更频率 |
|---|---|---|
| `SKILL.md` | 契约 + 规则 + 合规红线 | 低（改需谨慎） |
| `workflows/` | 四个日常工作流 | 中 |
| `prompts/` | 可直接复制的提示词 | 中 |
| `templates/` | 数据格式样板 | 低 |
| `docs/` | 面向人的说明 | 中 |
| `scripts/` | 可选工具 | 可弃 |
| `examples/fixtures/` | **合成测试数据（SYNTHETIC）** | 低 |

---

## 三、如何扩展数据契约

### 3.1 加字段（向后兼容，允许）

在 `templates/` 与 `SKILL.md` §3 同步添加，并在 `SKILL.md` 中标注引入版本。

```yaml
# 3.3 Daily log schema — added in v1.1
- 08:20 | breakfast | 酒店自助：炒蛋 2 个 + 培根 3 片 + 吐司 1 片 | 520 kcal | P42 C48 F16 | photo: photos/2026-10-12/0820.jpg | source: photo | edited: none | note: hotel buffet
```

**规则**：新字段一律**追加到行尾**，不得插在中间。这样旧解析器遇到多余字段时可直接忽略。

### 3.2 改字段名或删除（破坏性，需版本号）

1. 在 `SKILL.md` 里把旧字段标记为 `deprecated`
2. 新增一个 `docs/migrations/vX-to-vY.md` 说明如何转换
3. **不提供自动迁移脚本** —— 数据是用户的，破坏它比让他手动改更糟

### 3.3 校验

每次改契约后，跑：

```bash
python3 scripts/validate_log.py examples/fixtures/
```

全部 fixture 通过才允许提交。

---

## 四、如何新增一个工作流

模板：

```markdown
# Workflow NN — <name>

**Trigger:** <什么时候触发>

**Goal:** <一句话目标，含可验收的产出>

## Inputs
| Input | Required | Notes |

## Steps
1. ...（编号，可机械执行）

## Output format
<固定格式，便于机读>

## Edge cases
| Situation | Handling |

## Do not
- <常见错误>
```

**验收标准**：一个没读过这个仓库的人，只看这一页，能完成一次。

---

## 五、代码规范（`scripts/`）

### 5.1 语言与依赖

- Python 3.9+，**仅标准库**（不引入 pandas / requests 等）
- 文件编码 UTF-8

### 5.2 命名

| 对象 | 规范 | 示例 |
|---|---|---|
| 变量 / 函数 / 模块 | 英文，snake_case | `parse_daily_log`, `protein_g` |
| 类 | 英文，PascalCase | `DailyLog` |
| 常量 | 英文，UPPER_SNAKE | `VALID_SOURCES` |
| **注释 / 文档字符串** | **中文** | 见下 |

⭐ **为什么注释用中文**：本仓库的代码是**参考实现**，不是核心交付。契约与工作流是英文（面向全球用户），代码是给维护者看的（当前只有一个人）。语言分工明确，不混淆。

### 5.3 注释规范

```python
# -*- coding: utf-8 -*-
"""bodymd 日志解析器。

用途：把 log/YYYY-MM-DD.md 解析成结构化数据，输出周聚合。
契约版本：v1.0（见 SKILL.md §3）

设计约束：
1. 只依赖标准库
2. 解析失败必须给出可操作提示，不能只报错
3. 遇到未知字段应忽略而非中断（向后兼容）
"""

VALID_SOURCES = {"photo", "voice", "manual", "wearable", "video+voice", "estimated"}
"""合法的餐食来源。

契约要求：每条营养记录必须来自其中之一。
注意这个集合**只管餐食行** —— 训练行、## Body、## Sleep 各有独立取值集合
（见 SKILL.md §3.4）。把它们混成一个集合是真实踩过的坑：
文档只公布了 6 个值，仓库里实际用了 15 个。
"""


def parse_meal_line(line: str) -> dict:
    """解析一行餐食记录。

    输入形如：
        08:20 | breakfast | 燕麦 60g + 鸡蛋 3 个 | 520 kcal | P42 C48 F16 | photo: p.jpg | source: photo | edited: none

    返回：
        {"time": "08:20", "meal": "breakfast", "kcal": 520,
         "protein_g": 42, "carbs_g": 48, "fat_g": 16,
         "source": "photo", "edited": "none"}

    异常：
        ValueError —— 字段数不足或 source 非法时抛出
    """
```

**注释三原则**：
1. **模块级 docstring 写"为什么"，不写"是什么"**
2. **函数级 docstring 写输入 / 输出 / 异常**
3. **行内注释只用于解释不显然的决定**，禁止复述代码

### 5.4 错误信息规范

必须**可操作**。对比：

```python
# ✗ 不合格
raise ValueError("invalid source")

# ✓ 合格
raise ValueError(
    f"第 {lineno} 行 source 非法：{source!r}。"
    f"合法取值为 {sorted(VALID_SOURCES)}。"
    f"请检查 log/ 文件中该行的 source 字段。"
)
```

---

## 六、发布 Checklist

- [ ] `validate_log.py` 对全部 `examples/fixtures/` 通过
- [ ] 全文搜索，确认无个人数据、无 API key
- [ ] `.gitignore` 已包含 `profile.md` / `log/` / `reports/` / `photos/`
- [x] `README.md` 中的仓库地址已替换（`adwilds`）
- [ ] `LICENSE.md` 中的版权人已替换
- [ ] `README.md` 已说明 `examples/fixtures/` 为合成数据
- [ ] 合规红线（`SKILL.md` §7）未被改动
- [ ] 跑通一次完整流程（拍餐 → 训练 → 日报 → 周复盘）

---

## 七、维护者守则

1. **不为了"更完整"而加功能。** 四个工作流是设计上限，不是起点。
2. **不引入服务端。** 任何需要服务器的功能 = 自我否定。
3. **不接受"做个 App 吧"的请求。** 礼貌拒绝并指向设计初衷。
4. **数据契约的破坏性变更，宁可让用户手动改，也不写自动迁移。**
5. **star 数不是指标。** 付费客户和自发使用才是。
