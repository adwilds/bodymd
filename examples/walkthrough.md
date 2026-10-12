# A complete example — one day, start to finish

This is what actually happens when you use bodymd. Not a feature list — a session.

Read it once before you start. It takes four minutes and it removes every guess about what goes
where. Every log line below was run through the repository's own validator and aggregator, and the
command output in the appendix is copied from those scripts — not written by hand.

**What you need:** a phone, a folder, and any AI you can paste text into.
**What it costs per day:** about two minutes.

> **About the numbers below.** They belong to one notional example person. There is no real user
> behind them and they are not the author's. They are kept internally consistent on purpose — so
> that you can check the arithmetic yourself, and so that you catch it immediately if your model
> produces numbers that do not reconcile.

---

## Step 0 — the shape of it

```
your-folder/
├── profile.md            ← written once, in step 1
└── log/
    └── 2026-10-12.md     ← one file per day, append-only
```

That is the whole system. No account, no sync, no app.

---

## Step 1 — `profile.md`, written once

```bash
cp templates/profile.md profile.md
```

Then open it and replace the example values with yours:

```yaml
# Baseline
height_cm: 176
weight_kg: 75.0
body_fat_est_pct: unknown
age: unknown
sex: unknown

# Targets
protein_target_g: 145
deficit_target_kcal: 600
weekly_weight_change_target_pct: 0.5

# Training
training_days_per_week: 3.5
program: [deadlift, squat, bench]
increments_kg:
  upper: 2.5
  lower: 5.0

# Data sources
wearable: none
ai_tool: any

# Meta
created: 2026-10-12
last_reviewed: 2026-10-12
```

**If you don't know a number, write `unknown`.** It is a legal value — see `body_fat_est_pct`
above. A guess is not: a guess gets treated as data, and then every later calculation inherits
your guess.

Two of these keys drive everything downstream and are worth getting roughly right:
`protein_target_g` (start at 1.8-2.2 g per kg of bodyweight) and `deficit_target_kcal`
(start at 400-600). The rest are context so your AI does not re-ask you the same question every
week.

You will not edit this file again for a week. The weekly review is the only thing allowed to
change it, and only after you say yes.

---

## Step 2 — breakfast. Photo in, one line out.

You photograph the plate and say:

> 燕麦 60g，鸡蛋 3 个，牛奶 250ml

What comes back is not a verdict. It is a row you are expected to argue with:

```
items:        oats 60 g | 3 eggs | milk 250 ml
total:        505 kcal | P42 C48 F16
confidence:   medium
eating_order: [eggs, milk, oats]
```

Then it writes that into `log/2026-10-12.md`:

```markdown
## Meals
- 08:20 | breakfast | 燕麦 60g + 鸡蛋 3 个 + 牛奶 250ml | 505 kcal | P42 C48 F16 | photo: photos/2026-10-12/0820_breakfast.jpg | source: photo | edited: none
```

Two things to notice, because they are the whole design:

- **`source: photo`** — every number carries where it came from. `unknown` is legal; silence is not.
- **`edited: none`** — nothing was corrected, and the file says so. On a day where you correct
  something, that field is the most valuable line in the file (see step 3).

---

## Step 3 — lunch, and the one correction that matters

Photo of lunch. The AI says 640 kcal and puts the rice first.

Both are wrong-ish, and you fix both:

```
- 13:05 | lunch | 鸡胸 150g + 米饭 + 西兰花 | 570 kcal | P54 C55 F15 | photo: photos/2026-10-12/1305_lunch.jpg | source: photo | edited: 米饭 150g->120g | order_ok: no
```

`edited:` records **what you changed and why**. Not bookkeeping — this is the accuracy loop.
Tomorrow's model, possibly a different company's model, reads that line and starts from your
number instead of from zero.

**Eating order** is advice, not a field — protein first, vegetables second, starch last
(`SKILL.md` §4.2). But it is *checked*: after the meal you answer one question, and the answer goes
on the line as `order_ok: no`. One word, and it is the difference between a suggestion the system
can learn from and a suggestion it repeats forever. Almost nobody logs this. That is why almost
nobody knows whether eating protein first actually does anything for them.

> You will only ever be asked this once per meal, and you can ignore the question. Everything else
> in this file still works.

---

## Step 4 — training. Video for the movement, voice for the weight.

You film the set, and you say the number out loud: **"85 kilos."**

That split is not laziness, it is the honest limit of the technology — a camera can count reps and
recognise the lift, and it **cannot** read the number printed on the plate. Any tool that claims
otherwise is asking you to type it or reading it off your watch. See `SKILL.md` §5.1.

```markdown
## Training
- exercise: deadlift | set: 1 | reps: 8 | load_kg: 85 | rpe: 7 | source: video+voice
- exercise: deadlift | set: 2 | reps: 8 | load_kg: 85 | rpe: 7 | source: video+voice
- exercise: deadlift | set: 3 | reps: 8 | load_kg: 85 | rpe: 8 | source: video+voice
- session_burn_kcal: 250 | source: estimated
```

