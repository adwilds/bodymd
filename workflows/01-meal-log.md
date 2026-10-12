# Workflow 01 — Meal log

**Trigger:** the user sends a photo of food, or describes what they ate.

**Goal:** produce an editable estimate plus an eating order, then append it to today's log. Target: **under 15 seconds of user effort.**

---

## Inputs

| Input | Required | Notes |
|---|---|---|
| Photo (before eating) | preferred | fastest path |
| Photo (after eating) | optional | improves portion accuracy |
| Text or voice description | fallback | use when photos are impractical |
| Dish name only | minimum | e.g. "chicken rice" |

If no photo and no description, ask one question: *"What did you eat?"* Do not ask more than one.

---

## Steps

1. **Identify items.** List each distinct item on the plate.
2. **Estimate portion.** Use plate and hand as scale references if present.
3. **Compute** kcal, protein, carbs, fat per item.
4. **Ask about hidden fats** if any item is cooked, fried, or dressed:
   *"Any oil, butter, or sauce? That is usually the biggest miss."*
5. **Assign a confidence level.** See §4.3 of `SKILL.md`.
6. **Produce the eating order.**
7. **Present for editing.** One edit step per item.
8. **Append to `log/YYYY-MM-DD.md`** with the `## Meals` line format.

---

## Output format

```
Lunch — 566 kcal, P52 C61 F14

  chicken breast   200 g    330 kcal   P42
  white rice       150 g    195 kcal   C43
  broccoli         120 g     41 kcal   P3  C7

  confidence: medium  (portion of rice is the main uncertainty)

  Eat in this order:
    1. chicken breast
    2. broccoli
    3. white rice

  [edit any line]   [confirm]
```

---

## Edge cases

| Situation | Handling |
|---|---|
| Mixed dish (curry, stir-fry, stew) | Estimate as a whole; confidence **low**; ask for the dominant ingredient |
| Restaurant plate | Say explicitly that restaurant portions cannot be estimated reliably; widen the range |
| User wants no estimate | Log the item with `kcal: unknown`. A logged unknown beats an unlogged meal |
| Repeated meal | If the same meal appears in the last 14 days, offer that value first |
| Alcohol | Log it. Place last in eating order |

---

## Do not

- Do not refuse a meal because it is "unhealthy". There is no judgement in this system.
- Do not present a single precise number without a confidence level.
- Do not add items the user did not mention.
- Do not lecture about nutrition unless asked.
