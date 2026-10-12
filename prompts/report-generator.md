# Prompt — report generator

Copy this into any AI tool. Replace the bracketed parts.

---

```
Read my log for today: [paste the contents of log/YYYY-MM-DD.md]
My profile targets: [paste profile.md]

Write my daily report in exactly this format:

# Daily report — YYYY-MM-DD

Deficit       <n> kcal        target <=<target>      <ok|light|high>
Protein       <n> / <target> g                        <+/-n> g
Sleep         <h m>
Training      <description or "rest day">             <done|rest|skipped>
Next session  <exercise> @<load>

What changed
- <exactly one actionable line>

Notes
- <only items worth keeping: edits made, anomalies, reasons>

Rules:
- One screen. If it would need scrolling on a phone, cut it.
- No judgement words. No "failed", "over budget", "cheating", "bad day".
- Do not colour-code by medical threshold. Use the plain labels above.
- "What changed" gets exactly one line. A list of ten is a list of zero.
- A rest day is a legitimate state, not a miss.
- State the protein gap as a signed number, never as a red percentage bar.
- Do not add encouragement. This is an instrument panel, not a cheerleader.
```

---

## Why the prompt is shaped this way

| Line | Purpose |
|---|---|
| "exactly this format" | the report is generated daily; a fixed format is readable at a glance |
| `ok|light|high` | three neutral labels replace the usual red/amber/green medical coding |
| "exactly one line" for What changed | forces prioritisation — the hardest and most valuable part |
| "A rest day is a legitimate state" | removes the failure framing that makes people abandon trackers |
| "instrument panel, not a cheerleader" | keeps the tone flat and trustworthy |

---

## Weekly variant

Swap the source to the last 7 reports and use the recalculating rules in
`workflows/04-weekly-review.md`.
