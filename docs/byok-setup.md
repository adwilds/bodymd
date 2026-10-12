# BYOK setup

**BYOK = Bring Your Own Key.** bodymd runs on your AI account, not ours. There is no server in this project and no key ever passes through a third party.

This is not a limitation. It is the reason the project can exist without a business model attached to your meals.

---

## What you need

1. An AI tool that can read files from a folder and look at photos. Any of these work:
   - Claude Code, Cursor, Codex, or a similar agentic coding tool
   - CodeBuddy / WorkBuddy or another desktop AI assistant with filesystem access
   - Any chat model you can paste file contents into and paste results back out of
2. A folder. That is the whole storage layer.
3. Optional: a wearable export (Oura, Apple Health, Google Health Connect) for the sleep and expenditure numbers.

**Cheapest viable setup:** a free-tier model with file upload, plus manual copy-paste. The workflow is not dependent on agentic tooling — it is dependent on the file format. That is deliberate.

---

## Setup, in order

**Step 1 — clone and configure**

```bash
git clone https://github.com/adwilds/bodymd
cd bodymd
cp templates/profile.md profile.md
mkdir -p log reports photos
```

**Step 2 — fill in `profile.md`**

Only four numbers matter at the start: `weight_kg`, `protein_target_g`, `deficit_target_kcal`, and `program`. Everything else can wait.

**Step 3 — open your AI tool at this folder**

Point it at the repository directory so it can read `SKILL.md`, `profile.md`, and `log/`.

**Step 4 — run one day**

> Read SKILL.md. I'm starting today.

Then send a meal photo.

**Step 5 — keep the run going for 14 days before judging it**

The system is worthless for one day and informative for two weeks. The weekly review is where it starts paying.

---

## Cost expectations

| Setup | Rough monthly cost |
|---|---|
| Free tier + manual copy-paste | $0 |
| Paid agentic tool, ~90 meal photos + 12 training videos/month | one subscription, your provider's rate |
| Everything local except photo analysis | $0 |

Note what is **not** in that table: a per-scan fee. Nobody meters you here.

---

## Sync (optional)

Pick exactly one:

- **iCloud / Dropbox / OneDrive folder** — easiest, works on phone and laptop
- **git** — best if you want history and diffable changes
  ```bash
  git add log/ && git commit -m "week 41" && git push
  ```
- **nothing** — a local folder that never leaves your device

⚠️ If you use a third-party sync service, your health data sits on their servers. That is a trade-off, not a bug. Choose it knowingly.

---

## Security notes

- **Never commit `profile.md` or `log/` to a public repository.** Add them to `.gitignore` before your first push.
- Photos carry GPS metadata. Strip it if your photos leave the device.
- Your API key belongs in your tool's own config, never inside this repository.
- If you sync to git, use a **private** repository.

---

## If you are at a company

Deploying bodymd as an employee wellness programme, or delivering it to a client, is **commercial use** and requires a license. See `LICENSE.md`.
