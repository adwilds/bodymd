# personas.md — the ten fabricated users

Test week: **2026-09-14 (Mon) → 2026-09-20 (Sun)** for nine of the ten, so weekly aggregates are
directly comparable. Five of them deviate deliberately. **`CN-01` additionally carries
`2026-09-07 .. 2026-09-13`** — a second, earlier week, because the weekly review recalculates from
*this week vs last week* and a single-week fixture can never exercise that path (see the two-week
table below). **`DE-01` carries only 5 of the 7 days** (`09-14 .. 09-18`) — the partial week, and
the only fixture in which the adherence denominator can disagree with 7. **`CN-02` additionally
carries `2026-09-21 .. 2026-09-27`** — a second, later week with five consecutive missing weigh-ins,
the only fixture in which the weight mean cannot be computed at all. **`US-02` additionally carries
`2026-09-21 .. 2026-09-27`** — a second, later week whose 7-day mean equals the first week's
(74.20 kg), the only fixture in which the "flat for 2 consecutive weeks" rule is reachable.
**`UK-01` additionally carries `2026-09-21 .. 2026-09-27`** — a second, later week whose mean is
0.90 kg *higher* (93.87 → 94.77 kg), the only fixture in which the weight trend is **positive**
and therefore the only place where a sign-blind `abs(trend)` implementation can be caught.

**`BR-01` is the one persona that cannot share the September test week.** It exists to bracket an
**ISO year boundary**, and there is exactly one of those per year: `2026-12-28 .. 2027-01-03`
(ISO `2026-W53`, seven days spanning two calendar years) plus `2027-01-04 .. 2027-01-10`
(ISO `2027-W01`). Its numbers are not comparable to the September weeks and do not need to be —
the question it answers is *which week a day belongs to*, not how much anyone ate.

These are the baselines the fixtures were written against. Read them before reading the logs
— several "mistakes" in the logs are intentional consequences of the baseline, not typos.

---

## Baseline table

| ID | Name | Age / sex | City | Height | Weight (start → end) | Protein target | Training program | Wearable | Logging habit |
|---|---|---|---|---|---|---|---|---|---|
| `CN-01` | 李明 Li Ming | 32 / M | Shanghai | 178 cm | 82.4 → 81.6 kg | 150 g | Squat / deadlift / bench, 4–5×/wk | Mi Band | Photo + voice, logs everything |
| `CN-02` | 王婷 Wang Ting | 29 / F | Chengdu | 163 cm | 64.8 → 63.9 kg | 105 g | Glute bridge / squat, 3×/wk | none | Photo, forgets the scale — and in week 2 it breaks |
| `DE-01` | Jonas Brandt | 34 / M | Berlin | 182 cm | 88.9 → 88.6 kg | 155 g | Push / pull / legs, 3×/wk | none (sleep from a watch) | Manual + photo, never logs at the weekend |
| `US-01` | Michael Chen | 38 / M | San Francisco | 175 cm | 86.0 → 86.2 kg | 165 g | 5×5, 3–4×/wk | WHOOP | Photo, logs takeout as-is |
| `US-02` | Sarah Williams | 34 / F | Austin, TX | 168 cm | 74.2 → 74.1 kg (mean 74.20 → 74.20) | 130 g | Upper/lower, 4×/wk | Apple Watch | Photo + manual, drinks on Fridays |
| `UK-01` | James O'Brien | 41 / M | Manchester | 180 cm | 93.5 → 94.3 kg (mean 93.87 → 94.77) | 160 g | Squat / bench / deadlift, 3×/wk | Garmin | Manual, estimates loosely |
| `MX-01` | Carlos Ramírez | 27 / M | Mexico City | 172 cm | 78.0 → 78.3 kg | 145 g | Powerbuilding, 4×/wk | none | Voice, fast and imprecise |
| `NG-01` | Adaeze Okonkwo | 31 / F | Lagos + London | 165 cm | 70.5 → 70.5 kg | 120 g | Squat / RDL, 3×/wk | Fitbit | Manual, skips days when travelling |
| `IN-01` | Priya Sharma | 30 / F | London | 158 cm | 61.3 → 61.2 kg | 100 g | Squat / RDL, 3×/wk | none | Voice, describes meals aloud |
| `BR-01` | Rafael Souza | 36 / M | São Paulo | 177 cm | 88.4 → 87.4 kg (mean 88.40 → 88.00) | 155 g | Push / pull / legs + Sat upper, 4×/wk | none (sleep from the phone) | Photo + manual, voice in the gym, churrasco at the weekend |

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
Her bathroom scale has been out of batteries twice in the first week; in the second it gives up
entirely, and the replacement only arrives on the Sunday.

