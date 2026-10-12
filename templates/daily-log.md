# log/YYYY-MM-DD.md

Copy this to `log/` with today's date. **Append only — never delete or rewrite a line.**

```markdown
# 2026-10-12

## Meals
- 08:20 | breakfast | 燕麦 60g + 鸡蛋 3 个 + 牛奶 250ml | 520 kcal | P42 C48 F16 | photo: photos/2026-10-12/0820.jpg | source: photo | edited: none | order_ok: yes
- 13:05 | lunch | 鸡胸 150g + 米饭 + 西兰花 | 566 kcal | P52 C61 F14 | photo: photos/2026-10-12/1305.jpg | source: photo | edited: 米饭 150g->120g | order_ok: no
- 19:40 | dinner | 外食：辣椒炒肉 + 米饭 | 764 kcal | P54 C70 F22 | photo: photos/2026-10-12/1940.jpg | source: photo | edited: 加了 1 勺油 | order_ok: no

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

## Supplements
- item: creatine | dose_g: 5 | source: manual

## Totals
- intake_kcal: 1850
- protein_g: 148
- expenditure_kcal: 2330
- deficit_kcal: 480

## Notes
- lunch estimate edited down: AI read the rice as 150 g, it was nearer 120 g
- dinner out; the oil estimate is the weakest number today
```

---

## Field rules

| Field | Rule |
|---|---|
| `source` | **Always present.** Legal values depend on the record type — see the table below |
| `edited` | **Always present on meals.** What you changed about the AI's estimate. `none` if you changed nothing |
| `order_ok` | Optional. `yes` / `no` — did you actually eat in the suggested order? |
| `rpe` | Optional. Do not fabricate it |
| Time format | `HH:MM`, 24-hour |
| Weight | Log at the same time daily; morning is standard |

**Legal `source` values by record type** (`SKILL.md` §3.4):

| Record | Values |
|---|---|
| `## Meals` | `photo` · `voice` · `manual` · `wearable` · `video+voice` · `estimated` |
| `## Training` | `video+voice` · `voice` · `manual` · `estimated` |
| `## Body` | `scale` · `tape` · `manual` · `none` |
| `## Sleep` | the device or method, verbatim — `oura`, `whoop`, `garmin`, `fitbit`, `band`, `watch`, `phone`, `self-report` |
| `## Supplements` | `manual` · `product-label` |

---

## Optional sections

Three parts of this file are optional. Omit them and everything still works.

| Section / field | When to add it | What it buys you |
|---|---|---|
| `order_ok:` on a meal line | after you eat | tells you whether the eating-order advice is followed, and therefore whether it works |
| `## Body` | when you weigh in | the 7-day weight trend, which is the ground truth the weekly review runs on |
| `## Supplements` | if you take protein or creatine | keeps the protein total honest when it comes from powder rather than food |

## Rest days

**Omit the entire `## Training` section.** A placeholder line inside it (`- rest day`) is parsed as
a training set and fails validation. Note the rest day under `## Notes` instead:

```markdown
## Notes
- Rest day, no training section.
```

---

## Why the format is this rigid

A parseable line means the file can be read by **any** model, and by a script if you ever want one. **That is what makes the data yours** — no vendor format to migrate away from.

**Log an unknown rather than nothing.** `source: manual | value: unknown` beats a missing meal, because the deficit number stays honest.
