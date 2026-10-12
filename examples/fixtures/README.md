# Synthetic fixtures — disclosure and red lines

**Everything in this directory is fabricated.** No real person's health, weight, sleep,
or training data is contained here. The names, avatars, scales, wearables and meals are
invented for testing.

Every persona file carries a `SYNTHETIC` marker on its first line, per the project's
synthetic-data rule. To confirm the whole set is marked:

```bash
grep -L "^# SYNTHETIC" examples/fixtures/{CN,US,UK,MX,NG,IN}-*.md    # expect: no output
```

---

## 1. Why these files exist

`docs/testing.md` defines five test layers. Layers L1 (contract) and L2 (workflow) can be
automated; L4 (cross-model) and L5 (cuisine) need *realistic* input to be meaningful.

Without realistic fixtures, every test passes for the wrong reason: an AI looks good on
tidy data and fails on the data people actually produce — a skipped lunch, a scale that is
out of batteries, a 4-hour night before a heavy session, a weekend of drinking.

So these eight personas are deliberately **broken in believable ways**.

---

## 2. What is covered

| Persona | Region | Cuisine / context | Primary test purpose |
|---|---|---|---|
| `CN-01` 李明 | Shanghai, CN | Home cooking + canteen + late-night takeout | Eating-order failure repeated; one 4h-sleep night |
| `CN-02` 王婷 | Chengdu, CN | Sichuan, high oil | Manual correction of a staple portion; weight not logged for days |
| `US-01` Michael Chen | San Francisco, US | Chinese-American takeout | Skipped meal logged as `unknown`; restaurant weekend overshoot |
| `US-02` Sarah Williams | Austin, US | Mexican-American | Alcohol in the log; hidden calories in chips/queso |
| `UK-01` James O'Brien | Manchester, UK | Pub food, ale, Sunday roast | Liquid calories counted; largest single-meal outlier |
| `MX-01` Carlos Ramírez | Mexico City, MX | Tacos, quesadillas, barbacoa | One day with severe protein miss (48 g); weekend cheat day |
| `NG-01` Adaeze Okonkwo | Lagos, NG + London, UK | West African stews, travel week | A full day with **no training section at all**; jet lag |
| `IN-01` Priya Sharma | London, UK | South Asian vegetarian | Structurally hard protein; iterates toward soya chunks |

**Layout:** each file is one persona, seven days, one `# YYYY-MM-DD` heading per day. That is
layout **B** in `scripts/parse_log.py`. The test week is the same for everyone:
**2026-09-14 (Mon) → 2026-09-20 (Sun)**, so cross-persona aggregates are comparable.

---

## 3. Red lines these files must not cross

1. **No real data.** Derived from typical intake patterns and public food-composition
   figures, not from any individual.
2. **No identity bait.** Every persona is a plain placeholder identity. No contact details,
   no photos, no location more precise than a city.
3. **No fabricated precision.** Where a person would not know a number, the file says
   `unknown` rather than inventing one. `unknown` is a legal value in the contract.
4. **No medical claims.** Nothing here diagnoses, prescribes, or asserts a health outcome.
5. **Not a benchmark.** These are *plausibility* fixtures, not targets. Do not copy these
   numbers into a `profile.md` and treat them as advice.

---

## 4. Fidelity requirements (from `docs/testing.md` §7.3)

A fixture is **disqualified** if it does not contain:

1. **Imperfect data** — missed meals, `unknown` weights, edited estimates
2. **Real irregularity** — weekend blowouts, a 4-hour night, consecutive meals out
3. **Regional food** — real local dish names, not translated-menu English
4. **Traceable edits** — the `edited:` field says what changed and why
5. **Anomalies and failures** — at least one day with no training, at least one day with a
   severe protein miss

Each persona satisfies all five. The `NOTES` block at the end of each day records which
requirement that day is exercising, so the fixture doubles as its own test assertion.

---

## 5. How to run

```bash
# Layer L1 — contract validation. Expect: 0 fatal.
python3 scripts/validate_log.py examples/fixtures/

# Layer L2 — aggregation. Expect: 8 personas × 7 days = 56 rows.
python3 scripts/parse_log.py examples/fixtures/
```

Warnings are expected and **intended** — several days deliberately omit `load_kg` or
`edited:` to prove the validator degrades to a warning instead of a fatal error.

> The contract's design constraint (`scripts/validate_log.py`, docstring): *"能降级为警告的，
> 绝不当致命错误 —— 用户的记录不完整是常态，校验器的职责是提示，不是拒绝。"*
> These fixtures exist to prove that claim.