**Why she exists.** The hard case for **estimation under fat**: the AI can see the food but
cannot see the oil. She also does something almost no fixture does — she *overrides* the
model and says so in `edited:`. And in her second week (`09-21 → 09-27`) her scale dies for
good, which makes her the **coverage** case as well: five consecutive days with no weight.

**Injected failures.** `edited: 米饭 150g->120g` on one meal (a human correction of an
AI overestimate); three days with no weight logged (`unknown`); one day at 1,630 kcal with
64 g protein; an explicit note that oil is the weakest number of the day. In the second week:
**five consecutive missing weigh-ins** (`09-22 → 09-26`, the battery cover stripped), a 63 g
protein day, one 2,810 kcal birthday hotpot, and a new scale on the Sunday that replaces the
old one — so the two readings that bracket the gap come from two different pieces of hardware.

**What a correct report must say.** Oil is the dominant unknown in her log, and the correct
response is to reduce the variance (cook with a measured spoon for a week) rather than to
guess a bigger number. A report that silently picks a value has failed the test.

In the second week the quantity problem is different: **there is no weekly weight to report.**
Two readings bracketing five blank days are not a 7-day mean — the first is a Monday after a
hotpot, the second a Sunday morning on a brand-new scale — so both the mean and the trend must
print `——`. A report that averages them to `64.25 kg` and subtracts last week's `64.58 kg` will
say "−0.33 kg, pace normal, hold the plan", which is a conclusion the data cannot carry. The
front half of her log (4 weigh-ins of 7) is exactly the smallest number that still can.

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
bowl of queso add roughly 900 kcal to a day that photographs as a normal taco day. In her second
week (`09-21 → 09-27`) she is also the **plateau** case: the 7-day weight mean is the same
`74.20 kg` two weeks running, which makes the "flat for 2 consecutive weeks → increase deficit by
150 kcal" rule reachable for the first time.

**Injected failures.** 1,240 kcal dinner including two margaritas; a chips-and-queso snack;
one day with no `intake_kcal` in Totals (aggregator computes it); Friday at −390 kcal deficit.
In the second week: a 2,570 kcal Friday (−220 kcal deficit) that reproduces the same pattern, one
meal logged as `source: estimated` because a restaurant plate cannot be photographed into a number,
and two protein misses (107 g Friday, 106 g Saturday) that put adherence at exactly `5/7`.

**What a correct report must say.** The confounder is alcohol and restaurant chips, not
tortillas. A report that tells her to cut carbs has misread the data.

In the second week the question is different: **two weeks of a real ~400 kcal average deficit and
no movement in the mean.** A log that is being executed (5 of 7 protein days, 4 sessions, nothing
skipped) and a scale that will not move is a plateau, not an adherence problem — so the plan
changes, not the effort. The review must raise the deficit by 150 kcal and say why. Two traps sit
on either side of that answer: reading the week as `−0.3 kg` (first minus last: `74.4 → 74.1`) and
concluding "still falling, hold", or reading its `5/7` adherence as too low and spending another
week on protein. The mean is what makes it flat, and `5/7` is deliberately the smallest number that
does not trip the protein rule (`< 5 of 7`).

---

## 5. UK-01 · James O'Brien

**Context.** 41, Manchester, works in logistics. Pub culture is part of the job. Wears a
Garmin, logs by hand and estimates generously in both directions.

