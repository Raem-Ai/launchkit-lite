---
name: landing-copy
description: Write or rewrite landing page copy that converts, grounded in what the product actually does. Use when the user says "write my landing page", "improve my hero", "my landing page copy is weak", "write the homepage", "pricing page copy", or "rewrite this headline". Produces headline, subhead, feature sections, social proof scaffolding, FAQ, and CTAs — and writes them into the actual page components.
---

# Landing Copy

Most founder landing pages fail the same way: the headline describes the product's category instead of the customer's outcome, and the page lists features instead of answering objections. Fix both.

## Step 1 — Extract the truth (10 minutes, not 60)

Read the codebase and any README/docs. Determine:
- **Who it's for** — the specific person (not "businesses": "freelance designers who invoice monthly").
- **The painful before** — what they do today, in their words.
- **The after** — what changes once they use it.
- **The mechanism** — the one thing the product does that makes the after possible.
- **Proof available** — users, logos, metrics, testimonials, a founder story. If none, say so; don't invent.
- **Price and model** — free tier? trial? one-time?

If the repo doesn't answer "who" and "before", ask the user **one** question: "Describe the last person who signed up and what they were doing before." Then write.

## Step 2 — Write the page

### Hero
- **Headline** (≤ 10 words): the outcome, in the customer's language. Test it against three patterns and pick the strongest:
  1. Outcome: "Invoices that get paid in 3 days, not 30."
  2. Contrast: "Stop chasing clients. Start getting paid."
  3. Specific claim: "Send an invoice in 20 seconds from your phone."
  Reject anything with "platform", "solution", "seamless", "empower", "supercharge", "all-in-one".
- **Subhead** (≤ 25 words): who it's for + the mechanism.
- **Primary CTA**: a verb + the outcome, not "Get started". ("Send your first invoice", "Try it free for 14 days".)
- **Secondary CTA**: "See how it works" → demo/video/screenshots.
- **One line of friction removal** under the CTA: "No credit card." / "Free for your first 5 invoices." / "Cancel anytime."

### Proof strip (directly under hero)
Logos, a user count, a star rating, or a single strong quote. If nothing exists, use a founder line: "Built by a designer who got tired of chasing invoices." Never fabricate numbers or quotes.

### Problem section
Three short bullets of the "before", written as things the reader has said out loud. These should sting a little.

### How it works
Three steps, each: bold verb phrase + one sentence + screenshot placeholder. Steps, not features.

### Feature blocks (3–5)
Each: **benefit headline** → one sentence of mechanism → optional screenshot. Lead with the benefit, mention the feature second. "Know who's paid without opening a spreadsheet" > "Payment tracking dashboard".

### Objection-killer section / FAQ (5–7 questions)
Pull from the real objections of this category. Always include: "What happens when my trial ends?", "Can I cancel?", "Is my data safe?", "Does it work with <the tool they already use>?", and one about price.

### Pricing (if on the same page)
- Anchor the recommended plan visually.
- Each plan: who it's for in one line, then features.
- Yearly toggle with the discount shown as "2 months free", not "17% off".
- Under the plans: refund policy in one line, link to it.

### Final CTA
Repeat the headline promise, one line, the primary CTA, the friction-removal line.

## Step 3 — Ship it
Write the copy into the actual components. Keep the existing design system. Replace lorem ipsum and placeholder headlines. Leave `{/* TODO: screenshot */}` markers where images are needed, and list them for the user at the end.

## Style rules
- Second person. Present tense. Short sentences.
- Numbers over adjectives. "3 days" beats "fast".
- One idea per sentence. One CTA per screen.
- No exclamation points. No emoji in headlines.
- Read every headline aloud; if it sounds like a press release, rewrite it.

## Output
The page files edited, plus a 10-line summary: headline chosen (and the two alternatives), the proof used, and the screenshots the user still needs to add.
