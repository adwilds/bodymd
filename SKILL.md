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

### 3.3 Daily log schema

Each entry is one line. Never rewrite history; append only.

```markdown
## Meals
- 08:20 | breakfast | 520 kcal | P42 C48 F16 | photo: photos/2026-10-12/0820.jpg | edited: none
- 13:05 | lunch     | 566 kcal | P52 C61 F14 | photo: photos/2026-10-12/1305.jpg | edited: rice 150g->120g

## Training
- exercise: deadlift | set: 3 | reps: 12 | load_kg: 60 | rpe: 7 | source: video
- session_burn_kcal: 275

## Sleep
- hours: 7.33 | source: oura

## Totals
- intake_kcal: 1850
- protein_g: 128
- expenditure_kcal: 2330
- deficit_kcal: 480
```

### 3.4 Rules of the contract

1. **Append only.** Never delete or silently rewrite a prior entry.
2. **Always record `source`** on numbers: `photo` | `voice` | `manual` | `wearable`.
3. **Always record `edited`** when the user changes an AI estimate. This is the accuracy feedback loop.
4. **Machine-readable first.** Keep the bullet syntax identical so a script can parse it.
5. **No proprietary format.** Markdown only. No databases, no exports needed.

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
Protein       128 / 145 g                       [-17 g]
Sleep         7h 20m
Training      deadlift 3x12 @60kg               done
Next session  deadlift @62.5kg

## What changed
- protein below target: add 25 g at dinner

## Notes
- lunch estimate edited downward (rice 150g -> 120g)
```

Rules:
- **One screen.** If it does not fit on a phone screen, it is too long.
- **No alarming language.** No "you failed", no "over budget", no streaks broken.
- **One actionable line** under "What changed". Not a list of ten.
- Use neutral labels. Do not colour-code by medical thresholds. See §7.

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
