---
name: prelaunch-qa
description: Run a full pre-launch audit on a web app before it goes public. Use when the user says "am I ready to launch", "pre-launch check", "audit my app before launch", "what am I missing before shipping", or asks for a launch checklist. Produces a scored report with blockers, fixes, and a go/no-go verdict.
---

# Pre-Launch QA

You are the last reviewer before real users and real money hit this app. Be blunt. A founder who ships with a broken password reset loses more than one who ships a day late.

## Procedure

1. **Map the app first.** Read the repo structure, the framework, the auth provider, the payment provider, the DB, and the deploy target. Do not audit from assumptions. Write a 5-line summary of the stack before any findings.
2. **Walk every section below against the actual code.** For each item, mark it PASS / FAIL / N/A / UNVERIFIED (couldn't check from code alone — tell the user how to check manually).
3. **Score it.** Blockers are FAILs in sections marked 🔴. Anything else is a warning.
4. **Write the report** in the format at the bottom. Blockers first, then warnings, then passes collapsed into one line.
5. **Offer to fix.** For each blocker, state the exact file and change. Ask before editing.

## Audit sections

### 🔴 Auth & accounts
- Sign-up, sign-in, sign-out all work; errors shown to the user are human-readable.
- Password reset flow exists end-to-end (request → email → new password → login).
- Email verification if the product sends email to users.
- Session expiry is set; logged-out users can't reach protected routes (check middleware/route guards, not just UI).
- No test accounts, hardcoded credentials, or `admin/admin` in the codebase.

### 🔴 Payments
- Webhook endpoint verifies signatures. Grep for the verify call — if it's missing, this is a blocker.
- Subscription state is read from the DB, not from a client-side flag.
- Failed payment / past_due / canceled states are handled (what does the user see?).
- Test-mode keys are not in production env; live keys are not in the repo.
- Refund path exists, even if manual.

### 🔴 Secrets & env
- `.env*` in `.gitignore`. Run `git log --all -p -- .env` to confirm nothing was ever committed.
- Every secret the code reads is documented in `.env.example`.
- No API keys in client bundles (grep built output for `sk_`, `secret`, `key=`).

### 🔴 Data
- Backups exist and have been restored at least once. If UNVERIFIED, make it the first manual task.
- Users can delete their account and data (GDPR/CCPA baseline).
- DB has unique constraints on email and any natural keys.

### 🟡 Error handling
- Global error boundary / 500 page that doesn't leak stack traces.
- 404 page.
- Server errors are logged somewhere a human will see (Sentry, Logtail, even email).
- Forms show validation errors inline, not as alerts.

### 🟡 Performance & reliability
- Lighthouse mobile score estimate; flag images without dimensions, unoptimized hero images, render-blocking scripts.
- Rate limiting on auth and any public POST endpoint.
- Health check route for uptime monitoring.

### 🟡 Legal & trust
- Privacy policy and terms linked in footer and at sign-up.
- Contact email that a human reads.
- Cookie consent if using analytics in EU-reachable markets.

### 🟡 Launch surface
- OG image and meta description on every public page.
- Favicon, app title, 'title' tags not "Create Next App".
- Pricing page states what happens at the end of a trial.
- Transactional emails (welcome, receipt, reset) have been sent to a real inbox and read on a phone.

## Report format

```
# Pre-Launch Audit — <app name>
Stack: <5 lines>
Verdict: GO / NO-GO (<n> blockers)

## Blockers
1. <section> — <what's wrong> — <file:line> — <fix in one sentence>

## Warnings
- ...

## Manual checks you must do yourself
- ...

## Passed
<comma-separated list>
```

Keep the report under 60 lines. Founders skim. Put the worst thing first.
