# personas.md — the eight fabricated users

Test week: **2026-09-14 (Mon) → 2026-09-20 (Sun)**. Same window for all eight, so weekly
aggregates are directly comparable.

These are the baselines the fixtures were written against. Read them before reading the logs
— several "mistakes" in the logs are intentional consequences of the baseline, not typos.

---

## Baseline table

| ID | Name | Age / sex | City | Height | Weight (start → end) | Protein target | Training program | Wearable | Logging habit |
|---|---|---|---|---|---|---|---|---|---|
| `CN-01` | 李明 Li Ming | 32 / M | Shanghai | 178 cm | 82.4 → 81.6 kg | 150 g | Squat / deadlift / bench, 4–5×/wk | Mi Band | Photo + voice, logs everything |
| `CN-02` | 王婷 Wang Ting | 29 / F | Chengdu | 163 cm | 64.8 → 64.4 kg | 105 g | Glute bridge / squat, 3×/wk | none | Photo, forgets the scale |
| `US-01` | Michael Chen | 38 / M | San Francisco | 175 cm | 86.0 → 86.2 kg | 165 g | 5×5, 3–4×/wk | WHOOP | Photo, logs takeout as-is |
| `US-02` | Sarah Williams | 34 / F | Austin, TX | 168 cm | 74.2 → 74.2 kg | 130 g | Upper/lower, 4×/wk | Apple Watch | Photo + manual, drinks on Fridays |
| `UK-01` | James O'Brien | 41 / M | Manchester | 180 cm | 93.5 → 94.3 kg | 160 g | Squat / bench / deadlift, 3×/wk | Garmin | Manual, estimates loosely |
| `MX-01` | Carlos Ramírez | 27 / M | Mexico City | 172 cm | 78.0 → 78.3 kg | 145 g | Powerbuilding, 4×/wk | none | Voice, fast and imprecise |
| `NG-01` | Adaeze Okonkwo | 31 / F | Lagos + London | 165 cm | 70.5 → 70.5 kg | 120 g | Squat / RDL, 3×/wk | Fitbit | Manual, skips days when travelling |
| `IN-01` | Priya Sharma | 30 / F | London | 158 cm | 61.3 → 61.2 kg | 100 g | Squat / RDL, 3×/wk | none | Voice, describes meals aloud |

---

## 1. CN-01 · 李明 Li Ming

**Context.** Product manager in Shanghai. Eats breakfast at a street stall, lunch in the
company canteen, dinner as takeout when the release cycle is busy. Trains four to five
times a week at a commercial gym upstairs from the office.

**Why he exists.** He is the "does everything right except the one thing that matters" case.
He logs every meal, hits his training days, and still stalls — because he eats a large
late-night snack after the gym, and his protein sits around 90 g against a 150 g target.

**Injected failures.** Two surge days above 2,400 kcal; one 4.2-hour night (release night)
with training reduced from 4 sets to 3; one day where the protein line reads 74 g. One day
has no `## Totals — intake_kcal`, forcing the aggregator down its `computed` path.

**What a correct report must say.** His problem is not calories and not effort. It is
protein distribution and the post-training snack. A report that tells him to eat less has
failed the test.

---

## 2. CN-02 · 王婷 Wang Ting

**Context.** Designer in Chengdu. Home cooking dominates, and Sichuan cooking means a lot of
rapeseed oil that a photo cannot measure. She trains at a small studio three times a week.
Her bathroom scale has been out of batteries twice this week.

**Why she exists.** The hard case for **estimation under fat**: the AI can see the food but
cannot see the oil. She also does something almost no fixture does — she *overrides* the
model and says so in `edited:`.

**Injected failures.** `edited: 米饭 150g->120g` on one meal (a human correction of an
AI overestimate); three days with no weight logged (`unknown`); one day at 1,630 kcal with
64 g protein; an explicit note that oil is the weakest number of the day.

**What a correct report must say.** Oil is the dominant unknown in her log, and the correct
response is to reduce the variance (cook with a measured spoon for a week) rather than to
guess a bigger number. A report that silently picks a value has failed the test.

---

## 3. US-01 · Michael Chen

**Context.** Engineer in San Francisco, Chinese-American, orders takeout most weekdays.
Trains 5×5 three to four times a week. Wears a WHOOP.

**Why he exists.** He is the honest-incomplete logger: on a day of back-to-back meetings he
did not eat lunch and recorded it as `unknown` instead of deleting the meal. That single
choice keeps his deficit honest for the week.

**Injected failures.** One skipped lunch logged as `unknown kcal`; one 5.5-hour sleep night;
a Saturday that reaches 3,510 kcal across a pancake breakfast, dim sum and a steakhouse
dinner with two beers.

**What a correct report must say.** His weekly average deficit survives only because the
skipped meal is recorded. The report should praise the `unknown`, not treat it as a defect.

---

## 4. US-02 · Sarah Williams

**Context.** Marketing manager in Austin, Mexican-American household. Corn tortillas, black
beans, chips and queso are staples — a lot of it is genuinely healthy and a specific part of
it is not. Trains four times a week and is the most consistent lifter in the set.

**Why she exists.** She is the **liquid-calorie and hidden-chip** case: two margaritas and a
bowl of queso add roughly 900 kcal to a day that photographs as a normal taco day.