**Why he exists.** The **liquid-calorie outlier**: Wednesday's three pints of bitter push a
normal day to 2,540 kcal, and Sunday's roast lamb is the single largest meal in the whole
fixture set at 1,420 kcal. In his second week (`09-21 → 09-27`) he is also the **rising trend**:
the 7-day weight mean goes `93.87 → 94.77 kg`, which makes him the only fixture whose weight
trend is **positive** — and therefore the only one that can catch a review which reads the size
of the trend but not its sign.

**Injected failures.** A 1,680 kcal pub dinner including three pints; a full English on
Saturday; Sunday with no `intake_kcal`; every day above target except one; a 5.8-hour night.
In the second week: protein is fixed (six of seven days at or above 144 g) and the weight still
climbs — Sunday's roast plus a late cheese plate is the one 92 g day, the Wednesday pub and the
Friday kebab are unchanged, and every day still books a "deficit" between 180 and 600 kcal
against a Garmin burn figure that is roughly 1,000 kcal/day too high.

**What a correct report must say.** His weight is rising while his food log "looks fine"
because roughly a third of his weekly surplus is drunk. The lever is pints, not plates.

In the second week the answer changes and the discipline is in what the review must **not** say.
The ledger shows a 439 kcal average deficit and the scale shows `+0.90 kg` (0.95% of bodyweight)
— both cannot be true, and the scale is the ground truth. So: **do not** read `+0.90` as "falling
faster than 0.75%" and cut 100 kcal (that branch needs a negative trend; a sign-blind
`abs(trend)` check fires here, in exactly the wrong direction), and **do not** read it as a
plateau and add 150 kcal (`0.90` is not flat). No calorie rule in
`workflows/04-weekly-review.md` applies to a rising trend; the honest output says the expenditure
estimate is the suspect number and asks him to stop trusting the wrist. Protein does not preempt
this: at `6/7` the protein rule is silent, which is why the second week had to come *after* he
fixed it.

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

## 9. DE-01 · Jonas Brandt

**Context.** 34, Berlin, works in construction project management. Bread, cheese and sausage at
home, Kantine at lunch, and a Döner or a Currywurst when the day runs long. Trains push / pull /
legs three times a week. Logs by hand in the evening — and does not log at the weekend.

**Why he exists.** He is the **partial week** case, and the only persona whose week is not seven
logged days: he recorded `09-14 → 09-18` and nothing at all for `09-19` / `09-20`. Two **absent**
days are not two **zero** days, and the weekly row must say so — `5` days, `1/5 @155 g`.

**Injected failures.** Two days with no `## Training` section (both genuine rest days, one of them
an accidental 14-hour day); one 5.2-hour night; a day reconstructed in the evening from memory,
with a `source: estimated` dinner; 0.5 l of beer entered by hand after the photo showed only the
Döner; a Friday office cake that no photo would ever catch.

**What a correct report must say.** The week is **5 days long, not 7**, and the two missing days
are **the weekend** — the two days this pattern normally breaks on. So the report must say "1 of
the 5 days recorded", and must not (a) print `1/7`, which invents two days nobody logged, or
(b) call the week on track. The `598 kcal` average deficit is drawn from 5 days and is therefore
optimistic in an unknown direction, because the days that went unlogged are the surplus days.
Backfilling them would corrupt the same denominator the weekly review runs on.

---

## 10. BR-01 · Rafael Souza

**Context.** 36, São Paulo, operations at a family logistics firm. Pão na chapa and a pingado at
the corner before work, prato feito at a buffet at lunch, churrasco at the weekend and often at his
parents' on Sunday. Trains push / pull / legs plus a Saturday upper session, four times a week, at
a gym two blocks from the office. No wearable — sleep comes from the phone.

**Why he exists.** He is the **ISO year boundary** case, and the only persona whose dates are not in
September. His first week is `2026-12-28 → 2027-01-03`: seven days that are **one** ISO week
(`2026-W53`) and **two** calendar years. Nothing about a week's arithmetic changes at midnight on
31 December, but the *label* does. Key the week on `(day.year, ISO week number)` and those seven
days split into four and three — and the second block is printed as `2027-W53`, a week that does
not exist, because ISO 2027 has 52 weeks. His second week is `2027-01-04 → 2027-01-10`
(`2027-W01`): a different week in a different ISO year, which the trend must still subtract from.
`selftest.py`'s **T23** pins all of it.

