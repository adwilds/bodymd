# Workflow 04 — Weekly review

**Trigger:** 7 days elapsed since the last review, or the user asks for a week review.

**Goal:** recalculate targets from what actually happened, not from what was planned.

This is the step that separates bodymd from a calorie diary. **The diary records. The review recalculates.**

---

## Steps

1. Read the last 7 daily reports.
2. Compute the three weekly aggregates (or read them from `scripts/parse_log.py`).
3. Compare against `profile.md`.
4. Propose target changes, with the arithmetic shown.
5. Write the changes back to `profile.md` **only after the user confirms**.
6. Save the review to `reports/week-YYYY-WW.md`.

---

## The three aggregates

| Aggregate | Formula | What it tells you |
|---|---|---|
| **Average deficit** | mean of daily deficit | whether the plan matches reality |
| **Weight trend** | 7-day mean vs previous 7-day mean (needs a weight on >= 4 of the 7 days, else `——`) | the ground truth |
| **Protein adherence** | days hitting >=90% of target, out of 7 | whether the intake side is actually being executed |

**Use the 7-day mean, never a single day's weight.** Daily fluctuation is mostly water.

**Where these three numbers come from.** The aggregator computes all of them, grouped by ISO
week, so the arithmetic is reproducible instead of retyped:

```bash
python3 scripts/parse_log.py log/                 # reads protein_target_g from profile.md
python3 scripts/parse_log.py log/ --protein=150   # or state the target explicitly
```

Its second table prints one row per ISO week with exactly these three columns plus the trend
against the previous week. **Read that table rather than re-deriving it** — a second
implementation of the same formula will disagree with the first one eventually, and then you
will not know which number to trust.

Three things the script deliberately refuses to do:

- **It will not invent a trend from one week.** A first week prints `——`. "Falling" and
  "flat for two weeks" are statements about two weeks; with one week of data they are unanswerable.
- **It will not call two stray weigh-ins a "7-day mean".** If fewer than 4 of the week's days
  carry a weight, the weight mean *and* the trend print `——`. Three or fewer readings is not a
  sample: one is a Monday after a salty weekend, the other a Sunday morning before breakfast, and
  their difference is water — but a review that prints `-0.33 kg` reads it as fat. The same rule
  as everywhere else in this repo: `unknown` is a legal value, a confident number from bad coverage
  is not.
- **It will not guess a protein target.** The target comes from `profile.md`, or from the
  `--protein=` flag. If neither exists, the adherence column prints `——` instead of assuming
  a number — same rule as everywhere else in this repo: `unknown` is a legal value, a guess is not.

---

## Recalculation logic

```
if weight trend is falling faster than ~0.75% of bodyweight per week  ->  reduce deficit by 100 kcal
if weight trend is flat for 2 consecutive weeks                      ->  increase deficit by 150 kcal
if protein adherence < 5 of 7 days                                   ->  do not change calories; fix protein first
if training sessions < 2 of planned 3.5                              ->  do not change anything; the problem is adherence
```

**Never adjust calories while adherence is the problem.** Changing the plan when the plan is not being executed is the most common mistake in both coaching and product design.

---

## Output format

```
Week 41 review  (5 Oct - 11 Oct)

Average deficit      512 kcal / day
Weight trend         75.2 kg   (-0.4 kg vs last week)
Protein adherence    5 of 7 days
Training             3 of 3 sessions

Assessment
- on track: -0.4 kg/week is 0.5% of bodyweight, inside the 0.3-0.7% target band

Proposed change
- none. Hold current targets for one more week.

Open question
- protein missed on Tue and Fri. Same days you had late meetings.
  Want to move the protein target earlier in the day?
```

The week number is the **ISO week** (`YYYY-WW`), and it is stated with its date range so there is
no ambiguity about which seven days were reviewed.

---

## Do not

- Do not change more than one variable per week.
- Do not react to a single day.
- Do not propose changes when adherence is low — say so directly instead.
- Do not write the review longer than the daily report multiplied by two.
