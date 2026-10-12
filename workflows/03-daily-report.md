# Workflow 03 — Daily report

**Trigger:** end of day, or the user says "report", "how did today go".

**Goal:** one screen that answers *did today move me forward*, plus exactly one actionable line.

---

## Steps

1. Read `log/YYYY-MM-DD.md`.
2. Read `profile.md` for targets.
3. Compute the four numbers.
4. Write one screen. Not more.
5. Save to `reports/YYYY-MM-DD.md`.
6. Deliver it in the chat, not as a file attachment.

---

## The template

```
# Daily report — YYYY-MM-DD

Deficit       480 kcal        target <=600      ok
Protein       148 / 145 g                       +3 g
Sleep         7h 20m
Training      deadlift 3x12 @60 kg              done
Next session  deadlift @65 kg

What changed
- none: first day inside all three targets

Notes
- lunch estimate edited downward (rice 150g -> 120g)
```

This is the same day as the one in `templates/daily-log.md` — so the numbers can be checked
against each other. If your model's report does not reconcile with the log it was reading, the
model is the problem, not the format.

---

## Rules

| Rule | Why |
|---|---|
| **One screen.** | If it needs scrolling on a phone, cut it |
| **Neutral language.** | No "failed", no "over budget", no broken streaks |
| **One actionable line.** | A list of ten is a list of zero |
| **No colour coding by medical threshold.** | Compliance. See §7 of `SKILL.md` |
| **Show provenance.** | Every number carries where it came from |

---

## Interpretation guide

**Deficit**
- within target -> `ok`
- below target -> `light`  (recovering, not a failure)
- above target -> `high`   (state it plainly, no alarm)

**Protein**
State the gap as a signed number. Never as a percentage bar with a red fill.

**Training**
`done` / `rest day` / `skipped`. A rest day is a legitimate state, not a miss.

---

## Weekly rollup

After 7 days, hand off to `workflows/04-weekly-review.md`.

---

## Do not

- Do not add motivational messages. This is an instrument panel, not a cheerleader.
- Do not compare the user to other users.
- Do not editorialise about food choices.
- Do not extend the report to fill space.
