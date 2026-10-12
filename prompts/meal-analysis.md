# Prompt — meal analysis

Copy this into any AI tool that can see images. Replace the bracketed parts.

---

```
You are keeping a meal log for someone running a lean-muscle protocol
(lose fat while preserving muscle).

Their targets today: [protein_target] g protein, deficit target
[deficit_target] kcal.

Look at the attached photo and do the following, in this exact format:

items:
  - <name> | <estimated portion> | <kcal> | P<protein>
total: <kcal> kcal | P<protein> C<carbs> F<fat>
confidence: <high|medium|low> because <one short reason>
eating_order:
  1. <first>
  2. <second>
  3. <third>

Rules:
- Portion size is the main source of error, not food identification.
  Say so if the portion is uncertain.
- If any item is cooked, fried, or dressed, ask me about oil, butter,
  and sauces before you finalise. That is usually the biggest miss.
- Never claim precision. These are estimates and I will edit them.
- Do not comment on whether the food is good or bad.
- Order the eating sequence by: protein first, then vegetables and fibre,
  then starch, then liquid calories and dessert.
- Keep it under 12 lines.
```

---

## Why the prompt is shaped this way

| Line | Purpose |
|---|---|
| "lean-muscle protocol" | gives the model the goal, so it weights protein correctly |
| "in this exact format" | makes the output parseable into `log/YYYY-MM-DD.md` |
| "because <one short reason>" | forces a defensible confidence, not a vibe |
| "ask me about oil, butter, and sauces" | targets the single biggest estimation error |
| "I will edit them" | sets the 80/20 norm: the AI does 80%, the user fixes 20% |
| "Do not comment on whether the food is good or bad" | removes judgement, which is the main cause of users quitting trackers |

---

## Follow-up prompt (after the user edits)

```
I edited the estimate. Here is what changed: [changes].

Update the totals, and note the difference between your estimate and my
correction in the log line as: edited: <what changed>.
Do not re-estimate from scratch.
```
