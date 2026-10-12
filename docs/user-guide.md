# User Guide

> **Note on language:** this guide ships in English. The Chinese version is [`docs/zh-CN/user-guide.md`](zh-CN/user-guide.md) — written for the Chinese market, not a translation of this page.

---

## What this is

bodymd turns your AI into a body-management system that writes to files you own.

No app. No account. No subscription. Your log is a folder.

---

## 5-minute setup

**1. Get the folder**

```bash
git clone https://github.com/adwilds/bodymd
cd bodymd
```

**2. Create your files**

```bash
cp templates/profile.md profile.md
mkdir -p log reports photos
```

**3. Fill in four numbers**

Open `profile.md`. Only these matter at the start:

```yaml
weight_kg: 75.0
protein_target_g: 145
deficit_target_kcal: 600
program: [deadlift, squat, bench]
```

**4. Open your AI at this folder**

Point Claude Code, Cursor, Codex, or any agentic tool at the repository directory.

**5. Start**

> Read SKILL.md. I'm starting today.

---

## The four daily actions

### Action 1 — Log a meal

Take a photo **before** eating. Take a second one **after**.

Send them to your AI. You get back:

- each item, its portion, calories, protein
- a **confidence level** and why
- **the order to eat in** — protein first

**Edit anything that's wrong.** The AI does 80%. You fix the last 20%. That edit gets recorded, which is how the system learns what it gets wrong.

⏱ Target: under 15 seconds.

### Action 2 — Log training

Record one set on video. Send it.

You get back: **exercise and rep count**. That's it.

**Weight cannot be read from a video.** Say it: *"deadlift, sixty kilos."* Two seconds.

Then you get the next session's load.

### Action 3 — Check your deficit

```
expenditure − intake ≤ 600 kcal   →   you're in the fat-burning band
```

Expenditure comes from your wearable (Oura, Apple Watch, Whoop, Garmin) or an estimate.

**Every number in this system is an estimate.** None of it is a measurement.

### Action 4 — Read the report

One screen. Deficit, protein, sleep, training — plus **one** line about what changed.

If it scrolls, it's too long. Tell your AI to cut it.

---

## Every Sunday — the weekly review

This is the step that matters most.

Say: *"Weekly review."*

You get three aggregates and a proposed change:

| Aggregate | What it tells you |
|---|---|
| Average deficit | whether the plan matches reality |
| 7-day weight trend | the ground truth |
| Protein adherence | whether the intake side is being executed |

**One rule to remember:**
> If adherence is low, the system will not change your calories. It will tell you to fix the execution first.

Changing the plan when the plan isn't being followed is the most common mistake in both coaching and product design.

The system never writes to `profile.md` without your confirmation.

---

## Where your data lives

```
profile.md          your baseline and targets
log/YYYY-MM-DD.md   one file per day, append-only
reports/            generated reports
photos/             your meal and training photos
```

That's all of it. Open any file in any editor. It will still be readable in 2050.

**Back it up however you like** — iCloud, Dropbox, a private git repo, or a USB stick. Your call, not ours.

⚠️ **Never commit `log/` or `profile.md` to a public repository.** The `.gitignore` already handles this.

---

## Switching AI models

The workflow does not care which model you use.

- Today: Claude
- Tomorrow: GPT
- Next week: Gemini, Kimi, Zhipu, or whatever ships next

Just point the new tool at the same folder and say *"Read SKILL.md."* It picks up where the last one left off.

**That is the entire point of the project.** Everyone else makes you migrate. Here, there's nothing to migrate.

---

## Common questions

**Do I need a wearable?** No. Without one, use the weekly weight trend. Slower, but not wrong.

**Do I need to pay for an AI tool?** No. A free tier with file upload and copy-paste works.

**Can I use this for bulking?** Yes. Set `deficit_target_kcal` to 0 or negative and the arithmetic follows.

**Why doesn't it just build an app?** Because an app puts your data back in someone else's database. That's the thing this project exists to avoid.

**Is it a medical product?** No. It does not diagnose, treat, or cure anything. All numbers are estimates. See `docs/faq.md`.

---

## When it goes wrong

| Problem | Fix |
|---|---|
| The AI won't read `SKILL.md` | Make sure your tool is opened at the repository folder, not a parent folder |
| Estimates are way off | Check for hidden oils and sauces — that's the biggest miss. Say what was cooked |
| It asks you to log weight from video | Tell it to re-read `SKILL.md` §5.1. Load cannot be read from video |
| The report is too long | Say "one screen". It will cut |
| A field looks wrong | Run `python3 scripts/validate_log.py log/` |

---

## Commercial use

Personal use is free and always will be.

Company internal deployment, delivery to a client, or bundling into a paid product requires a license. See `LICENSE.md`.
