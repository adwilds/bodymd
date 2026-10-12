# FAQ

## Is this a calorie tracker?

No. It is a file format and four workflows. You can run it with no software at all — a folder, a phone camera, and any AI you can paste text into.

## Why not just use an app?

Apps are faster and more convenient. They also hold your data, can move features behind a paywall, and get acquired. In May 2026 MyFitnessPal moved photo scanning to Premium; Cal AI was acquired by MyFitnessPal in early 2026.

If you want convenience, use an app. If you want to own the record, use this.

## Can I use this alongside an app?

Yes, and it is a reasonable first step. Run both for two weeks, then decide which record you would rather still have in five years.

## Which model should I use?

Whichever you have. The data contract is deliberately model-agnostic. Meal photo analysis is the only step that meaningfully benefits from a stronger vision model.

## Why can't the AI read the barbell weight from my video?

Because a camera cannot see the number printed on the plate, and depth cues are not reliable enough to infer it. Exercise type and rep count are detectable; **load is not**.

Anyone claiming automatic weight detection from a phone video is either reading it from a wearable or asking you to type it. Say the weight. It takes two seconds.

## How accurate is the calorie estimate?

It depends on the meal, and honesty matters more than the number:

- **Simple plate** (chicken, rice, broccoli): roughly within 10-15%
- **Mixed dish** (curry, stir-fry, stew): materially worse
- **Restaurant food**: the weakest case — portions are unknown and hidden fats are invisible

The estimate is a starting point you edit, not a measurement. This is why the log has an `edited` field on every meal.

## Why is protein the headline number and not calories?

Because in a deficit, protein intake is what protects muscle. Calories decide the rate; protein decides what you lose. The daily report shows the deficit first and the protein gap second for that reason.

## Do I need a wearable?

No. Sleep and expenditure are inputs, not requirements. Without a wearable, use a weekly weight trend as the ground truth — it is slower but it is not wrong.

If you do have one (Oura, Apple Watch, Whoop, Garmin), export or paste the daily numbers into the `## Sleep` block. The workflow does not care about the brand.

## Will this work for a beginner?

The four workflows assume you already know what a set and a rep are. It is not a training programme and it will not teach you the lifts. For that, hire a coach or follow an established programme — then use bodymd to hold the record.

## Can I use it for bulking, maintenance, or a cut?

Yes. The workflow is deficit-oriented by default because that is the hard case, but the format is just a log. Set `deficit_target_kcal` to 0 for maintenance or negative for a surplus and the arithmetic follows.

## What about GLP-1 medications?

bodymd does not advise on medication. It is a logging and recalculation workflow.

Worth knowing if you are on one: this class of medication reduces muscle mass alongside fat, which is the specific problem that protein targets and resistance training address. Discuss anything medication-related with your prescriber.

## Is my data safe?

Your data is a folder on your device. This project has no server, no analytics, and no telemetry.

Two things to be careful about: don't commit `log/` to a public repo, and remember that if you sync to a cloud folder, that cloud is now holding your health data.

## I want an app for this. Will you build one?

No. The entire point is that your data is a folder you own. An app puts it back in someone else's database.

## Something in the workflow doesn't fit my situation.

Open an issue describing the case. Workflow changes are welcome. App requests will be closed.

## Can I use this at my company / for my clients?

Commercial use requires a license. See `LICENSE.md`.
