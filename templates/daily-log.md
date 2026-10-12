# log/YYYY-MM-DD.md

Copy this to `log/` with today's date. **Append only — never delete or rewrite a line.**

```markdown
# 2026-10-12

## Meals
- 08:20 | breakfast | 520 kcal | P42 C48 F16 | photo: photos/2026-10-12/0820.jpg | source: photo | edited: none
- 13:05 | lunch     | 566 kcal | P52 C61 F14 | photo: photos/2026-10-12/1305.jpg | source: photo | edited: rice 150g->120g
- 19:40 | dinner    | 764 kcal | P54 C70 F22 | photo: photos/2026-10-12/1940.jpg | source: photo | edited: added oil

## Training
- exercise: deadlift | set: 1 | reps: 12 | load_kg: 60 | rpe: 6 | source: video+voice
- exercise: deadlift | set: 2 | reps: 12 | load_kg: 60 | rpe: 7 | source: video+voice
- exercise: deadlift | set: 3 | reps: 12 | load_kg: 60 | rpe: 7 | source: video+voice
- session_burn_kcal: 275 | source: estimated

## Sleep
- hours: 7.33 | source: oura

## Body
- weight_kg: 74.8 | source: scale | time: 07:10
- waist_cm: 88.5 | source: tape | weekly

## Totals
- intake_kcal: 1850
- protein_g: 148
- expenditure_kcal: 2330
- deficit_kcal: 480

## Notes
- protein hit target for the first time this week
- dinner out; oil estimate is the weakest number today
```

---

## Field rules

| Field | Rule |
|---|---|
| `source` | **Always present.** One of `photo`, `voice`, `manual`, `wearable`, `video+voice`, `estimated` |
| `edited` | **Always present on meals.** What you changed about the AI's estimate |
| `rpe` | Optional. Do not fabricate it |
| Time format | `HH:MM`, 24-hour |
| Weight | Log at the same time daily; morning is standard |

---

## Why the format is this rigid

A parseable line means the file can be read by **any** model, and by a script if you ever want one. **That is what makes the data yours** — no vendor format to migrate away from.

**Log an unknown rather than nothing.** `source: manual | value: unknown` beats a missing meal, because the deficit number stays honest.
