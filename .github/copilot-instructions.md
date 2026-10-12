# Copilot instructions for this repository

This is a **body-management workflow**, not an application.

**Read [`SKILL.md`](../SKILL.md) before generating anything.** It is the operator manual:
the four workflows, the data contract, and the rules all live there.

## Rules

- **`log/*.md` is append-only.** Never delete a line and never change a number silently. A
  correction updates the `edited:` field of **that same line** (`SKILL.md` §3.4) — never append a
  second copy of the same meal, because `## Totals` would count it twice.
- **Every nutrition line needs `source:`** — `photo`, `voice`, `manual`, `wearable`,
  `video+voice`, or `estimated`. Training, `## Body` and `## Sleep` lines use their own sets
  (`SKILL.md` §3.4); do not apply the meal list to them.
- **`unknown` beats a guess.** Never fabricate a weight or a portion.
- **Never modify `profile.md`** without explicit confirmation.
- **No medical advice.** All numbers are estimates.
- **Optional fields are optional.** `order_ok`, `## Body`, `## Supplements` may be absent; never
  invent them to fill space.

## Layout

`SKILL.md` (manual) · `workflows/` · `templates/` · `scripts/` · `docs/` · `examples/`

See [`AGENTS.md`](../AGENTS.md) for the full rule list.
