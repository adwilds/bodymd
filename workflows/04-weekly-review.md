# Workflow 04 — Weekly review

**Trigger:** 7 days elapsed since the last review, or the user asks for a week review.

**Goal:** recalculate targets from what actually happened, not from what was planned.

This is the step that separates bodymd from a calorie diary. **The diary records. The review recalculates.**

---

## Steps

1. Read the last 7 daily reports.
2. Compute the three weekly aggregates.
3. Compare against `profile.md`.
4. Propose target changes, with the arithmetic shown.
5. Write the changes back to `profile.md` **only after the user confirms**.
6. Save the review to `reports/week-YYYY-WW.md`.

---

## The three aggregates

| Aggregate | Formula | What it tells you |
|---|---|---|
| **Average deficit** | mean of daily deficit | whether the plan matches reality |
| **Weight trend** | 7-day mean vs previous 7-day mean | the ground truth |
| **Protein adherence** | days hitting >=90% of target, out of 7 | whether the intake side is actually being executed |

**Use the 7-day mean, never a single day's weight.** Daily fluctuation is mostly water.

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
Week 41 review  (12 Oct - 18 Oct)

Average deficit      512 kcal / day
Weight trend         74.6 kg   (-0.4 kg vs last week)
Protein adherence    5 of 7 days
Training             3 of 3 sessions

Assessment
- on track: -0.4 kg/week is inside the 0.3-0.6 target band

Proposed change
- none. Hold current targets for one more week.

Open question
- protein missed on Tue and Fri. Same days you had late meetings.
  Want to move the protein target earlier in the day?
```

---

## Do not

- Do not change more than one variable per week.
- Do not react to a single day.
- Do not propose changes when adherence is low — say so directly instead.
- Do not write the review longer than the daily report multiplied by two.
