# Workflow 02 — Training log

**Trigger:** the user reports a set, sends a training video, or says "training done".

**Goal:** record the set accurately, then prescribe the next session's load. This is the **progressive overload engine**.

---

## Inputs

| Input | Gives you | Does not give you |
|---|---|---|
| Video | exercise, reps, sets, tempo | **load** |
| Voice note | everything, if the user says it | — |
| Manual text | everything | — |

**See §5.1 of `SKILL.md`: never infer load from video.** Ask for it.

---

## Steps

1. **Get the exercise and set data.** From video: identify the movement and count reps. From text: parse.
2. **Ask for load**, exactly once: *"What weight? (or say 'bodyweight')"*
3. **Ask for RPE** only if the user tracks it. Do not force it.
4. **Apply the progression rule** (§5.2 of `SKILL.md`).
5. **Append to `log/YYYY-MM-DD.md`** under `## Training`.
6. **Report the next session's load** in one line.

---

## The progression rule

```
all prescribed reps hit, RPE at or below target   ->  +1 increment
reps hit, RPE above target                        ->  repeat load
reps missed                                       ->  -1 increment, hold
2 sessions above target RPE                       ->  insert a lighter session
```

Default increments: **+2.5 kg** upper body, **+5 kg** lower body. Override only if the user specifies.

---

## Output format

```
Deadlift — set 3 of 3

  reps      12
  load      60 kg      (voice)
  rpe       7
  source    video

  Next session:  62.5 kg      (+2.5)
  Reason:        all reps hit at RPE 7, below target 8

  Session burn: 275 kcal  (estimated)
```

---

## Edge cases

| Situation | Handling |
|---|---|
| User does not know the load and cannot check | Log `load: unknown`, skip progression for that exercise |
| Bodyweight movement | Log `load: bodyweight`; progress by reps, not load |
| New exercise, no history | Start with a rep target and RPE target; no load prescription yet |
| User is sore or unwell | Never push progression. Ask, then log the reason |
| Cardio only | Log duration and estimated burn; no progression rule applies |

---

## Do not

- Do not prescribe load increases for an exercise with fewer than two logged sessions.
- Do not use video to claim load or depth or joint safety.
- Do not turn this into a coaching conversation unless asked.
- Do not present session burn as measured. It is an estimate.