**Injected failures.** A réveillon churrasco that puts 3,310 kcal in against 2,700 out — the only
negative-deficit day in the file, and the only drink line, whose ~400 kcal of ethanol the `P/C/F`
field deliberately cannot carry (alcohol is 7 kcal/g; the macro formula is not). A 4.6-hour night
on New Year's Day, which is also the one day with **no `## Training` section** and no session at
all. One missing weigh-in (`01-01`: a *recorded* day with `unknown`, not an absent day). A 51 g
protein day at 2,580 kcal — pastel, caldo de cana, açaí with condensed milk, pizza and a beer —
which is the severe miss, on a day he trained. Three traceable `edited:` corrections, including a
picanha portion he served himself twice.

**What a correct report must say.** Three things, in this order:

1. **The week label.** `2026-W53`, seven days, `2026-12-28 .. 2027-01-03`. Not two weeks, not
   `2027-W53`, and New Year's Day is not "day 1 of week 1". His second week is `2027-W01` — the
   first *different* week, not the first week.
2. **Week one is the first week of this persona**, so its trend is `——` because there is no prior
   week to subtract — not because the boundary confused anything. Protein is `3/7`, so the protein
   rule fires first and the réveillon day is a surplus to name, not a failure to correct.
3. **Week two: no calorie rule fires, and that is the answer.** `88.40 → 88.00 kg` is `−0.40 kg`
   (0.45% of bodyweight) — under the 0.75% line by magnitude, and `|−0.40|` is far from flat — and
   protein at `5/7` does not preempt it. The correct output is "hold the plan".

A report that prints three BR-01 rows, or prints a trend of `−0.25 kg`, has keyed the week on the
calendar year. A report that calls 01-01 the start of the week has done the same thing from the
other side.

---

## Aggregates to check after running `parse_log.py`

Measured output of `scripts/parse_log.py examples/fixtures/` — **103 days / 10 personas**.
These are the real numbers, not estimates. If your run disagrees, the parser or a fixture changed.

| ID | Days | Avg deficit | Training days | Notable |
|---|---|---|---|---|
| `CN-01` | 14 | 446 / 449 kcal | 9 | Two ISO weeks; protein 69–129 g vs a 150 g target, **0/7 days hit**; 1 day on the `computed` path. See the two-week table below |
| `CN-02` | 14 | 234 / 217 kcal | 3 / 4 | Two ISO weeks; 8 days weight `unknown` (5 of them consecutive); 1 manual correction; 1 `computed` day. **W39 has only 2 weigh-ins → weight mean and trend are `——`** |
| `DE-01` | 5 | 598 kcal | 3 | **A partial week: 5 of 7 days logged.** `09-19`/`09-20` absent (not zero); adherence reads `1/5`, not `1/7` |
| `US-01` | 7 | 687 kcal | 4 | 1 meal logged as `unknown`; Saturday +3,510 kcal (−610) |
| `US-02` | 14 | 442 / 383 kcal | 4 / 4 | Alcohol + chips; **plateau: identical mean both weeks (74.20 kg), trend `+0.00`**; Friday −390 then −220; W38 Saturday has no Totals → `——`; adherence 4/7 → 5/7 |
| `UK-01` | 14 | 623 / 439 kcal | 3 / 3 | **Rising trend: mean 93.87 → 94.77 kg, `+0.90` = 0.95% of bodyweight**; protein 0/7 → 6/7 in the second week; Sunday roast 1,420 kcal; one `computed` day (W38 Sunday) |
| `MX-01` | 7 | 373 kcal | 4 | Thursday 48 g protein; Saturday −780; 2 validator warnings |
| `NG-01` | 7 | 419 kcal | 3 | **One day with no Training section at all** |
| `IN-01` | 7 | 294 kcal | 3 | Protein rises 56 → 80 g across the week on her own initiative |
| `BR-01` | 14 | 269 / 490 kcal | 4 / 4 | **`2026-W53` → `2027-W01`: one week spanning two calendar years.** W53 is 7 days with 6 weigh-ins; 1 negative-deficit day (réveillon −610); 1 weigh-in `unknown`; 1 day with no Training section; 51 g protein day |

