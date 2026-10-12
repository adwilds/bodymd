# Copilot instructions for this repository

This is a **body-management workflow**, not an application.

**Read [`SKILL.md`](../SKILL.md) before generating anything.** It is the operator manual:
the four workflows, the data contract, and the rules all live there.

## Rules

- **`log/*.md` is append-only.** Never rewrite or delete a line. Correct by appending with
  `edited: <what changed and why>`.
- **Every nutrition line needs `source:`** — `photo`, `voice`, `manual`, `wearable`,
  `video+voice`, or `estimated`.
- **`unknown` beats a guess.** Never fabricate a weight or a portion.
- **Never modify `profile.md`** without explicit confirmation.
- **No medical advice.** All numbers are estimates.

## Layout

`SKILL.md` (manual) · `workflows/` · `templates/` · `scripts/` · `docs/` · `examples/`

See [`AGENTS.md`](../AGENTS.md) for the full rule list.
