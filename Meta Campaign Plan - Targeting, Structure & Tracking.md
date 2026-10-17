# Meta Campaign Plan: Targeting, Structure & Tracking (Arcady Media)

How the free email audit ads run: who they target, how the campaigns are structured and scaled, which events go to Meta, and how leads flow into GoHighLevel (or any CRM).

---

## 1. Targeting

All ad sets: **United States, Canada, United Kingdom, Australia** · ages 25–65 · Advantage+ placements · English.
**Exclude in every ad set:** existing clients (customer list) and anyone who already submitted the form in the last 30 days (website custom audience on the Lead event).

### Ad set 1: Broad
No interests or lookalikes. The creative does the targeting: every ad calls out "e-commerce brands doing $30K+ a month" in the first line, so Meta learns who responds.

### Ad set 2: Interest stack (store owners + Shopify)
Business owners and store owners, narrowed to people interested in Shopify and e-commerce tools.

- **Include (any of):** Small business owners · Facebook Page admins (behaviour) · Business owner (job title, if available)
- **AND narrow to (any of):** Shopify · Klaviyo · E-commerce · WooCommerce · BigCommerce · Recharge · Online store / Dropshipping
- Meta renames and removes interests often, so check each one in Ads Manager when building.

### Ad set 3: Lookalike (from Arcady's prospect list)
- **Seed:** one combined customer list of everyone Arcady has spoken to: past leads, booked calls, proposals, current and past clients, newsletter subscribers. Upload with email, phone, name and country for the best match rate.
- **Size:** at least 1,000 people for a reliable lookalike (Meta's minimum is 100).
- **Lookalike:** 1–3% in each target country. If client revenue or LTV data is available, use a value-based lookalike so Meta weights the best clients more.
- **Later:** once the funnel has 100+ qualified leads or booked calls, build a second lookalike from those.

---

## 2. Campaign Structure

### Phase 1 · Days 1–10 · Campaign 1: Audience Test (ABO)

| | |
|---|---|
| **Objective** | Leads (website) |
| **Optimisation event** | Lead (every form submission) |
| **Budget** | Ad set budgets (ABO), $100/day each, $300/day total (~$3,000 over 10 days) |
| **Ad sets** | 1 Broad · 2 Interest stack · 3 Lookalike |
| **Ads in every ad set** | Video 1 (founder) · Video 2 (text on video) · Image 1 (hand card) · Image 2 (growth options) |
| **Copy** | Long-form and short-form primary text, split across the ads, with the 5 headlines and 5 descriptions as dynamic options |

**How to pick the winner on day 10:** lowest cost per lead, then the highest share of qualified leads ($30K+/month, the QualifiedLead event). A cheap lead from a store too small to qualify isn't a win. Turn off ads within the winning ad set that have spent 2–3x the target cost per lead with no leads.

### Phase 2 · Days 10–30 · Campaign 2: Scale

| | |
|---|---|
| **Objective** | Leads (website) |
| **Optimisation event** | Lead |
| **Budget** | The winning audience at $200/day (~$4,000 over 20 days) |
| **Ads** | All 4 ads, plus new variations of the best performer |

Raise the budget in steps of about 20% every 2–3 days rather than all at once, so the ad set doesn't drop back into learning.

### Phase 3 · From $500/day or 30–40 form submissions a week · Campaign 3: Call Booking Optimisation

| | |
|---|---|
| **Objective** | Leads (website) |
| **Optimisation event** | Schedule (a booked call) |
| **Budget** | Start at the same daily spend as the scaling campaign, then scale |
| **Why wait** | Meta needs enough booked calls to learn from (ideally ~50 a week per ad set). Before that, optimising for calls starves the algorithm. |

**Ongoing:** keep scaling the winners and launch new ads every 1–2 weeks (new hooks, new proof, new formats) to stop creative fatigue.

**Spend in the first 30 days:** about $7,000 (10 days × $300 + 20 days × $200).

---

## 3. Events Sent to Meta (Pixel + Conversions API)

Every event fires from the browser (pixel) **and** from the server (Conversions API), with the same `event_id` so Meta counts it once. The server copy still gets through when ad blockers or iOS privacy settings block the pixel.

| Event | When it fires | Pages | Used for |
|---|---|---|---|
| **PageView** | Every page load | All funnel pages | Retargeting audiences, funnel drop-off |
| **ViewContent** | The VSL page loads | `/vsl/` | Retargeting people who saw the offer but didn't apply |
| **Lead** | Any form is submitted (opt-in or VSL application) | `/`, `/vsl/` | **Optimisation in Phases 1–2.** Sent with `content_name` (opt-in or VSL application), revenue band and email challenge |
| **QualifiedLead** (custom) | The applicant says $30K+/month | `/`, `/vsl/` | Judging audience quality, a custom conversion to report on, and a lookalike seed later |
| **Schedule** | A call is booked | `/vsl/confirmation/` + booking webhook | **Optimisation in Phase 3** |
| **Purchase** (offline, from GHL or any CRM) | The opportunity is marked Won in GHL or any CRM | Server only | Shows which ads produce clients, not just leads. Sent with the deal value |

**Customer data sent with each event (hashed with SHA-256):** email, phone, first and last name, country, and an external ID, plus the `fbp` / `fbc` cookies, IP address and browser. More matching data means better attribution and better optimisation.

**Setup checks:** test every event with a Test Event Code in Events Manager before launch, then aim for an Event Match Quality of 7+ on Lead and Schedule.

---

## 4. CRM Integration (GoHighLevel or Any CRM)

Every submission goes into GHL, or whichever CRM Arcady uses (HubSpot, Pipedrive, Close, etc.), as a contact, so the team can see and work every lead in one place. GHL is the example below; the same setup works in any CRM.

**On form submit (both funnels):**
- **Create or update the contact** (matched on email): name, email, phone, store URL, monthly revenue, biggest scaling bottleneck, email challenge.
- **Tags:** `email-audit` · `qualified` or `unqualified` ($30K+/month or not) · `funnel-optin` or `funnel-vsl`
- **Note** on the contact with every answer and the UTM source, campaign and ad, so the team knows which ad brought them in.
- **Opportunity** in an "Email Audit" pipeline (in GHL or any CRM):

| Stage | Who lands here |
|---|---|
| New Request | Everyone, on submit |
| Qualified | $30K+/month |
| Audit Only | Under $30K (they still get the audit) |
| Call Booked | After booking |
| Audit Delivered | Once the video and fix list are sent |
| Proposal Sent | After the walkthrough call |
| Won / Lost | Outcome. **Won sends the offline Purchase event to Meta** (GHL workflow, or the CRM's Meta integration / Zapier) |

**On booking:** tag `call-booked` and move the opportunity to Call Booked. If the booking calendar moves into GHL (or the CRM's own calendar), this happens automatically. If Calendly stays, a Calendly webhook does it.

**GHL workflows (or the CRM's automations):**
- An internal alert to the team for every qualified lead (and a priority alert for $250K+/month stores).
- Call reminders by email and SMS: 24 hours and 1 hour before.
- The Meta Conversions API action on "Opportunity Won", which sends the offline Purchase event (in another CRM: its Meta integration or a Zapier/Make step).

**Emails:** the 3-email follow-up sequence runs in Klaviyo, as built. The form sends the lead to Klaviyo and the CRM at the same time: Klaviyo handles nurture emails, GHL (or the CRM) handles the pipeline, booking and reminders. Anyone tagged `call-booked` leaves the Klaviyo sequence.
