---
name: prelaunch-qa
description: Run a full pre-launch audit on a web app before it goes public. Use when the user says "am I ready to launch", "pre-launch check", "audit my app before launch", "what am I missing before shipping", or asks for a launch checklist. Produces a scored report with blockers, fixes, and a go/no-go verdict.
---

# Pre-Launch QA

You are the last reviewer before real users and real money hit this app. Be blunt. A founder who ships with a broken password reset loses more than one who ships a day late.

## Procedure

1. **Map the app first.** Read the repo structure, the framework, the auth provider, the payment provider, the DB, and the deploy target. Do not audit from assumptions. Write a 5-line summary of the stack before any findings.
2. **Walk every section below against the actual code.** For each item, mark it PASS / FAIL / N/A / UNVERIFIED (couldn't check from code alone — tell the user how to check manually).
3. **Score it.** Blockers are FAILs in sections marked 🔴. Anything else is a warning. Sections that don't apply (no auth, no payments) are N/A, not PASS — and if a 🔴 section is N/A because the feature is *missing* rather than *not needed*, say which.
   Also check: `git remote -v` — if the repo was ever pushed to a public remote with a secret in history, say so.
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
- `.env*` in `.gitignore`.
- Scan source AND history for committed secrets: `git grep -nE 'sk_live|sk_test|AKIA|-----BEGIN|api[_-]?key\s*[:=]\s*["\x27][A-Za-z0-9]' $(git rev-list --all) | head`. A hit in any commit is a blocker even if the current file is clean — the key is burned.
- If a live key is found: the first fix is **rotate it in the provider's dashboard now**, before removing it from code. Say this explicitly.
- Every secret the code reads is documented in `.env.example`.
- No secrets reachable from the browser: grep client-side source and any build output for `sk_`, `secret`, `key=`.

### 🔴 Data
- Backups exist and have been restored at least once. This is always UNVERIFIED from code — list it under manual checks, not as a FAIL.
- If the app has no persistence at all and the product clearly needs it, that's a blocker: say so under Data.
- Users can delete their account and data (GDPR/CCPA baseline).
- DB has unique constraints on email and any natural keys.

### 🟡 Error handling
- Global error boundary / 500 page that doesn't leak stack traces.
- 404 page.
- Server errors are logged somewhere a human will see (Sentry, Logtail, even email).
- Forms show validation errors inline, not as alerts.

### 🟡 Performance & reliability
- Flag images without width/height, uncompressed hero images (>300KB), render-blocking scripts in `<head>`, missing viewport meta. Don't invent a Lighthouse score; tell the user to run it.
- Security headers: CSP, HSTS, X-Frame-Options present (check framework config or hosting headers file).
- User input rendered to the page uses safe APIs (textContent / framework escaping), never raw innerHTML with user strings.
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
