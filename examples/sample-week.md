# Example — one real week (anonymized)

A 36-year-old male, 172 cm, 74.6 kg at the start. Three training days, four rest days.
Published with permission. Numbers are as logged, including the mistakes.

---

## Monday

```
# Daily report — Day 1

Deficit       480 kcal        target <=600      ok
Protein       148 / 145 g                       +3 g
Sleep         7h 20m
Training      deadlift 3x12 @60 kg              done
Next session  deadlift @62.5 kg

What changed
- none: first day inside all three targets

Notes
- lunch estimate edited downward (rice 150g -> 120g)
- dinner out; oil estimate is the weakest number today
```

**What actually happened:** first day using the system. The AI put white rice first in the eating order. Corrected manually — protein first. That correction is the reason the workflow now has an explicit ordering rule instead of a note.

---

## Tuesday

```
Deficit       310 kcal        target <=600      light
Protein        96 / 145 g                       -49 g
Sleep         6h 05m
Training      rest day                          rest
Next session  squat @40 kg

What changed
- protein 49 g short: the gap is a late meeting, not a food choice

Notes
- skipped the pre-bed protein because of a 21:00 call
```

**What actually happened:** low day. The system did not flag it as a failure, which is the point — a red "you failed" screen on day 2 is where most people quit. The weekly review picked up the pattern instead (see below).

---

## Wednesday

```
Deficit       540 kcal        target <=600      ok
Protein       152 / 145 g                       +7 g
Sleep         7h 45m
Training      squat 3x12 @40 kg (video)         done
Next session  squat @45 kg

What changed
- none

Notes
- video gave exercise + reps; weight entered by voice
- burned 310 kcal estimated
```

**What actually happened:** the video analysis correctly identified squat and counted 12 reps in all three sets. It could not see the weight. Two seconds to say "forty kilos" — that is the entire cost of the platform limitation.

---

## Thursday

```
Deficit       455 kcal        target <=600      ok
Protein       139 / 145 g                       -6 g
Sleep         7h 10m
Training      rest day                          rest
Next session  bench @30 kg

What changed
- protein 6 g short: within noise

Notes
- none
```

---

## Friday

```
Deficit       680 kcal        target <=600      high
Protein       121 / 145 g                       -24 g
Sleep         7h 00m
Training      bench 3x10 @30 kg                 done
Next session  bench @30 kg

What changed
- deficit above target: Friday dinner is the pattern, not the exception

Notes
- restaurant meal; confidence low on the whole entry
- bench reps missed (10 of 12); holding load next session
```

**What actually happened:** the progression rule fired correctly. Two reps missed -> repeat the load instead of adding weight. A simpler system would have added 2.5 kg and produced a bad session the following week.

---

## The weekly review

```
Week 41 review  (Day 1 - Day 7)

Average deficit      472 kcal / day
Weight trend         74.3 kg   (-0.3 kg)
Protein adherence    5 of 7 days
Training             3 of 3 sessions

Assessment
- on track: -0.3 kg/week is inside the 0.3-0.7 target band

Proposed change
- none. Hold current targets for one more week.

Open question
- protein missed on Tue and Fri. Both were days with evening meetings.
  Want to shift the protein target earlier in the day?
```

---

## What this week actually taught

| Finding | What changed in the repository |
|---|---|
| The eating order was wrong on day 1 | `SKILL.md` §4.2 became a deterministic rule instead of a suggestion |
| Video could not produce the weight | `SKILL.md` §5.1 and `docs/faq.md` now state the limitation explicitly |
| A "failure" label was demotivating on day 2 | The daily report uses three neutral states instead of pass/fail |
| Restaurant meals are the weakest estimate | `workflows/01-meal-log.md` now requires confidence labelling and a widened range |

**This is how the project was built: three people, fourteen days, manually, before a single line of code.**