**Injected failures.** 1,240 kcal dinner including two margaritas; a chips-and-queso snack;
one day with no `intake_kcal` in Totals (aggregator computes it); Friday at −390 kcal deficit.

**What a correct report must say.** The confounder is alcohol and restaurant chips, not
tortillas. A report that tells her to cut carbs has misread the data.

---

## 5. UK-01 · James O'Brien

**Context.** 41, Manchester, works in logistics. Pub culture is part of the job. Wears a
Garmin, logs by hand and estimates generously in both directions.

**Why he exists.** The **liquid-calorie outlier**: Wednesday's three pints of bitter push a
normal day to 2,540 kcal, and Sunday's roast lamb is the single largest meal in the whole
fixture set at 1,420 kcal.

**Injected failures.** A 1,680 kcal pub dinner including three pints; a full English on
Saturday; Sunday with no `intake_kcal`; every day above target except one; a 5.8-hour night.

**What a correct report must say.** His weight is rising while his food log "looks fine"
because roughly a third of his weekly surplus is drunk. The lever is pints, not plates.

---

## 6. MX-01 · Carlos Ramírez

**Context.** 27, Mexico City, works in a family business. Eats comida corrida at lunch,
tacos in the evening, and lives for the weekend barbecue. Logs by voice while walking.

**Why he exists.** The **severe protein miss** case: on Thursday he eats pan dulce, rice with
vegetables, mango, and cheese enchiladas — 48 g of protein for a 78 kg man.

**Injected failures.** A 48 g protein day; a Saturday cheat day at 3,280 kcal (−780 kcal
deficit); no wearable, so sleep is self-reported; three days without `load_kg` on some sets.

**What a correct report must say.** Thursday is a *composition* failure, not a calorie
failure — 1,940 kcal and almost no protein. The fix is one protein anchor per meal, not a
reduction.

---

## 7. NG-01 · Adaeze Okonkwo

**Context.** 31, Lagos, consultancy work that takes her to London for part of the week.
Eats egusi, efo riro, ogbono, jollof and pounded yam. Trains at a gym near home and in hotel
gyms when travelling.

**Why she exists.** She is the **missing-day** case: Friday is a flight-plus-client-meetings
day and contains **no `## Training` section at all**. The correct handling is to leave it
empty and say so in NOTES — not to backfill an estimated session.

**Injected failures.** A day with no training section; a 5.0-hour red-eye night; a 1,700 kcal
day; two days where the cultural dish makes the starch estimate the weakest number.

**What a correct report must say.** The empty training day is data, not a gap. Backfilling it
would corrupt the adherence denominator used by the weekly review.

---

## 8. IN-01 · Priya Sharma

**Context.** 30, London, South Asian vegetarian. Ghee, paneer, dal, roti, and — importantly
— a protein ceiling that is structural rather than motivational: a traditional vegetarian
plate simply does not carry 100 g of protein without deliberate design.

**Why she exists.** The **iterating-user** case. She is the only persona whose log *changes
itself* over the week: on Wednesday she adds Greek yogurt specifically to move the protein
number, and by Sunday she introduces soya chunks. Her log is the test for whether the
system recognises a user solving their own problem.

**Injected failures.** Two days at 56 g protein; a kheer dessert on Friday; one day with no
`intake_kcal`; `load_kg` omitted on two sets.

**What a correct report must say.** She has already diagnosed and started fixing her own
bottleneck. The report should reinforce the soya-chunk move and quantify it, not restart the
analysis from zero. A report that says "eat more protein" without noticing she did has failed.

---

## Aggregates to check after running `parse_log.py`

Measured output of `scripts/parse_log.py examples/fixtures/` — **56 days / 8 personas**.
These are the real numbers, not estimates. If your run disagrees, the parser or a fixture changed.

| ID | Days | Avg deficit | Training days | Notable |
|---|---|---|---|---|
| `CN-01` | 7 | 449 kcal | 5 | Protein 74–129 g vs a 150 g target; 1 day on the `computed` path |
| `CN-02` | 7 | 234 kcal | 3 | 3 days weight `unknown`; 1 manual correction; 1 `computed` day |
| `US-01` | 7 | 687 kcal | 4 | 1 meal logged as `unknown`; Saturday +3,510 kcal (−610) |
| `US-02` | 7 | 442 kcal (6 days) | 4 | Alcohol + chips; Friday −390; Saturday has no Totals → `——` |
| `UK-01` | 7 | 623 kcal | 3 | Weight rising 93.5 → 94.3 kg; Sunday roast 1,420 kcal |
| `MX-01` | 7 | 373 kcal | 4 | Thursday 48 g protein; Saturday −780; 2 validator warnings |
| `NG-01` | 7 | 419 kcal | 3 | **One day with no Training section at all** |
| `IN-01` | 7 | 294 kcal | 3 | Protein rises 56 → 80 g across the week on her own initiative |

**Note on `US-02`:** its average is over 6 days, not 7. Saturday has no `## Totals` section at
all, so `expenditure_kcal` is `None` and the deficit is genuinely unknown. The parser prints
`——` and excludes it. Treating an unrecorded day as a zero-deficit day would silently bias
every weekly average upward — this fixture exists to catch that.

**Note on `MX-01`:** it is the only file that triggers `WARN` (2 items), by design, to prove
the validator degrades instead of rejecting. Everything else is clean.