**Note on `DE-01`:** it is the only **partial week** in the set — 5 recorded days inside a 7-day ISO
week. Its weekly row prints `5` days and `1/5`, never `1/7`: the denominator is the days that were
**recorded**, and the two absent days are counted in neither the numerator nor the denominator.
An absent day is deliberately **not** the same thing as `weight_kg: unknown` (`CN-02`'s case) — an
`unknown` is a recorded day with a missing number, an absent day is not a record at all. Before this
fixture existed every persona-week in the set was exactly 7 days long, so `1/5` and `1/7` were
indistinguishable and a hardcoded denominator would have passed every gate.

**Note on `US-02`:** its average is over 6 days, not 7. Saturday has no `## Totals` section at
all, so `expenditure_kcal` is `None` and the deficit is genuinely unknown. The parser prints
`——` and excludes it. Treating an unrecorded day as a zero-deficit day would silently bias
every weekly average upward — this fixture exists to catch that.

**Note on `MX-01`:** it is the only file that triggers `WARN` (2 items), by design, to prove
the validator degrades instead of rejecting. Everything else is clean.

**Note on `CN-02`'s second week:** `2026-W39` is 7 recorded days with **2 weigh-ins** — `09-22` to
`09-26` are five *consecutive* recorded days whose `## Body` line reads `weight_kg: unknown`
(the scale died, then the battery-cover screw stripped). Those days are **recorded**, not absent:
meals, sleep and `## Totals` are all there, every deficit in that week is fully computable, and
the two rest days among them simply have no `## Training` section. The only thing missing is the
ground truth.

Two readings bracketing five blank days are not a "7-day mean", so both the mean and the trend
print `——`. The naive output is `64.25 kg → −0.33 kg`, which looks *completely normal*: 0.5% of
bodyweight per week, inside the target band, so the review would say "hold the plan". The two
readings are a Monday after a hotpot (high) and a Sunday morning on a brand-new scale (low);
their difference measures water and hardware, not fat. **A number that looks normal is the most
expensive kind of wrong answer**, which is why this is a fixture and not a paragraph.

The other week in the same file is the boundary on the other side: `2026-W38` has **4** weigh-ins
and *does* produce a mean (`64.58 kg`). 4 of 7 computes, 3 of 7 does not — so a parser that
requires 7, or one that accepts 2, both fail on this one persona.

---

## `CN-02` across its two ISO weeks

| ISO week | Dates | Days | Avg deficit | Weight mean | Trend | Protein adherence | Training |
|---|---|---|---|---|---|---|---|
| `2026-W38` | 09-14 → 09-20 | 7 | 234 kcal | 64.58 kg (4 weigh-ins) | `——` (first week) | 1/7 @105 g | 3 days |
| `2026-W39` | 09-21 → 09-27 | 7 | 217 kcal | `——` (2 weigh-ins) | `——` (no mean to subtract) | 1/7 @105 g | 4 days |

**What a correct review must conclude.** Nothing about weight. The mean is unknown, so the trend
is unknown, and both of the first two recalculation rules (`falling faster than 0.75%`, `flat for
two consecutive weeks`) are **unanswerable this week** — not "satisfied", not "not satisfied".
The honest output names the missing input and asks for it: get four weigh-ins next week before
touching calories. A review that prints `−0.33 kg` has run a rule on a number the log never
contained.

---

## `US-02` across its two ISO weeks

| ISO week | Dates | Days | Avg deficit | Weight mean | Trend | Protein adherence | Training |
|---|---|---|---|---|---|---|---|
| `2026-W38` | 09-14 → 09-20 | 7 | 442 kcal (6 days) | 74.20 kg (7 weigh-ins) | `——` (first week) | 4/7 @130 g | 4 days |
| `2026-W39` | 09-21 → 09-27 | 7 | 383 kcal | 74.20 kg (7 weigh-ins) | **`+0.00` kg** | 5/7 @130 g | 4 days |

**What a correct review must conclude.** This is a plateau, and the rule that fires is:

> if weight trend is flat for 2 consecutive weeks → **increase deficit by 150 kcal**

The two weeks have **the same 7-day mean to the hundredth of a kilo** while the daily readings move
0.8 kg across the week. That is the whole argument for the mean: `74.4 → 74.1` by endpoints says
`−0.3 kg`, which would read as "still falling, hold the plan", and the week is not falling at all.
`74.4` (Monday) and `74.1` (Sunday) are two single mornings; `74.20` twice is the plateau.

Adherence does **not** get in the way, and that is deliberate: `5/7` is the smallest number of days
that leaves the protein rule (`< 5 of 7 → fix protein first`) silent. At `4/7` — the first week's
figure — the protein rule would preempt the plateau, and a fixture that never lets the plateau rule
be the operative one would close nothing. Both misses are Friday and Saturday, the two days the
alcohol and the chips are also in; the review should name that link, not treat five days as a
failure.

The proposed change is therefore one variable, with its arithmetic shown: deficit `+150 kcal/day`,
everything else held.

---

## `UK-01` across its two ISO weeks

| ISO week | Dates | Days | Avg deficit | Weight mean | Trend | Protein adherence | Training |
|---|---|---|---|---|---|---|---|
| `2026-W38` | 09-14 → 09-20 | 7 | 623 kcal (6 days) | 93.87 kg (7 weigh-ins) | `——` (first week) | 0/7 @160 g | 3 days |
| `2026-W39` | 09-21 → 09-27 | 7 | 439 kcal | 94.77 kg (7 weigh-ins) | **`+0.90` kg** | 6/7 @160 g | 3 days |

**What a correct review must conclude.** That no calorie rule fires — and that this is the
answer, not a failure to find one.

`+0.90 kg` is **0.95% of bodyweight**, larger than the 0.75% the first rule is calibrated
against. An implementation that compares `abs(trend) / weight > 0.0075` therefore fires
*"falling faster than 0.75% → reduce deficit by 100 kcal"* on a man who is **gaining** a kilo a
week. Same number, opposite conclusion, and nothing else in the gate suite notices: before this
week existed, every two-week trend in the set was negative (`CN-01`) or exactly zero (`US-02`).

Two more traps are deliberately removed so that the sign is the *only* thing under test:

- **The plateau rule must stay silent.** `+0.90` is not flat, so "flat for 2 consecutive weeks →
  +150 kcal" must not be reachable by rounding. A fixture where the gain were small (say
  `+0.1 kg`) would let a sloppy flatness test pass for the wrong reason.
