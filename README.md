# Arcady Media: Free Email Audit Funnel

Test assignment: a lead capture system for Arcady Media's free email audit offer for e-commerce brands.

## Funnel
`/` landing page (opt-in form) → `/thank-you/` (next steps + trust proof)

**Landing page:** headline + subheadline · 3 value props · risk-reversal line · opt-in form (name, email, store URL, monthly revenue band, biggest email challenge) · client logos · 4 result stats · "Six areas we check" · 3-step how it works · testimonials (verbatim from arcadymedia.com) · FAQ · final CTA.

**Thank-you page:** personalised headline (first name), summary chips (store / revenue / challenge), 3 next steps (audit starts today → audit arrives within 5 business days → optional walkthrough call via Arcady's Calendly), trust block (4 stats + 2 testimonials), link to their 58 case studies.

## VSL funnel, `/vsl/`
`/vsl/` → "See If You Qualify" opens a full-screen application, one question per screen (`assets/apply.js`, Netlify form `vsl-application`): store URL → biggest scaling bottleneck → monthly revenue → email challenge → name → email → phone. Letter keys pick answers, Enter continues, back arrow bottom right. UTMs are saved with the entry. →
- **$30K+/mo** → `/vsl/book/` (Arcady's Calendly embedded, prefilled with name + email) → once booked, the page sends them to `/vsl/confirmation/` (confirmation video + 3 prep steps + proof). No Calendly redirect setting needed.
- **Under $30K** → `/thank-you/` (they still get the audit).

VSL page sections: qualifier pill · headline · sub with risk reversal · mechanism line (ads vs email) · **VSL placeholder** · CTA · logo marquee · By the Numbers (4) · **6 video testimonial placeholders** · review cards (verbatim quotes) · FAQ (6) · final CTA · footer disclaimer.
Direct link that opens the pop-up: `/vsl/#apply`.

**Placeholders to fill:** VSL (`vsl/index.html`), 6 video testimonials + their quote / name / brand, confirmation video (`vsl/confirmation/index.html`). Each is marked with an HTML comment.

## Project hub, `/hub/`
A presentation page for the Loom walkthrough: sidebar with every page (landing page, thank-you, VSL, application, book, confirmation), the email sequence slot (next deliverable) and the VSL script. Pages load live on the right with a desktop/mobile switch. Each item has its own link, e.g. `/hub/#vsl`, `/hub/#emails`, `/hub/#vsl-script`. Marked noindex.
The 3 follow-up emails are copied from `emails/public/` into `site/emails/`. After re-running `emails/build.py`, copy them across again.

## Ads
- `Meta Ad Copy - Free Email Audit.md` (source) and `site/docs/ad-copy.html` (page with feed previews, headline/description switcher, copy buttons). Served at `/docs/ad-copy.html`, linked in the hub under Ads.
- `Ad Creatives - Video Scripts & Image Concepts.md` (source) and `site/docs/video-scripts.html` (both video scripts with animated 9:16 frame previews). Image ads have a hub view (`/hub/#image-ads`) with two empty 4:5 slots; drop the images into `site/assets/ads/` and swap each `.img-frame` placeholder for an `<img>`.

- `Meta Campaign Plan - Targeting, Structure & Tracking.md` (source) and `site/docs/campaign-plan.html`: targeting, 3-phase campaign structure, pixel + Conversions API events, GHL pipeline. Linked in the hub under Ads.

## Scripts
- `VSL Script - Free Email Audit.md` (source) and `site/docs/vsl-script.html` (page with teleprompter mode, ad-cut filter, print). Served at `/docs/vsl-script.html`.

## Tech
- Static HTML/CSS/JS in `site/`, no build step. Brand: Arcady blue #5176F9, navy #141722, Urbanist (Tangier, their display font, isn't public).
- Form posts to **Netlify Forms** (form name `email-audit`, honeypot `company_website`). Submissions show in Netlify → Forms. On localhost the POST is skipped and you go straight to the thank-you page.
- On submit, a `dataLayer` event `audit_optin` is pushed (ready for pixel / GTM later).

## Run locally
```
cd site && python3 -m http.server 4180
```
Open http://localhost:4180/

## Deploy (Netlify)
Repo: https://github.com/shawalnazir/arcady-email-audit (private, branch `main`).
In Netlify: **Add new site → Import an existing project → GitHub → arcady-email-audit**. No build command needed; `netlify.toml` at the root publishes the `site/` folder and sets the headers. Turn on form detection in **Site configuration → Forms** so the `email-audit` and `vsl-application` forms collect entries.

## Klaviyo hookup (to do)
Send each form submission to the Klaviyo list "Email Audit Requests" with these profile properties (exact names and values are in `03-follow-up-emails.md`, section 2): `first_name`/`last_name` (split from `name`), `store_url`, `monthly_revenue`, `email_challenge`, plus `bottleneck`, `phone`, `qualified` from the VSL application. Then paste the HTML from `emails/klaviyo/` into the 3 flow emails.

## Assumptions to confirm
- Audit delivery time "within 5 business days" and format (recorded video + prioritized fix list) were set by us.
- Outside-in audit ("no logins needed"), with read-only Klaviyo access optional.
- Revenue bands: Under $30K, $30K–$100K, $100K–$250K, $250K–$500K, $500K–$1M, $1M+.
- No confirmation email is sent yet (comes with the email / CRM deliverables).
