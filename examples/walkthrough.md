# A complete example — one day, start to finish

This is what actually happens when you use bodymd. Not a feature list — a session.

Read it once before you start. It takes four minutes and it removes every guess about what goes
where. Everything below is a real run: the log files validate clean, and the command output at
the bottom is copied from the actual scripts.

**What you need:** a phone, a folder, and any AI you can paste text into.
**What it costs per day:** about two minutes.

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

Then open it and put in your numbers:

```yaml
height_cm: 172
weight_kg: 75.0
body_fat_est_pct: 29
protein_target_g: 145
deficit_target_kcal: 600
training_days_per_week: 3.5
program: [deadlift, squat, bench]
created: 2026-10-12
```

**If you don't know a number, write `unknown`.** It is a legal value. A guess is not — a guess
gets treated as data, and then every later calculation inherits your guess.

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
- 13:05 | lunch | 鸡胸 150g + 米饭 + 西兰花 | 570 kcal | P54 C55 F15 | photo: photos/2026-10-12/1305_lunch.jpg | source: photo | edited: 米饭 150g->120g
```

`edited:` records **what you changed and why**. Not bookkeeping — this is the accuracy loop.
Tomorrow's model, possibly a different company's model, reads that line and starts from your
number instead of from zero.

**Eating order** is not a field in the log; it is advice attached to the meal. Protein first,
vegetables second, starch last (the rule is `SKILL.md` §4.2). You act on it; the log just records
that you ate.

---

## Step 4 — training. Video for the movement, voice for the weight.

You film the set, and you say the number out loud: **"60 公斤。"**

That split is not laziness, it is the honest limit of the technology — a camera can count reps and
recognise the lift, and it **cannot** read the number printed on the plate. Any tool that claims
otherwise is asking you to type it or reading it off your watch. See `SKILL.md` §5.1.

```markdown
## Training
- exercise: deadlift | set: 1 | reps: 12 | load_kg: 60 | rpe: 7 | source: video+voice
- exercise: deadlift | set: 2 | reps: 12 | load_kg: 60 | rpe: 7 | source: video+voice
- exercise: deadlift | set: 3 | reps: 12 | load_kg: 60 | rpe: 8 | source: video+voice
- session_burn_kcal: 275 | source: estimated
```

> **Rest day?** Omit the whole `## Training` section. Writing `- rest day` inside it makes the
> validator treat that line as a training set and fail. Say it in `## Notes` instead:
> `- Rest day, no training section.`

Then it answers the question you actually have — what do I put on the bar next time:

> All three sets completed at target RPE. Lower body, so +5 kg → **deadlift @65 kg next session.**

That arithmetic is `SKILL.md` §5.2, and it is deterministic: the same log gives the same answer in
any tool. The model is not guessing here.

---

## Step 5 — end of day. The report is one screen.

Say **"report"**. What comes back:

```
# Daily report — 2026-10-12

Deficit       445 kcal        target <=600      [ok]
Protein       134 / 145 g                       [-11 g]
Sleep         7h 20m                            oura
Training      deadlift 3x12 @60kg  RPE 7-8      done
Next session  deadlift @65kg

## What changed
- protein 11 g short: the 25 g shake never got logged today

## Notes
- lunch estimate edited downward (rice 150g -> 120g)
- hotpot dipping sauce estimated at half a bowl — the weakest number today
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
| 2026-10-12 | 1,705 | 134 | 2,150 | 445 | deadlift 3×12 @60 | 75.0 |
| 2026-10-13 | 1,840 | 139 | 2,200 | 360 | squat 3×5 @100 | 74.8 |
| 2026-10-14 | 1,620 | 118 | 2,100 | 480 | rest | 74.7 |
| 2026-10-15 | 1,950 | 150 | 2,250 | 300 | bench 3×8 @60 | 74.9 |
| 2026-10-16 | 2,240 | 108 | 2,150 | −90 | rest | 74.5 |
| 2026-10-17 | 1,780 | 120 | 2,300 | 520 | deadlift 3×5 @105 | 74.4 |
| 2026-10-18 | 1,690 | 102 | 2,050 | 360 | rest | 74.2 |

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
- weight trend is inside the 0.3-0.6 kg/week band: the calorie side is working
- protein adherence is the failure: 3 of 7 days, and the three misses are
  exactly the non-training days

Proposed change
- no calorie change. Per the rule below, do not touch calories while adherence
  is the problem.
- fix the input side instead: log the 25 g shake on rest days as a standing item

Changed profile.md? NOT YET — waiting for your confirmation.
```

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
--------------------------------------------------------
检查 7 个文件：致命 0 项，警告 0 项
```

Exit code `0` = clean, `1` = at least one fatal, `2` = warnings only. Each code (V1-V9) and the
exact fix is in [`../docs/troubleshooting.md`](../docs/troubleshooting.md) §8.

And the aggregator, which reads the same files:

```bash
python3 scripts/parse_log.py .
```

```
bodymd 聚合 —— 7 天 / 7 个档案
============================================================================
档案          日期                 摄入     蛋白      消耗      缺口    训练组  来源
----------------------------------------------------------------------------
2026-10-12  2026-10-12      1,705    134   2,150     445      3  totals
2026-10-13  2026-10-13      1,840    139   2,200     360      3  totals
2026-10-14  2026-10-14      1,620    118   2,100     480      0  totals
2026-10-15  2026-10-15      1,950    150   2,250     300      3  totals
2026-10-16  2026-10-16      2,240    108   2,150     -90      0  totals
2026-10-17  2026-10-17      1,780    120   2,300     520      3  totals
2026-10-18  2026-10-18      1,690    102   2,050     360      0  totals
```

⚠️ Read the `档案` (record) column carefully when you use the one-file-per-day layout: it labels
each row with the date, so it reports "7 天 / 7 个档案" instead of "7 days / 1 person". The numbers
are right — the label is just counting files. Known wart, not yet fixed.

---

## Appendix B — the failures this example does *not* hide

- **Day 5 (16 Oct) went over.** Deficit −90. The report says so without drama, and the weekly
  average absorbs it.
- **Protein adherence was 3 of 7.** The week was a calorie success and a protein failure, and the
  review says that plainly.
- **The dipping sauce was a guess.** It is labelled a guess in `## Notes`.
- **Macro arithmetic does not close exactly.** Most days the macros re-add to within 30-80 kcal of
  the stated intake, because portions and fibre are rounded. Real logs look like this. The
  validator does not require the arithmetic to close, and neither should you.

---

**Related:** [`sample-week.md`](sample-week.md) shows a different week's reports without the
step-by-step. [`../docs/troubleshooting.md`](../docs/troubleshooting.md) is what to read when this
example does not match what you got.
