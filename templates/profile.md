# profile.md

Copy this file to the repository root and edit it. Your AI reads it at the start of every session.

```yaml
# Baseline
height_cm: 172
weight_kg: 75.0
body_fat_est_pct: 29
age: 36
sex: male

# Targets
protein_target_g: 145
deficit_target_kcal: 600
weekly_weight_change_target_pct: 0.5

# Training
training_days_per_week: 3.5
program:
  - deadlift
  - squat
  - bench press
increments_kg:
  upper: 2.5
  lower: 5.0

# Data sources
wearable: oura
ai_tool: claude-code

# Meta
created: 2026-10-12
last_reviewed: 2026-10-12
```

---

## How to set your numbers

**protein_target_g** — a common starting point is **1.8-2.2 g per kg of bodyweight** for someone training while in a deficit. Adjust with a professional if you have kidney or liver conditions.

**deficit_target_kcal** — a starting point is **400-600 kcal**, aiming for **0.3-0.7% of bodyweight per week**. Faster than that tends to cost muscle.

**increments_kg** — the smallest realistic step your gym allows. 2.5 kg per side plates is typical for upper body, 5 kg for lower.

⚠️ These are starting points, not prescriptions. This file is a record of *your* decisions.

---

## Notes

- **This file is yours.** The AI may propose changes in the weekly review, but it must not write to this file without your confirmation.
- Keep the keys exactly as written. They are the data contract.
- Add keys if you need them. Removing keys may break older workflows.
