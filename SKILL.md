---
name: bodymd
description: Run a personal lean-muscle system (fat loss while preserving muscle) on local Markdown files, using whatever AI model the user has. Use when the user wants to log meals, log training, get eating-order advice, track a calorie deficit and protein target, or generate a daily body report — without handing their data to a third-party app.
---

# bodymd

An operating system for lean muscle that runs on **local Markdown files**. This skill defines the workflows, the file formats, and the rules. It deliberately contains no model-specific instructions, so the same data works with any capable AI.

---

## 1. When to use this skill

Use it when the user:
- wants to log a meal and get calories, protein, and **eating order**
- wants to log a training set and get the **next session's load**
- wants today's **deficit and protein progress**
- wants a **daily report** combining sleep, intake, and expenditure
- wants a **weekly review** with recalculated targets
- explicitly says "lean muscle", "recomp", "lose fat keep muscle", or "run my bodymd"

Do **not** use it for: clinical nutrition, medical advice, eating-disorder support, or anything requiring a diagnosis. See §7.

---

## 2. The four workflows

| Workflow | File | Trigger |
|---|---|---|
| Meal log | `workflows/01-meal-log.md` | user sends a food photo or describes a meal |
| Training log | `workflows/02-training-log.md` | user reports a set or sends training video |
| Daily report | `workflows/03-daily-report.md` | end of day, or "give me my report" |
| Weekly review | `workflows/04-weekly-review.md` | 7 days elapsed, or "week review" |

---

## 3. Data contract

**This section is the point of the project.** The formats are stable. Any model that can read and write these files can take over from any other.

### 3.1 File layout

```
profile.md                     # baseline and targets (user-owned, rarely edited)
log/YYYY-MM-DD.md              # one file per day, append-only
reports/YYYY-MM-DD.md          # generated daily report
reports/week-YYYY-WW.md        # generated weekly review
photos/YYYY-MM-DD/             # meal and training photos, referenced not copied
```

### 3.2 `profile.md` schema

Copied from `templates/profile.md` and filled in once. Keys are fixed; values are yours.

```yaml
# Baseline
height_cm: 176
weight_kg: 75.0
body_fat_est_pct: unknown     # legal to leave unknown; most people never measure it
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
wearable: none                # oura | whoop | garmin | fitbit | apple-watch | none
ai_tool: any

# Meta
created: 2026-10-12
last_reviewed: 2026-10-12
```

Only `protein_target_g`, `deficit_target_kcal`, `training_days_per_week`, `program` and
`increments_kg` are read by the daily workflows. The rest exist so a model does not have to guess
— and so the user does not have to repeat themselves in every new chat window.

`profile.md` is never written by the model without explicit confirmation. It is the user's file.

> **About the example numbers.** Every number in this repository's examples belongs to **one
> notional example person**. There is no real user behind them, and they are not the author's.
> They are kept internally consistent so the arithmetic in the examples can actually be checked.
> The contract prefers your numbers, not these.

### 3.3 Daily log schema

`templates/daily-log.md` is the canonical blank. Each entry is one line. Never rewrite history;
append only.

```markdown
## Meals
- 08:20 | breakfast | 燕麦 60g + 鸡蛋 3 个 + 牛奶 250ml | 520 kcal | P42 C48 F16 | photo: photos/2026-10-12/0820.jpg | source: photo | edited: none | order_ok: yes
- 13:05 | lunch | 鸡胸 150g + 米饭 + 西兰花 | 566 kcal | P52 C61 F14 | photo: photos/2026-10-12/1305.jpg | source: photo | edited: 米饭 150g->120g | order_ok: no

## Training
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
```

The meal line is positional for the first four fields and keyword-based after that:

```
time | meal | what you ate | kcal | P/C/F | photo: | source: | edited: | order_ok:
```

### 3.4 Rules of the contract

1. **Append only — with one precisely defined exception.** Never delete a line, and never change
   a number without saying so. **A correction updates the `edited:` field of that same line**, so
   the line itself records that it was corrected and how. Never append a second copy of the same
   meal: `## Totals` would count it twice, and a doubled meal is worse than a wrong one.
2. **Always record `source`.** What counts as legal depends on the record type. The six-value set
   is the one the validator enforces, and it applies to **meal** lines:

   | Record | Legal `source` values |
   |---|---|
   | Meals | `photo` · `voice` · `manual` · `wearable` · `video+voice` · `estimated` |
   | Training | `video+voice` · `voice` · `manual` · `estimated` |
   | Body | `scale` · `tape` · `manual` · `none` |
   | Sleep | the device or method, verbatim: `oura`, `whoop`, `garmin`, `fitbit`, `band`, `watch`, `phone`, `self-report` |
   | Supplements | `manual` · `product-label` |

   `source` is always its own `|`-separated field. Putting confidence inside it
   (`source: photo · conf: medium`) fails validation — confidence goes in its own field.

   The Sleep list is deliberately open rather than fixed: the point of the field is to record
   *which* device produced the number, and a hard-coded list of wearables goes stale every year.
   `Body` uses `none` when you could not measure.