- **The protein rule must not preempt.** W38 is `0/7`, and at `< 5 of 7` the protein rule stops
  the review before it ever gets to the weight. So the second week is the week *after* he fixed
  it: `6/7`, one Sunday miss (roast + late cheese plate = 92 g). If both weeks had stayed at
  `0/7`, the wrong-sign bug would be invisible even with a positive trend in the file.

**The ledger is the third trap.** Every day books a deficit of 180–600 kcal, and the week
averages 439 — while the scale rises 0.9 kg. Those cannot both be true. The Garmin burn figure
is the number to distrust (his own notes say so), and that is what the review has to say. A
review that reports "deficit 439 kcal, on track" has read the arithmetic and ignored the only
measurement in the file that is not an estimate.

---

## `CN-01` across its two ISO weeks

This is the only persona in the repo whose week-over-week trend is **falling fast enough to reach**
the 0.75% branch — `CN-02`'s second week has no mean to subtract, `US-02`'s second week is flat,
`UK-01`'s second week is **rising** (that one is the counter-example: a positive trend must not fire
this branch either), and `BR-01`'s second week is falling at only `−0.40 kg` (0.45% of bodyweight,
under the line by magnitude, so it never gets to the rule). That makes this pair the only place
where the `falling faster than 0.75%` branch of `workflows/04-weekly-review.md` can be checked
*with its sign pointing down*, including its precedence against the protein rule.

