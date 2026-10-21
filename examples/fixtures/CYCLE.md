# The simulation cycle

**What this is.** A repeatable procedure for growing the fixture set one honest step at a time.
It exists because this repository has exactly one form of evidence it can generate on its own:
**synthetic data that survives its own validator.**

**What this is not.** It is not a way to manufacture the impression of real users. Read the
hard rules before anything else.

---

## Hard rules (none of these are negotiable)

1. **Every new file carries the `SYNTHETIC` marker** in its first line, and every new persona
   is registered in `personas.md` with a name that is obviously fabricated.
2. **Never invent provenance.** Do not write "real user", "anonymized", "published with
   permission", "collected from a pilot", or any phrasing that implies a human used this.
   *This repository has already had to retract exactly that claim once.* Fabricated
   provenance is worse than no data: it is a lie that survives review.
3. **The validator is the arbiter, not the author.** A cycle that adds data which
   `validate_log.py` rejects is not a cycle — it is a broken commit. Fix the data.
4. **A cycle may not weaken the contract to make new data pass.** If new data does not fit
   `SKILL.md` §3, either the data is wrong, or the contract has a real gap — and a contract
   change is its own commit with its own reasoning, never a side effect.
5. **Never claim an unexecuted acceptance test.** `docs/testing.md` §8 describes a real-user
   pilot that **has not been run**. Fixtures do not substitute for it, and may not be described
   as if they did.

---

## One cycle

Do these in order. Each has a concrete output.

**1. Pick the top open gap** from the backlog below. If the backlog is empty, stop and say so —
do not invent a gap to keep the loop busy.

**2. Make the smallest fixture change that closes it.** Usually one new week for one existing
persona, or one new persona. One gap per cycle.

**3. Write the data so the arithmetic is real.** Sums must actually add up:
`intake = Σ meals`, `protein = Σ meals`, `deficit = expenditure − intake`. Deliberate
imperfections (a missed lunch, a dead scale, a skipped day) are welcome and are **the point** —
but they must be *internally consistent* imperfections.

**4. Run every gate.** All four must pass before anything is committed:

```bash
python3 scripts/selftest.py                          # expect 22/22 PASS
python3 scripts/validate_log.py examples/fixtures/   # expect 0 fatal, 2 warnings
python3 scripts/parse_log.py    examples/fixtures/   # expect 82 days / 9 personas
```

Plus: every relative Markdown link resolves.

**5. Update the registry.** `personas.md` (baseline table, aggregate table, any new
"what a correct report must say" paragraph) and `examples/fixtures/README.md` (layer counts).
A fixture without a registry entry is an orphan: nobody knows what it is for.

**6. If a gate fails, fix the real cause.** A failure is the most valuable thing a cycle
produces. If a fixture exposes a parser bug, fix the parser and add an assertion to
`selftest.py` — an unfixed finding will be re-found by the next cycle, forever.

**7. Commit and push** with the proxy set (see below), one commit per cycle, message stating
which gap was closed and what it now covers.

```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 git push origin main
```

Use `gh` for any repository creation. **Do not touch the user's browser.**

---

## Definition of done for a cycle

- [ ] Exactly one coverage gap closed, named in the commit message
- [ ] New data passes `validate_log.py` with 0 fatal errors
- [ ] `selftest.py` is green, and **its assertion count went up** if the cycle found a real defect
- [ ] Registry updated; no orphan fixture
- [ ] No provenance claim anywhere that is not literally true
- [ ] Pushed, and the remote tree matches the local tree

---

## Coverage backlog

Ordered by value. Strike through an entry when closed, and note the commit.

| # | Gap | What it would prove |
|---|---|---|
| ~~G1~~ | ~~**A partial week** — a persona who logged 5 of 7 days~~ → **CLOSED** by `DE-01` (`09-14 → 09-18`, five of seven days): the weekly row prints `5` days / `1/5 @155 g`, and T19's independent recomputation rejects a hardcoded `/7`. Commit: *"Close G1 — a partial week, so the adherence denominator cannot be 7"* | The adherence denominator. "0/5" and "0/7" are different claims, and a naive implementation reports the same number for both |
| G2 | ~~**Weight missing for 4+ consecutive days**~~ → **CLOSED** by `CN-02` (`2026-09-21 → 09-27`, five consecutive missing days, only 2 weigh-ins): the week's mean and trend print `——`, and T20 pins both sides of the threshold (4 of 7 still computes). It found a real defect: the old aggregator averaged the two stray readings into `64.25 kg` and reported `-0.33 kg`. Commit: *"Close G2 — five blank days are not a week's mean"* | That the trend degrades to `——` instead of averaging two stray weigh-ins into a confident conclusion |
| ~~G3~~ | ~~**A genuine plateau** — two consecutive weeks with the same mean~~ → **CLOSED** by `US-02` (`2026-09-21 → 09-27`, a second week whose 7-day mean is the identical 74.20 kg): the trend prints `+0.00` and T21 pins it, together with the two things that would hide it — the week's endpoints read `74.4 → 74.1` (`−0.3 kg`, i.e. "still falling"), and its `5/7` adherence sits exactly one day above the protein rule that would otherwise preempt the plateau. Commit: *"Close G3 — two weeks at the same mean, so the plateau rule can fire"* | The `flat for 2 consecutive weeks → increase deficit by 150 kcal` rule. Currently unreachable: no persona has two weeks *and* flat weight |
| G4 | **A persona gaining weight** | That the "falling faster than 0.75%" branch does not fire on the wrong sign |
| G5 | **A week spanning an ISO year boundary** (e.g. 2026-12-28 → 2027-01-03) | That week numbering does not silently merge two different weeks into one label |
| G6 | **A persona with no `protein target` in the header** | That the adherence column shows `——` rather than guessing a target |
| G7 | **Every meal on one day `source: estimated`** | That an all-guess day is visible as such, not averaged in as if it were measured |
| G8 | **A 30-day single file** | That parsing scales past two weeks without the label/date logic collapsing |

**If you close every gap above and the gates are still green, the cycle loop is finished.**
The honest answer at that point is "the fixture set is complete for this contract", not
"generate more personas".

---

## Why one gap per cycle

Because a cycle that changes five things at once cannot be reviewed, and when a gate fails you
cannot tell which change broke it. **This repository's most expensive defects were all found by
running one new thing through an existing check** — not by adding volume.
