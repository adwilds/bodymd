# Run bodymd with any model

**bodymd is not a Claude product, a Codex product, or a Kimi product.** It is a set of
Markdown files. Any model that can read text can run it — that is the entire point.

---

## The one design decision that makes this possible

`SKILL.md` is **plain Markdown with a two-line YAML header.** There is no platform-specific
syntax, no vendor function-calling format, no SDK. So there are only three ways a tool can
consume it:

| How the tool reads files | What you do | Tools |
|---|---|---|
| **Automatically** reads a conventional filename | Nothing — the adapter files are already in this repo | Claude Code, Codex CLI, Cursor, Copilot |
| **You paste** it into the chat | Copy `SKILL.md` + `profile.md` + today's log | ChatGPT, Gemini, Claude.ai, DeepSeek web, Kimi web, 豆包 |
| **You upload** it as a file / knowledge base | Upload once, reference each session | Kimi, 豆包, 通义, Gemini |

**Switching models mid-cut costs you nothing but a re-paste.** Your data never moves. This
is the claim the whole project rests on — and it is testable in about two minutes.

---

## Compatibility matrix

| Tool | Reads automatically | Status |
|---|---|---|
| **Claude Code / Claude Desktop (Skills)** | `SKILL.md` (native frontmatter) | ✅ Adapter present |
| **Codex CLI / ChatGPT Codex** | `AGENTS.md` | ✅ Adapter present |
| **Cursor / Windsurf** | `.cursor/rules/*.mdc` | ✅ Adapter present |
| **GitHub Copilot / VS Code** | `.github/copilot-instructions.md` | ✅ Adapter present |
| **ChatGPT (web) / Gemini (web)** | — (paste) | ✅ Manual path documented |
| **Claude.ai (web)** | — (paste) | ✅ Manual path documented |
| **Kimi / 豆包 / 通义 / DeepSeek (web)** | — (upload or paste) | ✅ Manual path documented |
| **Ollama / local models** | — (paste) | ⚠️ Untested — small models may mis-handle the contract |

> ⚠️ **Honesty note.** The *adapter files* are in place and structurally correct. The
> **end-to-end integration has not been tested against every vendor's current loader.**
> Treat the matrix as "this is wired up", not "this is proven". If a loader changes, the
> fallback is always the paste path — which cannot break, because it needs nothing from
> the vendor.

---

## 1. Claude Code / Claude Desktop

The repo already has the right shape: `SKILL.md` with `name:` and `description:` frontmatter.

```bash
git clone https://github.com/adwilds/bodymd
cd bodymd
cp templates/profile.md profile.md     # then edit it
```

Then either drop the folder into your skills directory, or just open a session inside the
repo and say:

> Read SKILL.md. Start today's log.

---

## 2. Codex CLI, Cursor, Copilot

You do not need to explain anything — `AGENTS.md`, `.cursor/rules/bodymd.mdc`, and
`.github/copilot-instructions.md` already point each tool at `SKILL.md` and repeat the
non-negotiable rules (append-only, `source:` required, `unknown` beats a guess).

Open the repo and speak normally:

> Log this meal. 12:30, canteen, rice and fish and greens.

---

## 3. ChatGPT / Gemini / Claude.ai (web chat)

No file access, so you paste. **What to paste, in this order:**

1. The whole of `SKILL.md`
2. The whole of `profile.md`
3. Today's `log/YYYY-MM-DD.md` (or "no log yet today")
4. Your request

A reusable opener:

> You are running the bodymd workflow. Below is the operator manual, then my profile, then
> today's log. Follow the manual exactly. Do not invent numbers — write `unknown` instead.
> Do not rewrite any existing log line.
>
> --- SKILL.md ---
> (paste)
> --- profile.md ---
> (paste)
> --- log ---
> (paste)
>
> Now: log this meal. 12:30, canteen, rice and fish and greens.

Then copy the model's output back into `log/YYYY-MM-DD.md` yourself. **You will feel this
friction on day one** — and that is the point: the file is yours, which is why you can walk
away from this model tomorrow.

---

## 4. Chinese users: Kimi / 豆包 / 通义 / DeepSeek

This is the case bodymd was designed for, and it is the reason the project has a Chinese
front page.

**Why it matters here more than anywhere else:** you are probably forced to move between
豆包, Kimi, DeepSeek, 通义 and Claude depending on the task, the week, and what your company
allows. Every tool you log into has its own data silo. **`换模型不换数据` is not a nice
feature in China — it is the daily reality.**

**Setup (once):**

1. Create a knowledge base / upload a file in your tool of choice (Kimi and 豆包 both
   support this). Upload `SKILL.md` and `profile.md`.
2. Start each session by referencing it, then paste only what changed — today's log.

**Or with no upload support at all (works everywhere):**

> 你正在运行 bodymd 工作流。下面是操作手册、我的档案和今天的记录。严格按手册执行。
> 不要编造数字 —— 不知道就写 `unknown`。不要改写任何已有的记录行。
>
> --- SKILL.md ---
> （粘贴）
> --- profile.md ---
> （粘贴）
> --- 今天 ---
> （粘贴）
>
> 现在：记录这一餐。12:30，食堂，米饭、鱼、青菜。

**中文版详细说明见 [`docs/zh-CN/run-with-any-model.md`](zh-CN/run-with-any-model.md)。**

---

## 5. The actual test: switch models mid-week

Do this once, in week one. It is the only way to know the claim is real.

| Step | Do this | You should see |
|---|---|---|
| 1 | Log Monday–Wednesday with model A | `log/` has three files, all with `source:` |
| 2 | Switch to model B. Paste `SKILL.md` + `profile.md` + the three logs. Ask: *"Summarise my week so far and tell me my next training load."* | The same numbers you got from model A |
| 3 | Run `python3 scripts/parse_log.py log/` | A table that agrees with both models |
| 4 | If model B's numbers differ, the disagreement is **about the estimates, not the data** | — |

**If step 2 works, bodymd works.** If the numbers move when the model moves, the problem is
a missing field in the contract — file it as an issue. That is exactly the bug the data
contract exists to prevent.

---

## 6. What actually breaks when you switch models

| Breaks | Does not break |
|---|---|
| The *style* of advice | Your `log/` history |
| The *estimate* of a portion (different vision models differ) | `profile.md` |
| Whether the tool reads `SKILL.md` automatically | Any number you typed with `source: manual` |
| The *formatting* of the daily report | The deficit (it is arithmetic on your own data) |

**The rule:** the contract protects **facts you recorded**; models are free to disagree
about **estimates you did not**. That separation is the whole design.

---

## 7. Quick reference

```bash
git clone https://github.com/adwilds/bodymd && cd bodymd
cp templates/profile.md profile.md      # edit: height, weight, age, protein target
mkdir -p log

python3 scripts/selftest.py             # prove the repo is sound (no dependencies)
python3 scripts/validate_log.py log/    # check your own logs against the contract
python3 scripts/parse_log.py log/       # weekly aggregate
```

Scripts are **optional**. Every one of them just reads the Markdown you would have written
by hand. If you never run Python, bodymd still works.