| ISO week | Dates | Days | Avg deficit | Weight mean | Trend | Protein adherence | Training |
|---|---|---|---|---|---|---|---|
| `2026-W37` | 09-07 → 09-13 | 7 | 446 kcal | 82.73 kg | `——` (first week) | 0/7 @150 g | 4 days |
| `2026-W38` | 09-14 → 09-20 | 7 | 449 kcal | 82.01 kg | **−0.71 kg** | 0/7 @150 g | 5 days |

**What a correct review must conclude.** Weight is falling (−0.71 kg/week ≈ 0.9% of bodyweight),
which would normally trigger *"reduce deficit by 100 kcal"*. **It must not.** Protein adherence
is 0/7, and the rule that fires first is:

> if protein adherence < 5 of 7 days → **do not change calories; fix protein first**

The whole point of this fixture pair is that the *weight* signal says one thing and the
*adherence* signal says another, and the documented order of precedence picks adherence. A
report that proposes a calorie change here has skipped the check that separates this system
from a calorie diary.

**On the trend arithmetic.** It is the mean of the seven daily weights, not the first minus
the last. Using endpoints would let two days of water weight decide a whole week's conclusion:
`82.4 − 81.6 = −0.8 kg` looks like a bigger drop than the true `−0.71 kg`, and neither number
is the one the rules are calibrated against.

---

## `BR-01` across its two ISO weeks

| ISO week | Dates | Days | Avg deficit | Weight mean | Trend | Protein adherence | Training |
|---|---|---|---|---|---|---|---|
| `2026-W53` | 12-28 → 01-03 | 7 | 269 kcal | 88.40 kg (6 weigh-ins) | `——` (first week) | 3/7 @155 g | 4 days |
| `2027-W01` | 01-04 → 01-10 | 7 | 490 kcal | 88.00 kg (7 weigh-ins) | **`−0.40` kg** | 5/7 @155 g | 4 days |

Read the dates, not the labels: week one **starts in 2026 and ends in 2027**, and it is still one
week. `2026-12-28 .. 2026-12-31` are four calendar-2026 days; `2027-01-01 .. 2027-01-03` are three
calendar-2027 days; together they are ISO week **2026-W53**, because ISO weeks belong to the ISO
week-year, which is the year that owns the week's Thursday — `2026-12-31`. The next Monday,
`2027-01-04`, opens `2027-W01`.

**What a correct review must conclude.** For week two: **no calorie rule fires.** `−0.40 kg` is
0.45% of bodyweight (the 0.75% line would need 0.66 kg), so the "falling faster than 0.75%"
branch is silent by magnitude; `|−0.40|` is nowhere near flat, so the plateau branch is silent
too; and protein at `5/7` is above the `< 5 of 7` line, so the protein rule does not preempt it.
"Hold the plan" is the answer, and it is an answer this time, not an absence of one.

**The defect this fixture exists to catch.** Re-key the week on `(day.year, ISO week number)` and
the same file prints:

| what a naive key prints | days | weigh-ins | weight mean | trend |
|---|---|---|---|---|
| `2026-W53` | 4 | 4 | 88.25 kg | `——` |
| `2027-W01` | 7 | 7 | 88.00 kg | **`−0.25` kg** |
| `2027-W53` | 3 | 2 | `——` | `——` |

Three rows instead of two, a trend of `−0.25` instead of `−0.40` (it subtracted a four-day mean),
and a label — `2027-W53` — for a week that does not exist. Every number in that table looks
plausible. That is the problem: the 4-day mean `88.25` is a real average of real readings, and
`−0.25 kg` is inside the target band, so a review built on it would say "hold the plan" for the
wrong reason. `selftest.py` T23 asserts both sides — the correct grouping *and* the fact that the
naive key really does produce `4 / 3 / 7` with a phantom `2027-W53`.

**Why week one is 6 weigh-ins, not 7.** `01-01` is `weight_kg: unknown` — a *recorded* day with a
missing number (he woke at 11:30 after the party), which is a different thing from `DE-01`'s two
**absent** days. 6 of 7 is still above the 4-reading floor, so the mean and the `——` trend here are
real numbers, not a degraded path.
