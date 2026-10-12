# bodymd

**A body-management workflow that runs on your own AI. Your data stays in files you own.**

*Point your AI at your body. Keep the data.*

`MIT` (code) · `CC BY-NC-SA 4.0` (docs) · Python 3 standard library only · zero dependencies

> 中文版 → **[吃练记 · 薄肌手册](README.zh.md)**　｜　`bodymd` = body + `.md`

---

## Start here

| | |
|---|---|
| **What it is** | A food-and-training log that lives in **your own Markdown files**, plus four workflows any AI can follow. Two minutes a day. |
| **What it is not** | An app. No account, no server, no database, no subscription, no telemetry. |
| **Who it is for** | Someone cutting fat who already trains, wants the record to outlive switching AI tools, and will spend two minutes a day on it. |
| **What you need** | Any AI you can paste text into. A free tier is enough. Python 3 is optional, for the validator only. |
| **Why it exists** | The app you use now can paywall its scanner, raise the price, or get acquired. Then your 200 logged meals are not something you can carry out the door. Here, the log is a folder you own. |

**→ [Quick start](#quick-start)** ・ **[What a day looks like](#how-it-works)** ・ **[Something is broken](#something-is-broken)** ・ **[FAQ](docs/faq.md)**

**Want to see it before you set anything up?** [`examples/walkthrough.md`](examples/walkthrough.md)
is one complete day plus a Sunday review — the actual files, the actual prompts, and the actual
output of the scripts.

---

## The thing that bothered me

A calorie app has two jobs: hold your food log, and think about it.

It only does the first one squarely. The log lives in their database. When they raise prices,
paywall the photo scanner, or get acquired, none of that is your decision — and the 200 meals
you typed in are not something you can carry out the door.

The second job is worse. The *thinking* is tied to their model. When they swap it, your
workflow changes too, and nobody asked you.

So I split the two apart.

## What this actually is

Not an app. Not a hosted service. No account, no server, no database.

It is a **file format plus a set of instructions**, both written in plain Markdown:

- Your log is a folder of `.md` files. Open it in any editor, in any year.
- The instructions are Markdown too, so any capable model can pick them up.
- You bring your own key, or just paste into the chat window you already pay for.
- This repo stores nothing, runs no inference, and meters no tokens.

Change models on Tuesday. Nothing in your data changes.

## How it works

It is 21:40 and dinner is over. You take two photos — plate before, plate after — and hand
them to your AI with the workflow file. What comes back is not a verdict. It is a row you
are expected to argue with:

```markdown
## Meals
- 21:12 | dinner | 辣椒炒肉 + 米饭 (2 碗) | 720 kcal | P32 C68 F36 | photo: photos/2026-10-12/2112.jpg | source: photo | edited: 米饭按 2 碗计（AI 估 1.5 碗）
- 21:30 | snack | 酸奶 1 杯 | 130 kcal | P6 C15 F5 | photo: photos/2026-10-12/2130.jpg | source: photo | edited: none
```

You fix the rice estimate. You write that correction into `edited:` on the same line. It stays in
the file permanently — so tomorrow's model, a different one, from a different company, starts from
your correction instead of from zero.

**The `edited:` field is the whole product.** It is how a workflow gets more accurate while the
model underneath keeps changing.

Then it totals the day — sleep, intake, expenditure — tells you whether you are inside your
deficit, and gives you exactly one thing to change tomorrow. On Sunday it does the only
calculation that matters: your **weight trend over the last seven days versus the week before**,
and it recalculates your targets from that, not from a formula you typed in once and never
revisited.

## The decision everything else follows from

**§3 of [`SKILL.md`](SKILL.md) is the point of this repository. It is a data contract.**

It defines every field in `profile.md` and `log/YYYY-MM-DD.md`: what is required, what is
optional, what `unknown` means (it is a legal value — a guess is not), and how a correction
gets recorded so it can never be silently overwritten.

Once that contract is stable, the model becomes a replaceable part. That is the only reason
any of this outlives the next model release.

## What's in here

| Path | What it is |
|---|---|
| `SKILL.md` | The operator manual an AI reads. **Start here.** |
| `AGENTS.md` | The same non-negotiables, for tools that read it automatically — Codex CLI, Cursor, Copilot |
| `PRD.md` | Product requirements: scope, user tiers, FR-1..FR-8, compliance, milestones |
| `workflows/` | The four daily workflows: meal log, training log, daily report, weekly review |
| `prompts/` | Standalone prompt files, one per step |
| `templates/` | The file formats your data lives in |
| `docs/run-with-any-model.md` | ⭐ Setup for each tool — Claude Code, Codex, Cursor, ChatGPT, Kimi, 豆包 |
| `docs/troubleshooting.md` | ⭐ **When something breaks.** The ten failures I have seen, with fixes, plus the validator's error codes |
| `docs/` | Why local data, BYOK setup, user guide, dev guide, testing plan, FAQ |
| `scripts/selftest.py` | ⭐ One command proves the whole repo is intact (13 checks, stdlib only) |
| `scripts/` | Reference implementation: contract validator + weekly aggregator |
| `examples/walkthrough.md` | ⭐ **A complete run, start to finish** — one day plus the weekly review, with the real files and the real script output |
| `examples/sample-week.md` | One worked week, with what each lesson changed in this repo |
| `examples/fixtures/` | 8 fabricated test users × 7 days |
| `README.zh.md` | The Chinese front page — `吃练记 · 薄肌手册`, written natively, not translated |
| `docs/zh-CN/` | Chinese versions of the guides, including its own troubleshooting page |

### What your folder looks like

The repo is the instructions. Your data lives beside them — this is the whole data model:

```
your-folder/
├── profile.md               ← fill in once: height, weight, targets, program
├── log/
│   └── 2026-10-12.md        ← one file per day, append-only
├── reports/                 ← generated reports
└── photos/                  ← your meal and training photos
```

Only the first two are required. `profile.md`, `log/`, `reports/` and `photos/` are excluded by
`.gitignore` on purpose — **never commit them to a public repo.**

## Quick start

Nothing to install. Pick the row that matches you:

| Your situation | Go to |
|---|---|
| I use a coding agent | [Path A](#path-a--a-coding-agent) |
| I use a chat window — ChatGPT, Kimi, 豆包, Gemini | [Path B](#path-b--a-plain-chat-window) |
| I only want to see whether any of this holds up | [Path C](#path-c--just-run-the-tests) |

**What you get in the first five minutes:** a `profile.md` with your targets and today's log open
in front of you. You do not need to finish a day to know whether the idea works — one corrected
meal line is enough to see it.

### Path A — a coding agent

Claude Code, Codex CLI, Cursor, Copilot, Gemini CLI.

```bash
git clone https://github.com/adwilds/bodymd && cd bodymd
cp templates/profile.md profile.md     # then open it and put in your real numbers
```

Then:

1. Open the agent **at this folder** — not a parent folder, this one.
2. Say: `Read SKILL.md. Start today's log.`
3. Fill in `profile.md`. It asks for height, weight, protein target, deficit target, training days.
   **`unknown` is a legal answer** for anything you don't know — a guess is not.
4. Log one meal: photograph the plate, hand it over, and look at the line it writes.
5. Correct one number by hand, and watch the `edited:` field appear.

If step 4 produced something that looks like the block in [How it works](#how-it-works), it is
working. If not, [`docs/troubleshooting.md`](docs/troubleshooting.md) starts with exactly this case.

`AGENTS.md` carries the rules for tools that read it automatically; `.cursor/rules/` and
`.github/copilot-instructions.md` do the same job for Cursor and Copilot. That is the whole
install.

### Path B — a plain chat window

ChatGPT, Kimi, 豆包, Gemini, 通义, DeepSeek — anything you can paste text into.

1. Open a new chat.
2. Paste `SKILL.md`, then your `profile.md`. Ask for today's log.
3. Talk to it the way you normally would: *"米饭两碗"*, *"今天没练"*, *"昨晚睡 6 小时"*.
4. At the end of the session, copy the updated log block back into `log/YYYY-MM-DD.md`.

**This is not a downgrade** — it is the same contract, and it is a supported way to use this.
The one thing to remember: a new chat remembers nothing, so steps 1-2 repeat every time. Per-tool
notes: [`docs/run-with-any-model.md`](docs/run-with-any-model.md).

### Path C — just run the tests

```bash
python3 scripts/selftest.py                          # 13 checks → expect 13/13 PASS
python3 scripts/validate_log.py examples/fixtures/   # → expect 0 fatal, 2 warnings
python3 scripts/parse_log.py    examples/fixtures/   # → expect 56 days / 8 personas
```

The third command reads eight test users — Chinese, Chinese-American, British, Mexican,
Nigerian, South Asian, and two more — one week each. **They are fabricated, and they are supposed
to be messy:** a skipped lunch, a scale with dead batteries, a 48 g protein day, a day with no
training logged at all. Disclosure and red lines:
[`examples/fixtures/README.md`](examples/fixtures/README.md).

The **2 warnings are deliberate.** They exist to prove the validator drops a missing optional
field to a warning instead of rejecting the file. Incomplete records are the normal case — a
validator that refuses them is decoration.

## What I have not tested

A README that only lists strengths is an advertisement, so:

- **The per-tool adapters are structurally correct, but I have not load-tested them against
  every vendor's current build.** The files are in place and parse; the end-to-end integration
  with each vendor's own loader has not been verified on each of them. Read the *Compatibility
  matrix* note in [`docs/run-with-any-model.md`](docs/run-with-any-model.md) as "it is wired up",
  not as "it has been verified". The paste-it-in fallback is the one path that cannot break.
- **The contract is version 0.** Field names may still change, and I will say so in the commit
  when they do.
- **The fixtures are plausibility fixtures, not benchmarks.** Do not copy their numbers into a
  `profile.md` and treat them as advice.
- **Nobody has paid for anything here, and that is not currently the point.**

## What this is not

- **Not a medical device.** Nothing here diagnoses, treats, or cures anything.
- **No effect promises.** No weight promise, no timeline, no measurements.
- **Not a replacement for a physician, dietitian, or coach.**
- Every calorie, macro and expenditure number this produces is an **estimate**, and it says so
  in the file.

## Where this came from

The workflow came before the code, deliberately — and you can see that in the repo: the
contract, the workflows and the prompts *are* the product. The two Python scripts exist to
check them, not to run them.

It started as a written-down version of a routine I had seen demonstrated in public —
photograph the plate, get the numbers, eat in a given order, log the set, read one screen at
night, recheck on Sunday — reduced to something that needs no app, no subscription, and no
particular company.

There is a second front page for this project, [`README.zh.md`](README.zh.md), under a
different name — 吃练记. That is not a translation. The Chinese side has a different job:
distribution, and testing whether the demand is real — in the one market where switching
models every few weeks is not a preference but a fact of life. **The data format is identical
in both.**

## Status

Early, and honest about it. Next up, and **not done yet**: running this workflow by hand for
14 days with three people, using free tools, and asking them on day 19 whether they would keep
going without me.

If they would not, the right conclusion is that this is a good personal tool rather than a
product — and that is a fine thing for it to be.

## Something is broken

Four places to look, in this order:

| | |
|---|---|
| **The AI is misbehaving** — invents its own format, asks for things you already gave it, adds advice you did not ask for | [`docs/troubleshooting.md`](docs/troubleshooting.md) — the ten failures I have actually hit, with fixes |
| **A script failed** | Same file, [§8](docs/troubleshooting.md#8-the-validator-says-fatal-or-warn). Every validator code (V1-V9) is mapped to its fix. ⚠️ The validator's console messages are currently in Chinese — that table is the translation |
| **"Should I use this for X?"** | [`docs/faq.md`](docs/faq.md) |
| **None of the above** | [Open an issue](https://github.com/adwilds/bodymd/issues/new/choose) — one template for bugs, one for questions |

When you report something, include:

1. **Which tool and model.** Behaviour differs a lot between models, and it is the first thing I will ask.
2. **The exact output**, not a summary of it.
3. The relevant `log/` day with anything personal removed. **Numbers are safe to share; identity is not.**
4. If a script failed: the full command and its complete output.

This is a side project, so issues get answered in batches. A report I can reproduce gets fixed
far faster than one I have to guess at.

## Contributing

Issues and workflow improvements are welcome — especially from people who ran it for a week and
found where it breaks. That is the most useful thing anyone can send me.

**Feature requests that begin "you should build an app" will be closed.** That is the one problem
this project exists to not have.

## License

- Code, workflows, templates: **MIT**
- Documentation and long-form writing: **CC BY-NC-SA 4.0**
- **Commercial use** — internal deployment at a company, delivery to a client, or bundling
  into a paid product — **requires a license.** Open an issue and ask.
