# Why local data

*A short argument for keeping your body's records in files you own.*

---

## The thing nobody says out loud

Every food app is a data business with a calorie counter attached.

That is not a criticism — it is a description. MyFitnessPal, Lose It!, Yazio, Cal AI: they all hold your log on their servers, behind their login, under their terms. That is the deal, and for a lot of people it is a fine deal.

It stops being a fine deal in three situations.

**One: the paywall moves.** In May 2026 MyFitnessPal moved photo meal scanning, recipe URL import, and per-meal macro goals behind Premium. The workflow you built your habit on was now $79.99 a year. Your data did not change. Your access did.

**Two: the company changes hands.** Cal AI — the photo-first tracker two teenagers built to $30M+ ARR — was acquired by MyFitnessPal, the incumbent it was built to disrupt. It still runs as a standalone app. For now. When the roadmap, the pricing, or the sun-setting decision arrives, it will arrive from a company you did not choose.

**Three: the model changes.** This one is new, and it is the real one. Your tracker now depends on a vision model you do not control. When that model is upgraded, replaced, or deprecated, your "AI accuracy" moves — and you have no way to compare, because you cannot see which model produced which number.

## The reframe

The instinct is to ask: *which app should I use?*

The better question is: **what do I actually own at the end?**

- Own an app subscription -> you own access, revocable
- Own a database export -> you own a blob you cannot read
- **Own a folder of plain Markdown -> you own the thing itself**

## What "owning it" buys you, concretely

**Swappability.** When a better model ships, you point your workflow at it. No migration, no re-logging, no "import your history" flow that loses half the fields. The data contract does not care which model reads it.

**Auditability.** Every number in the log carries a `source` field: `photo`, `voice`, `manual`, `wearable`. You can always answer "where did this come from" — including "that was an estimate from a weaker model in October".

**Permanence.** A folder survives a startup's shutdown, an acquisition, an API deprecation, and your own changing interests. A `.md` file will be readable in 2050.

**No metering.** You bring your own key, so no one counts your scans. The workflow does the same thing on day 1 and day 400.

## The honest counter-arguments

**"Local files are less convenient."** True. There is no push notification, no widget, no camera button on your home screen. You open a folder instead of an app. That is a real cost, and for many people it outweighs the benefit.

**"No automatic sync."** You pick your own sync — iCloud, Dropbox, git, or nothing. That is more work and more control in the same package.

**"The AI still processes my photos."** Also true. Local storage is not local inference. Your photo goes to whichever model you chose. The difference is that you chose it, you can see the API call, and you can switch providers — which is more than the app model gives you.

## The thesis, stated plainly

> In the AI era, the moat is not the model — it is the **data contract**.

Models are commoditising, fast. Everyone has access to roughly the same capability. What almost nobody has is a stable, readable, swappable representation of their own data that survives a model change.

That is the part worth building. The calories are downstream of it.

## What this means for a product builder

If you are building anything AI-native, ask: **if my user switched models tomorrow, would their data still work?**

- If yes, you have a product.
- If no, you have a wrapper with a subscription attached. The 2026 numbers on those are unkind: most are abandoned or under $500/month within six months.

The contract is the product. The rest is interface.

---

*This document is licensed CC BY-NC-SA 4.0. Commercial use requires a license.*
