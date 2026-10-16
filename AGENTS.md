# AGENTS.md

This repository is a **body-management workflow**, not an application.

**Read [`SKILL.md`](SKILL.md) first.** It is the operator manual: it defines the four
workflows, the data contract, and the rules.

---

## Rules for any agent working in this repo

1. **Read `SKILL.md` before answering anything.** Do not improvise a workflow.
2. **Read `profile.md`** (if present) for the user's baseline and targets.
3. **`log/*.md` is append-only**, with one precisely defined exception: **a correction updates the
   `edited:` field of that same line** (`edited: rice 150g -> 120g`). Never delete a line, never
   change a number without saying so in `edited:`, and **never append a second copy of the same
   meal** — `## Totals` would count it twice. The history *is* the data.
4. **Every nutrition line needs `source:`**, legal values:
   `photo` · `voice` · `manual` · `wearable` · `video+voice` · `estimated`.
   **Training, `## Body` and `## Sleep` lines use different sets** (`SKILL.md` §3.4) — do not
   apply the meal list to them.
5. **`unknown` beats a guess.** If a weight or portion cannot be known, write `unknown`.
   An explicit unknown keeps the deficit honest; a fabricated number corrupts it.
6. **Never write to `profile.md` without explicit confirmation.** It records the user's
   own decisions, not the model's.
7. **Do not give medical advice.** No diagnoses, no medication guidance, no promised
   outcomes. Estimates only.
8. After changing anything under `scripts/`, run `python3 scripts/selftest.py`.

---

## Layout

| Path | What it is |
|---|---|
| `SKILL.md` | ⭐ Operator manual — start here |
| `workflows/` | The four daily workflows |
| `templates/` | The file formats |
| `scripts/` | Contract validator, weekly aggregator, self-test |
| `docs/` | `run-with-any-model.md`, testing, dev guide, user guide, BYOK, FAQ |
| `docs/zh-CN/` | Chinese versions |
| `examples/` | One worked week + 9 synthetic users (eight full weeks, one partial) |

---

## License

MIT (code, workflows, templates) · CC BY-NC-SA 4.0 (docs) · commercial use requires a
license. See [`LICENSE.md`](LICENSE.md).