3. **Always record `edited`** when the user changes an AI estimate. This is the accuracy feedback loop.
4. **Machine-readable first.** Keep the bullet syntax identical so a script can parse it.
5. **No proprietary format.** Markdown only. No databases, no exports needed.
6. **Rest days: omit the `## Training` section entirely.** A placeholder line inside it
   (`- rest day`) is parsed as a training set and fails validation. Note the rest day in
   `## Notes` instead: `- Rest day, no training section.`
7. **Optional fields stay optional.** Three extensions are in use today — `order_ok` on meal
   lines, `## Supplements`, and `## Body`. A model that ignores them still produces a valid file;
   a model that writes them produces a more useful one. Adding a field never requires a migration,
   which is the whole reason the format is line-based rather than column-based.

---

## 4. Meal analysis rules

### 4.1 Output contract

For every meal, return exactly:

```
items:       [name, estimated portion, kcal, protein]
total:       kcal | protein | carbs | fat
confidence:  high | medium | low
eating_order: [ordered list]
```

### 4.2 Eating order logic

Order by this priority unless the user says otherwise:

1. **Protein first** — meat, eggs, fish, dairy, legumes
2. **Fiber and vegetables second**
3. **Starch and carbohydrate last**
4. **Liquid calories and dessert last of all**

Rationale to give the user only if asked: protein first improves satiety and blunts the post-meal glucose curve.

**Close the loop.** Advice that is never checked cannot be improved. When the meal is over, ask one
question — *"did you eat it in that order?"* — and record the answer as `order_ok: yes` or
`order_ok: no` on the meal line. It is one word, it is optional, and it is the only way anyone
ever finds out whether the ordering rule does anything. See §3.3.

### 4.3 Accuracy honesty

- State a confidence level on every estimate.
- Portion size is the dominant error source, not food identification. Say so when confidence is low.
- Hidden fats (cooking oil, sauces, dressings) are the second source. **Always ask about them if a dish is cooked.**
- Never claim precision. These are estimates.

### 4.4 The 80/20 rule

Do 80% of the work; let the user fix the last 20%. **Every estimate must be editable, and editing must be one step.** Never present a number the user cannot correct.

See `prompts/meal-analysis.md`.

---

## 5. Training rules

### 5.1 What can be detected from video

| Readable from video | Not readable from video |
|---|---|
| exercise type | **load / weight** |
| rep count | RPE with confidence |
| set count | |
| tempo and range of motion | |

**Never guess load from video.** Ask for it by voice or text. See `docs/faq.md`.

### 5.2 Progressive overload rule

Default progression, adjust only with explicit user instruction:

- Last session **completed all prescribed reps at the prescribed RPE** -> increase load by the smallest available increment (typically **+2.5 kg** upper body, **+5 kg** lower body).
- Reps completed but RPE above target -> **repeat the same load**.
- Reps missed -> **reduce by one increment** and hold.
- Two consecutive sessions above target RPE -> insert a lighter session.

### 5.3 Session burn

Report estimated session burn as a single number labelled `estimated`. Never present it as measured.

---

## 6. Report format

The daily report is one screen. Structure:

```
# Daily report — YYYY-MM-DD

Deficit       480 kcal        target <=600      [ok]
Protein       148 / 145 g                       [+3 g]
Sleep         7h 20m
Training      deadlift 3x12 @60kg               done
Next session  deadlift @65kg

## What changed
- none: first day inside all three targets

## Notes
- lunch estimate edited downward (rice 150g -> 120g)
```

Rules:
- **One screen.** If it does not fit on a phone screen, it is too long.
- **No alarming language.** No "you failed", no "over budget", no streaks broken.
- **One actionable line** under "What changed". Not a list of ten.
- Use neutral labels. Do not colour-code by medical thresholds. See §7.

When there *is* something to change, it is still exactly one line:

```markdown
## What changed
- protein below target: add 25 g at dinner
```

---

## 7. Guardrails

**This is not a medical product.** The following are hard rules for anything generated by this skill.

Never:
- claim to diagnose, treat, cure, or prevent any disease
- present any number as a clinical measurement; always label estimates as estimates
- use red / amber / green colour coding that implies a clinical threshold
- use the phrase "medical-grade" or anything similar
- advise on medication, dosing, or supplements beyond protein and creatine at standard doses
- continue serving a user who shows signs of disordered eating; refer them to a professional

If a user asks for any of the above, decline and point to a qualified professional.

---

## 8. Model-agnostic notes

| Step | Requirement | If the model is weak |
|---|---|---|
| Meal photo analysis | vision + reasonable food knowledge | ask the user to describe the meal in words |
| Eating order | simple rule application, no model needed | apply §4.2 deterministically |
| Training load advice | arithmetic against the log | apply §5.2 deterministically |
| Daily report | templating | fill the template in `templates/report.md` |

**Design intent:** anything that can be deterministic, should be. Reserve the model for the parts that genuinely need judgement — mainly photo interpretation and confidence assessment.

## 9. If the user wants an app

Decline politely. Point at §3.1: the whole design is that their data is a folder they own. An app would put it back in someone else's database.
