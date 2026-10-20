# LaunchKit Lite — free Claude Code skills for shipping a SaaS

Two skills, free, MIT licensed:

- **`prelaunch-qa`** — "am I ready to launch?" → scored audit of auth, payments, secrets, data, errors, legal, and launch surface, with a go/no-go verdict and file:line fixes.
- **`landing-copy`** — "write my landing page" → converting copy written straight into your components: 3 headline variants, proof strip, problem, how-it-works, features-as-benefits, FAQ, pricing, CTA.

## Install

```
cp -r skills/* ~/.claude/skills/
```
or
```
/plugin marketplace add https://github.com/Raem-Ai/launchkit-lite
/plugin install launchkit-lite@launchkit-lite
```

## The full kit

LaunchKit adds four more skills: **Stripe billing** (Checkout, verified webhooks, DB as source of truth, portal, every failure state), **legal pages** generated from your real data flows, **launch posts** for PH / Show HN / Reddit / X / LinkedIn / email, and **analytics setup** around your activation moment.

→ https://raem.gumroad.com/l/launchkit — $29, unlimited projects.

## Also in this repo

- **`docs/etsy-title-fixer/`** — free bookmarklet that scores an Etsy listing title against what buyers type into Etsy search. Live: https://raem-ai.github.io/launchkit-lite/etsy-title-fixer/
- **`reel-factory/`** — the open-source pipeline (ffmpeg + Playwright + Whisper) behind the daily challenge reels. The method and prompts are in the Reel Factory kit on Gumroad.

Both came out of the "$100 → $10,000 in 30 days" challenge: https://carlosg.ai/challenge
