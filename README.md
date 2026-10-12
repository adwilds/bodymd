# bodymd

**A body-management workflow that runs on your own AI. Your data stays in files you own.**

*Point your AI at your body. Keep the data.*

`MIT` (code) · `CC BY-NC-SA 4.0` (docs) · Python 3 standard library only · zero dependencies

> 中文版 → **[吃练记 · 薄肌手册](README.zh.md)**　｜　`bodymd` = body + `.md`

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
- 21:12 辣椒炒肉 + 米饭 (2 碗) | 720 kcal · protein 32 g | order: protein first ✗ | source: photo · conf: medium
- 21:30 一杯酸奶 | 130 kcal · protein 6 g | source: photo
- edited: 米饭 按 2 碗计（AI 估 1.5 碗）；用户改
```

You fix the rice estimate. You write down that you fixed it. The correction stays in the file
permanently — so tomorrow's model, a different one, from a different company, starts from your
correction instead of from zero.

That last line is the whole product. **`edited:` is how a workflow gets more accurate while
the model underneath keeps changing.**

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
| `docs/` | Why local data, BYOK setup, dev guide, user guide, testing plan, FAQ |
| `scripts/selftest.py` | ⭐ One command proves the whole repo is intact (13 checks, stdlib only) |
| `scripts/` | Reference implementation: contract validator + weekly aggregator |
| `examples/sample-week.md` | One worked week, with what each lesson changed in this repo |
| `examples/fixtures/` | 8 fabricated test users × 7 days |
| `README.zh.md` | The Chinese front page — `吃练记 · 薄肌手册`, written natively, not translated |
| `docs/zh-CN/` | Chinese versions of the guides |

## Install

### If you use a coding agent — Claude Code, Codex CLI, Cursor, Copilot, Gemini CLI

```bash
git clone https://github.com/adwilds/bodymd && cd bodymd
cp templates/profile.md profile.md     # fill in your baseline once
```

Then, in the agent:

> Read SKILL.md. Start today's log.

`AGENTS.md` carries the rules for tools that read it automatically; `.cursor/rules/` and
`.github/copilot-instructions.md` do the same job for Cursor and Copilot. That is the whole
install.

### If you use ChatGPT, Kimi, 豆包 — or any plain chat window

There is nothing to install. Paste or upload `SKILL.md` with your `profile.md`, ask for today's
log, and paste the updated file back at the end of the session. **This is not a downgrade** —
it is the same contract, and it is a supported way to use this. Per-tool notes:
[`docs/run-with-any-model.md`](docs/run-with-any-model.md).

### If you just want to see whether any of this holds up

```bash
python3 scripts/selftest.py                          # 13 checks → expect 13/13 PASS
python3 scripts/validate_log.py examples/fixtures/   # → expect 0 fatal, 2 warnings
python3 scripts/parse_log.py    examples/fixtures/   # → expect 56 days / 8 personas
```

The third command reads eight test users — Chinese, Chinese-American, British, Mexican,
Nigerian, South Asian — one week each. **They are fabricated, and they are supposed to be messy:**
a skipped lunch, a scale with dead batteries, a 48 g protein day, a day with no training
logged at all. Disclosure and red lines: [`examples/fixtures/README.md`](examples/fixtures/README.md).

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

## Contributing

Issues and workflow improvements are welcome, especially from people who actually ran the
thing for a week and found where it breaks.

**Feature requests that begin "you should build an app" will be closed.** That is the one
problem this project exists to not have.

## License

- Code, workflows, templates: **MIT**
- Documentation and long-form writing: **CC BY-NC-SA 4.0**
- **Commercial use** — internal deployment at a company, delivery to a client, or bundling
  into a paid product — **requires a license.** Open an issue and ask.
