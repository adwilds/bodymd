# User Guide

> **Note on language:** this guide is in English because it ships to users. A short Chinese summary for the maintainer is at the bottom.

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

---

---

## 中文摘要（维护者用，对外发布时可删除）

**这是什么**：用你自己的 AI 跑的身体管理工作流。没有 App、没有账号、没有订阅。你的记录就是一个文件夹。

**5 分钟上手**：克隆 → `cp templates/profile.md profile.md` → 填四个数（体重 / 蛋白目标 / 缺口目标 / 训练动作）→ 把 AI 工具指向这个文件夹 → 说"读 SKILL.md，今天开始"。

**每天的四个动作**：拍餐（餐前+餐后，按顺序吃，先蛋白）→ 拍训练（视频只给动作和次数，**重量必须口述**）→ 看缺口（消耗 − 摄入 ≤600 kcal）→ 读日报（一屏，一条行动）。

**每周日做周复盘**：算三个聚合（平均缺口 / 7 天体重趋势 / 蛋白达标天数），系统最多改一个变量；**执行率不足时不准改计划**。

**换模型**：把新工具指向同一个文件夹即可，数据不用迁移——这就是这个项目的全部意义。

**数据在哪**：`profile.md` + `log/` + `reports/` + `photos/`。**永远不要把 `log/` 或 `profile.md` 提交到公开仓库。**
