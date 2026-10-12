# Troubleshooting

Two things go wrong in this project: **the AI does something the contract does not allow**, or
**the files fail validation**. Find your symptom below and apply the fix.

Everything here is a failure I have actually seen, not a hypothetical. If your problem is not
listed, [report it](#reporting-a-problem) — that is how this page grows.

---

## Quick index

| Symptom | Section |
|---|---|
| The AI invents its own format, or ignores `SKILL.md` | [1](#1-the-ai-ignores-the-format) |
| Numbers look wrong | [2](#2-the-estimates-are-wrong) |
| It asks for things I told it last time | [3](#3-it-keeps-asking-for-things-i-already-told-it) |
| It gives medical advice, or moralises about my food | [4](#4-the-ai-gives-advice-i-did-not-ask-for) |
| The report is a wall of text | [5](#5-the-report-is-too-long) |
| It wants the barbell weight from a video | [6](#6-it-wants-me-to-log-load-from-a-video) |
| Yesterday's entry changed | [7](#7-it-rewrote-an-entry-i-already-wrote) |
| A script failed, in a language I can't read | [8](#8-the-validator-says-fatal-or-warn) |
| My coding agent never picks up the rules | [9](#9-my-coding-agent-ignores-skillmd-and-agentsmd) |
| Am I about to leak my health data? | [10](#10-what-never-goes-into-a-public-repo) |

---

## 1. The AI ignores the format

**Cause, in 9 cases out of 10:** the tool was not opened at the repository folder, or `SKILL.md`
was never loaded into the conversation.

| Your setup | Fix |
|---|---|
| A coding agent (Claude Code, Codex CLI, Cursor, Copilot) | Open the agent **at the repo folder**, not a parent folder. Then say: *"Read SKILL.md. Start today's log."* |
| A plain chat window (ChatGPT, Kimi, 豆包, Gemini, 通义, DeepSeek) | Paste `SKILL.md` **at the start of every new conversation**. A new chat has no memory of the last one. |
| An uploaded knowledge base | Upload `SKILL.md` + your `profile.md` once, then say *"Follow SKILL.md §3.3 exactly."* |
| Still drifting | Say: *"Stop. Re-read SKILL.md §3.3. Output only the daily log block."* Naming the section number is the strongest correction available. |

If it keeps happening after that, the model may be too small for a multi-file instruction. Paste
in `SKILL.md` §3 only — the contract is the part that matters, and it fits in one message.

---

## 2. The estimates are wrong

| Case | Expected accuracy | What to do |
|---|---|---|
| Simple plate — chicken, rice, broccoli | roughly ±10-15% | Accept it |
| Mixed dish — curry, stir-fry, stew | materially worse | **Say what was cooked**, not just what you see. "Stir-fried in 2 tbsp oil" changes the number more than any model upgrade |
| Restaurant food | the weakest case | Portions and hidden fats are invisible. Estimate the whole meal as one line, then `edited:` it |

**The largest single source of error is hidden fat.** Oil, butter, sesame paste, cheese, sauces.
If your numbers are consistently low, this is why — before blaming the model.

When you correct an estimate, you must write it in `edited:`:

```markdown
- 12:30 番茄炒蛋 + 米饭 | 540 kcal · protein 22 g | source: photo | edited: 米饭按 2 碗计，AI 估 1.5 碗
```

That line is not bookkeeping. It is what makes tomorrow's model — possibly a different one —
start from your correction instead of from zero. See `SKILL.md` §3.4.

---

## 3. It keeps asking for things I already told it

**Cause:** the chat session is stateless. Nothing is remembered between conversations.

**Fix:** the memory lives in files, not in the chat.

- `profile.md` — your baseline: height, weight, targets, constraints. Fill it in **once**.
- `log/YYYY-MM-DD.md` — every day. Feed the last 7 days together when you ask for the weekly review.

If you are pasting into a chat window, paste `profile.md` + the log files along with `SKILL.md`.
Yes, that is three things to paste. It is still the only workflow where the memory survives the
tool.

---

## 4. The AI gives advice I did not ask for

The contract forbids it. `SKILL.md` §7 is the guardrail list; §9 is the "I want an app" script.

Paste this to put it back on rails:

> Re-read SKILL.md §7. You are a logging system, not a coach. Output the log block and the daily
> report. No medical advice, no moralising, no effect promises.

If a model insists on adding commentary, that is a model problem, not a contract problem — switch
models. The data does not care.

---

## 5. The report is too long

Say **"one screen"**. It will cut. The daily report is specified in `SKILL.md` §6 and is not a
place for essays.

If it overruns even at "one screen", ask for the two headline numbers only: the deficit and the
protein gap.

---

## 6. It wants me to log load from a video

It cannot. `SKILL.md` §5.1 is explicit: exercise type and rep count are detectable from video,
**load is not** — a camera cannot read the number printed on the plate.

Say the weight out loud, or type it. Two seconds.

If you have no wearable, expenditure stays an estimate. That is accepted; do not let a tool
invent precision it does not have.

---

## 7. It rewrote an entry I already wrote

The log is **append-only** (`SKILL.md` §3.4). A correction is a **new** `edited:` line, never a
silent overwrite of the old one — you need to be able to see that the number changed and why.

Recovery:

1. If you keep the folder in git: `git diff` to see exactly what changed, `git checkout` to undo.
2. Otherwise: the previous figure is usually in your chat history — copy it back and add the
   `edited:` line.
3. Then tell the AI: *"The log is append-only. Never rewrite an existing line."*

This is also the argument for backing the folder up with git, even privately. Two of the eight
fixture personas exist precisely to test this class of mess.

---

## 8. The validator says FATAL or WARN

**A warning is not a failure.** The validator is written so that an incomplete record degrades to
a warning instead of being rejected — recording badly is normal, and a validator that refuses your
real day is decoration. Only `FATAL` blocks.

```bash
python3 scripts/validate_log.py log/
```

Exit code `0` = pass · `1` = fatal present · `2` = warnings only.

⚠️ **The validator's console messages are currently in Chinese.** This table is the mapping.

| Code | Level | Meaning | Fix |
|---|---|---|---|
| V1 | FATAL | Meal line has fewer than 6 `|`-separated fields | Re-check the line structure in `SKILL.md` §3.3 |
| V2 | FATAL | No `source:` on the line | Every nutrition record must state its source |
| V3 | FATAL | `source:` value not allowed | Legal values: `photo`, `voice`, `manual`, `wearable`, `video+voice`, `estimated` |
| V4 | WARN | No `edited:` field | Write `edited: none` if you changed nothing |
| V5 | FATAL | No kcal number and no explicit `unknown` | Either the number, or the literal word `unknown` |
| V6 | FATAL | Training line missing `exercise:` or `reps:` | Both are required |
| V7 | WARN | Training line missing `load_kg:` | Use `unknown` when you cannot confirm it; `bodyweight` for bodyweight lifts |
| V8 | WARN | Time is not `HH:MM` | 24-hour format, zero-padded |
| V9 | INFO | No `## Meals` or `## Training` section found | Rest days are fine; a missing Meals section usually means the heading was renamed |
| — | FATAL | File is not UTF-8 | Re-save the file as UTF-8 |

Expected output on a healthy repo:

```bash
python3 scripts/selftest.py                          # 13 checks → 13/13 PASS
python3 scripts/validate_log.py examples/fixtures/   # → 0 fatal, 2 warnings (both intended)
python3 scripts/parse_log.py    examples/fixtures/   # → 56 days / 8 personas
```

The **2 warnings are deliberate**: they prove the validator downgrades a missing optional field
instead of rejecting the file.

---

## 9. My coding agent ignores SKILL.md and AGENTS.md

Check the file actually exists at the path your tool expects:

| Tool | File it reads | Present in this repo |
|---|---|---|
| Codex CLI, and tools following the `AGENTS.md` convention | `AGENTS.md` | yes |
| Cursor | `.cursor/rules/bodymd.mdc` | yes |
| GitHub Copilot | `.github/copilot-instructions.md` | yes |
| Claude Code and others | `SKILL.md`, loaded on request | yes |

Two real limits, stated plainly:

- **These adapters are wired up, not load-tested against every vendor's current build.** If your
  tool's loader changed, the fallback that cannot break is pasting `SKILL.md` into the chat.
- Some agents only read `AGENTS.md` from the repository root and will not follow it up the tree.
  Open the folder that *contains* `AGENTS.md`.

---

## 10. What never goes into a public repo

Your health data is a folder on your device. This project has no server, no analytics, no
telemetry — so the only way to leak it is to publish it yourself.

`.gitignore` already excludes `profile.md`, `log/`, `reports/` and `photos/`. Keep it that way.

- **Never** commit `log/` or `profile.md` to a public repo.
- **Careful with cloud sync**: a synced folder means that cloud now holds your health data. That
  may be fine — just decide it deliberately.
- **When asking for help**, paste numbers, never identity. The report format contains no name,
  address, or account. Replace anything personal with `REDACTED`.

---

## Reporting a problem

[Open an issue](https://github.com/adwilds/bodymd/issues/new/choose). Two templates: one for a
bug, one for a question.

**Include:**

1. Which tool and model (e.g. "ChatGPT, GPT-5.1" / "Claude Code, Sonnet 4.5"). Model behaviour
   differs, and this is the first thing I will ask.
2. What you did, and what came back — the exact output, not a summary.
3. The relevant `log/` day, with anything personal removed. Numbers are safe; identity is not.
4. If a script failed: the full command and its complete output.

**Fast to fix:** the contract, the validator, the workflows, the prompts, the fixtures.

**Will be closed:** "you should build an app", "add a mobile UI", "make it sync", "auto-detect
weight from video". Those are the problems this project exists to not have — `SKILL.md` §5.1 and
§9 explain why.