> **Rest day?** Omit the whole `## Training` section. Writing `- rest day` inside it makes the
> validator treat that line as a training set and fail. Say it in `## Notes` instead:
> `- Rest day, no training section.`

Then it answers the question you actually have — what do I put on the bar next time:

> All three sets completed at target RPE. Lower body, so +5 kg → **deadlift @90 kg next session.**

That arithmetic is `SKILL.md` §5.2, and it is deterministic: the same log gives the same answer in
any tool. The model is not guessing here. Check it at step 6: the next deadlift session in the week
really is 90 kg, because that is the load the log prescribed.

---

## Step 5 — end of day. The report is one screen.

Say **"report"**. What comes back:

```
# Daily report — 2026-10-12

Deficit       445 kcal        target <=600      [ok]
Protein       134 / 145 g                       [-11 g]
Sleep         7h 20m                            oura
Training      deadlift 3x8 @85kg  RPE 7-8      done
Next session  deadlift @90kg

## What changed
- protein 11 g short: the 25 g shake never got logged today

## Notes
- lunch estimate edited downward (rice 150g -> 120g)
- the beef stew was ladled from a pot, no scale — the weakest number today
```

Three rules make this different from a dashboard: it **fits on a phone screen**, it carries **no
alarming language** (no "you failed", no broken streaks), and there is **exactly one actionable
line**. A list of ten things to fix is the same as a list of zero.

Sleep came from an Oura ring (`source: oura`). A watch, a phone, or a guess is equally acceptable —
the field records which one it was, and nothing downstream pretends the guess was a measurement.

---

## Step 6 — the week, as it actually accumulated

Seven files, one per day. Rest days simply have no Training section.

| Date | Intake | Protein | Expenditure | Deficit | Training | Weight |
|---|---|---|---|---|---|---|
| 2026-10-12 | 1,705 | 134 | 2,150 | 445 | deadlift 3×8 @85 | 75.0 |
| 2026-10-13 | 1,840 | 139 | 2,200 | 360 | squat 3×8 @80 | 74.8 |
| 2026-10-14 | 1,620 | 118 | 2,100 | 480 | rest | 74.7 |
| 2026-10-15 | 1,950 | 150 | 2,250 | 300 | bench 3×8 @50 | 74.9 |
| 2026-10-16 | 2,240 | 108 | 2,150 | −90 | rest | 74.5 |
| 2026-10-17 | 1,780 | 120 | 2,300 | 520 | deadlift 3×8 @90 | 74.4 |
| 2026-10-18 | 1,690 | 102 | 2,050 | 360 | rest | 74.2 |

Weights come from `## Body`, one line per morning weigh-in (`source: scale`). The weekly review uses
their 7-day mean and ignores any single day, because daily fluctuation is mostly water.

Read the Training column against step 4: the progression prescribed there — 85 kg, +5, so 90 kg —
is the load that actually appears on 17 Oct. Nothing had to be carried between sessions by memory.

---

## Step 7 — Sunday. This is the step that makes it not a diary.

**The diary records. The review recalculates.** (`workflows/04-weekly-review.md`)

```
Week 42 review  (12 Oct - 18 Oct)

Average deficit      339 kcal / day
Weight trend         74.6 kg   (-0.4 kg vs last week)
Protein adherence    3 of 7 days
Training             4 of 4 sessions

Assessment
- weight trend is inside the 0.3-0.7% band: the calorie side is working
- protein adherence is the failure: 4 of the 7 days fell short, and three of
  those four are rest days

Proposed change
- no calorie change. Per the rule below, do not touch calories while adherence
  is the problem.
- fix the input side instead: log the 25 g shake on rest days as a standing item

Changed profile.md? NOT YET — waiting for your confirmation.
```

Two things about those numbers, because they are exactly where a fake example would cheat:

- **"3 of 7" is measured at 90% of target, not 100%** — 3 days reached at least 130.5 g of the
  145 g target. That threshold is written down in `workflows/04-weekly-review.md`, not chosen to
  make the week look better.
- **The date range and the ISO week number are both stated** so the seven days are unambiguous.

The rule that produced that answer is written down, not vibed:

```
if protein adherence < 5 of 7 days   ->  do not change calories; fix protein first
```

**Never adjust calories while adherence is the problem.** A plan that is not being executed is not
a plan that needs tuning. Most apps do the opposite — they see a slow week and change the target.

Two mechanics worth keeping:

- **Weight trend uses the 7-day mean, never a single day.** Daily fluctuation is mostly water.
- **`profile.md` is only rewritten after you confirm.** The system never edits your baseline behind
  your back.

---

## Step 8 — Monday. Different model, no migration.

Open a different tool. Paste `SKILL.md` and last week's files. Ask for today.

It reads your `edited:` corrections, it knows your best squat set, it knows the shake was the leak.
**Nothing gets exported, converted, or re-entered.** That is the entire reason the format is this
rigid.

