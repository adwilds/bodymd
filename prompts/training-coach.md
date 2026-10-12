# Prompt — training coach

Copy this into any AI tool. Replace the bracketed parts.

---

```
You are keeping a training log for someone running a lean-muscle protocol.

Here is my history for the relevant exercise:

[paste the last 4-6 training entries from log/*.md]

Today's session:
- exercise: [name]
- reps completed: [n] of [target]
- load: [kg]
- RPE: [n] (or "not tracked")

Apply these rules and give me the next session's load:

1. All prescribed reps hit, RPE at or below target -> +2.5 kg upper body,
   +5 kg lower body
2. Reps hit but RPE above target -> repeat the same load
3. Reps missed -> reduce by one increment and hold
4. Two consecutive sessions above target RPE -> insert a lighter session

Output exactly:
  next_load: <kg>
  reason: <one line, citing which rule applied>
  session_burn_estimate: <kcal, labelled estimated>

Rules:
- Do not prescribe a load increase if there are fewer than two previous
  sessions logged for this exercise.
- Do not comment on my form. You cannot see it.
- Do not add motivational language.
- One line of reason. Not a paragraph.
```

---

## Why the prompt is shaped this way

| Line | Purpose |
|---|---|
| "Here is my history" | the progression rule is arithmetic on the log, not a judgement call |
| The four rules inline | makes the output deterministic across models — this is the **data contract** idea applied to behaviour |
| `next_load / reason / session_burn_estimate` | fixed output keys, so any model produces parseable output |
| "Do not prescribe... fewer than two previous sessions" | prevents the most common bad output: confident nonsense on thin data |
| "Do not comment on my form" | a real failure mode; the model cannot see the video's depth or tempo from a description |

---

## Note on video

If you send a training video, expect the model to give you **exercise and rep count only**.

**Load cannot be read from a video.** Say it, or type it.