---

## Appendix A — check your own log

```bash
python3 scripts/validate_log.py log/
```

Run against the seven files above, the real output is:

```
[通过]   log/2026-10-12.md
[通过]   log/2026-10-13.md
[通过]   log/2026-10-14.md
  [INFO] 第 0 行：未找到 ## Training 段落（休息日可接受）
[通过]   log/2026-10-15.md
[通过]   log/2026-10-16.md
  [INFO] 第 0 行：未找到 ## Training 段落（休息日可接受）
[通过]   log/2026-10-17.md
[通过]   log/2026-10-18.md
  [INFO] 第 0 行：未找到 ## Training 段落（休息日可接受）
--------------------------------------------------------
检查 7 个文件：致命 0 项，警告 0 项
```

(The blank lines between files are trimmed above, nothing else. The three `[INFO]` lines are
the rest days — a missing `## Training` section is *reported*, not punished.)

Exit code `0` = clean, `1` = at least one fatal, `2` = warnings only. Each code (V1-V9) and the
exact fix is in [`../docs/troubleshooting.md`](../docs/troubleshooting.md) §8.

And the aggregator, which reads the same files:

```bash
python3 scripts/parse_log.py .
```

```
bodymd 聚合 —— 7 天 / 1 个档案
============================================================================
档案          日期                 摄入     蛋白      消耗      缺口    训练组  来源
----------------------------------------------------------------------------
log         2026-10-12      1,705    134   2,150     445      3  totals
log         2026-10-13      1,840    139   2,200     360      3  totals
log         2026-10-14      1,620    118   2,100     480      0  totals
log         2026-10-15      1,950    150   2,250     300      3  totals
log         2026-10-16      2,240    108   2,150     -90      0  totals
log         2026-10-17      1,780    120   2,300     520      3  totals
log         2026-10-18      1,690    102   2,050     360      0  totals

按 ISO 周聚合（周复盘的三个变量）
====================================================================================
档案        ISO 周        天         平均缺口       体重均值         趋势         蛋白达标     训练
------------------------------------------------------------------------------------
log       2026-W42    7       339 kcal   74.64 kg         ——    3/7 @145g   4 天

读法：
  · 体重趋势 = 当周 7 天体重均值 − 上一周 7 天体重均值。首周显示「——」是正常的。
  · 蛋白达标按目标的 90% 计（不是 100%），见 workflows/04-weekly-review.md。
  · 只有一周数据时，周对周规则无法判定 —— 这不是脚本的缺陷，是数据的缺陷。
```

**Look at the last table.** It contains all three of step 7's numbers: `339 kcal`, the weight mean
`74.64 kg` (reported as `74.6` in the review), and `3/7` adherence. They are a **script's output**,
not a model's arithmetic. That is the whole argument for a rigid line format: the review stops
being the model's opinion about your week and becomes a computation over your files.

**And the `——` in the trend column is the honest part.** With one week of data, "falling" and
"flat for two weeks" are unanswerable — those rules are statements about *two* weeks. A tool that
printed a number there would be inventing one. `CN-01` in
[`fixtures/personas.md`](fixtures/personas.md) is the two-week case where a real trend appears.

The `档案` (record) column reads `log` because that is the **folder** name. The folder is the
identity when you keep one file per day — so if you later keep two people's logs, use
`log-alice/` and `log-bob/` and the same command reports two records.

**The date range and the ISO week number are printed together** (`2026-W42`) so the seven days
are never ambiguous. Week 42 of 2026 is 12–18 October; if your tool and the script disagree about
which days that is, you will see it here rather than three weeks later in a wrong conclusion.

---

## Appendix B — the failures this example does *not* hide

- **Day 5 (16 Oct) went over.** Deficit −90. The report says so without drama, and the weekly
  average absorbs it.
- **Protein adherence was 3 of 7**, measured at 90% of target. The week was a calorie success and a
  protein failure, and the review says that plainly instead of changing the calorie target.
- **The dipping sauce was a guess.** It is labelled a guess in `## Notes`. So is the group meal on
  day 5, which is entered as one line with confidence `low`.
- **Order adherence was 1 in 3 meals.** `order_ok: yes` on one, `no` on the other two, every day of
  the week. The advice was given and mostly not followed, and that fact is recorded rather than
  quietly dropped — which is the only way anyone ever finds out whether the rule works.
- **Macro arithmetic does not close exactly.** Across these seven days the macros re-add to within
  70 kcal of the stated intake for every meal, and almost always *below* it: fibre counts as
  carbohydrate but does not yield the full 4 kcal/g, and portions are rounded. The validator does
  not require the arithmetic to close, and neither should you — **a log in which every number
  reconciles perfectly is a log somebody fitted to look good.**

---

**Related:** [`sample-week.md`](sample-week.md) shows a different week's reports without the
step-by-step. [`../docs/troubleshooting.md`](../docs/troubleshooting.md) is what to read when this
example does not match what you got.
