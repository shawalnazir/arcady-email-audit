# Arcady Media: Free Email Audit Follow-Up Sequence

**Platform:** Klaviyo. Arcady is a Klaviyo partner, so the sequence runs on the same platform it would build for clients.
**Goal:** get a call booked for every audit request within 48 hours of the request.
**Sequence:** 3 emails. Email 1 goes out the moment the form is submitted, email 2 at +24h and email 3 at +48h. Anyone who books leaves the flow straight away.

---

## 1. What's working, and how it shaped this sequence

| Finding | What it means for these emails |
|---|---|
| Replying within 5 minutes makes contact far more likely than replying at 30 minutes. The usual figures are 21x more qualified leads and up to 100x more contacts. They're widely repeated vendor numbers, so treat them as direction, not fact. | Email 1 is a booking email, not a thank-you. The booking link is the first thing they see while their intent is highest. |
| The standard follow-up pattern that works is: confirm, then give value without a pitch, then make a clear ask. | Email 1 confirms the audit has started and books the walkthrough. Email 2 teaches (the 3 leaks) and shows proof. Email 3 handles objections and makes the last ask. |
| Plain-text emails from a real person get far more replies than designed emails when the goal is a conversation. Practitioner estimates run 4–9x, which is directional. | All three emails are written as plain text from a named strategist, with one link and a reply-to inbox someone reads. Each email offers a reply as a second way to respond. |
| Making the prospect take one small step cuts no-shows from curiosity bookings. Asking for a reply is the simplest version. | The P.S. in each email asks for a reply. Email 3 offers a "later" reply so the lead isn't lost. |
| Personalising to what the lead told you lifts conversion. | The form's "biggest email challenge" answer drives a different paragraph in email 1, and the revenue band drives a line in email 3. |
| Klaviyo 2026 benchmarks (183,000+ brands): flows bring in about **41% of email revenue from 5.3% of sends**. Flow click rate is 5.58% vs 1.69% for campaigns. | This is the hook in emails 1 and 2. Most stores under-build flows, and this figure gives them a reason to want the audit. |

---

## 2. Klaviyo setup

**Trigger:** the profile is added to the list **"Email Audit Requests"** by either form (opt-in page or VSL application). The form saves these profile properties, with the **exact** values below, because the conditional blocks check them:
- `first_name` (and `last_name`): split from the form's `name` field when the lead is sent to Klaviyo
- `store_url`
- `monthly_revenue`, with these options:
  - Under $30K
  - $30K – $100K
  - $100K – $250K
  - $250K – $500K
  - $500K – $1M
  - $1M+
- `email_challenge`, with these options:
  - Email drives too little of our revenue
  - Flows are missing or out of date
  - Low open rates or landing in spam
  - Our list isn't growing
  - We rely too much on discounts
  - No time or team to run it (opt-in page only)
  - We don't send email yet
  - Something else
- VSL application only: `bottleneck`, `phone`, `qualified`
- UTM fields

**Flow filter:** `audit_call_booked` is not equal to `true`. Klaviyo checks flow filters before every step, so anyone who books stops getting emails.

**Booking signal:** a Calendly "Invitee Created" webhook goes to Zapier or Make, which:
- sets `audit_call_booked = true` on the profile
- tracks a "Booked Audit Call" metric

```
Form submit → Added to "Email Audit Requests"
   │
   ├─ Email 1: audit started + book the walkthrough (send immediately, Smart Sending OFF)
   ├─ Internal alert (conditional split: monthly_revenue = $250K – $500K, $500K – $1M or $1M+)
   │     → email to Tarun's inbox: "High-value audit request: {{ store_url }}"
   │
   ├─ Wait 1 day
   ├─ Email 2: the 3 leaks + proof (only if not booked)
   │
   ├─ Wait 1 day
   ├─ Email 3: objections + last ask (only if not booked)
   │
   └─ Exit. Not booked → monthly newsletter, but only if they ticked the marketing consent box
```

**The offer, as the emails describe it** (matches the landing pages, ads and VSL): the audit starts the day they request it, the recorded video walkthrough and fix list arrive within 5 business days, and the call is a 30-minute walkthrough of the findings. The emails drive to booking that call.

**Sending details**
- **From:** "Tarun at Arcady Media" (tarun@arcadymedia.com). Replies go to Tarun, not a no-reply address.
- **Template:** Klaviyo text-only template. No header image and no logo bar, so it reads like a personal email.
- **Booking link:** `https://calendly.com/arcady-media/intro-strategy-call?name={{ first_name|urlencode }}&email={{ email|urlencode }}&a1={{ person|lookup:'store_url'|urlencode }}&utm_source=klaviyo&utm_campaign=email-audit&utm_content=e1` (e2 and e3 in the later emails)
- **Main KPI:** booked-call rate (bookings ÷ audit requests). Clicks come second. Ignore opens, because Apple Mail Privacy Protection inflates them.
- **Compliance:**
  - One-click unsubscribe and the company address go in the footer, as Gmail and Yahoo now require.
  - Add an unticked "Send me Arcady's email tips" consent box to the form, so leads can move into the newsletter afterwards (CASL/GDPR).

**After booking (separate flow, outside this brief):**
- confirmation with a reply-to-confirm ask
- reminder at 24h
- reminder at 1h

---

## 3. The emails

The full HTML for each email is generated by `emails/build.py` (`emails/klaviyo/` for Klaviyo, `emails/public/` for previews). The copy below matches it.

### Email 1: Immediate confirmation

**Send:** straight away when the form is submitted.
**Subject:** Got your audit request for {{ person|lookup:'store_url' }}
**A/B subject:** {{ first_name|default:'Hey' }}, your email audit is one step away
**Preview text:** Your audit has started. Here's what happens next.

> Hi {{ first_name|default:'there' }},
>
> Thanks for requesting a free email audit for {{ person|lookup:'store_url' }}. It's already started.
>
> Here's how it works:
>
> 1. **Today, we go through your store as a customer would.** We sign up, browse, leave a cart and see what lands in our inbox (and when). We also check your sending setup.
> 2. **Within 5 business days, you get your audit:** a recorded video walkthrough and a fix list, ranked by how much revenue each fix is worth.
> 3. **Then we walk you through it on a 30-minute call:** the three changes we'd make first and what they're worth. You keep everything whether or not we work together.
>
> **[Book your audit call →]({{ booking_link }})**
>
> *(One paragraph based on `email_challenge`:)*
> - **Email drives too little of our revenue:** You said email drives too little of your revenue. That's usually a flows problem, not a campaigns problem. Across Klaviyo's 183,000+ brands, automated flows bring in about 41% of email revenue from just 5% of sends. Your audit shows which of your flows are missing or underperforming.
> - **Flows are missing or out of date:** You said your flows need work. We'll start with the four that usually hold the most money: welcome, abandoned cart, browse abandonment and post-purchase.
> - **Low open rates or landing in spam:** You said deliverability is a problem. We'll check your authentication (SPF, DKIM, DMARC), how much and how often you send, and how clean your list is, before anything else.
> - **Our list isn't growing:** You said your list isn't growing. We'll look at your sign-up pop-up, the offer behind it, and what a new subscriber gets in their first week.
> - **We rely too much on discounts:** You said you lean on discounts. We'll show you where flows and better offers can do that job instead, so you protect your margin.
> - **No time or team to run it:** You said you don't have the time or team for email. That's fine. The audit needs nothing from you, and the walkthrough call is 30 minutes.
> - **We don't send email yet:** You said you don't send email yet. Good news: your fix list becomes a build list, with the flows that make the most money first.
> - **Anything else:** Your audit covers your flows, campaigns, list growth and deliverability, so you'll see where the biggest gains are.
>
> Pick any slot from next week on, so your audit is ready before we talk.
>
> Talk soon,
> Tarun
> Founder & CEO, Arcady Media
>
> P.S. None of the times work? Reply with two times that suit you and we'll make one of them happen.

---

### Email 2: Value + proof

**Send:** 1 day after email 1, only if they haven't booked.
**Subject:** The 3 leaks we find in most email audits
**A/B subject:** Where {{ person|lookup:'store_url' }} is leaving email revenue
**Preview text:** None of them need more ad spend to fix.

> Hi {{ first_name|default:'there' }},
>
> While we work on your audit, here's a preview. These are the three leaks we find most often when we open up a store's email:
>
> **1. The welcome flow is one email.** A discount code, then nothing. That's the moment a new subscriber is most interested, and most brands stop talking to them.
>
> **2. Abandoned cart goes out once, or too late.** One reminder a day later catches only a fraction of carts. A short series that starts within the hour catches far more.
>
> **3. Nothing happens after the first order.** No thank-you, no "how to use it", no reminder to reorder. So all of the email revenue depends on campaigns and discounts.
>
> Fixing these doesn't need more traffic or more ad spend. It turns the customers you already paid for into more revenue. That's how flows make about 41% of email revenue from just 5% of the emails sent (Klaviyo's 2026 benchmarks).
>
> Here's what it looks like when the fixes are done properly:
>
> - **Enhanced Scents** went from $200K to $1.2M a month.
> - **Spornia** tripled its repeat purchase rate and made $639K from email.
>
> Your audit will show which of these leaks {{ person|lookup:'store_url' }} has. On the call, we'll walk you through what fixing each one is worth.
>
> **[Book your audit call →]({{ booking_link }})**
>
> Tarun
> Founder & CEO, Arcady Media
>
> P.S. Curious which leak you have? Reply "which one" and I'll tell you the first thing I noticed on your site.

---

### Email 3: Objections + last ask

**Send:** 1 day after email 2 (48h after the request), only if they haven't booked.
**Subject:** Should I keep a call slot for your audit?
**A/B subject:** {{ first_name|default:'Quick one' }}, still want your audit?
**Preview text:** No pressure either way. Just let me know.

> Hi {{ first_name|default:'there' }},
>
> I haven't seen a booking for your audit walkthrough, so I'll keep this short. These are the questions people usually ask before they book:
>
> **"Is this a sales call in disguise?"**
> It's an audit first. You get the video and the fix list either way, and you can make the changes yourself. On the call we walk you through the findings. If you'd like help after that, we'll talk about it. If not, that's fine.
>
> **"Do I need to give you access to Klaviyo?"**
> No. We do the audit from the outside, as a customer would. If you want us to go deeper, you can share your screen on the call.
>
> **"Is my store big enough?"**
> {% if person|lookup:'monthly_revenue' == 'Under $30K' %}
> At your stage, a few well-built flows can make a real difference. If email isn't the right lever yet, we'll tell you straight.
> {% else %}
> Yes. At {{ person|lookup:'monthly_revenue' }} a month, small gains in flow performance add up to real money.
> {% endif %}
>
> Brands that have done this with us say it better than I can. Tanoa's marketing director: "We thought retail was our best channel until we doubled our online revenue in the first 60 days with Arcady Media."
>
> If you'd like us to walk you through it, here's the link:
>
> **[Book your audit call →]({{ booking_link }})**
>
> If now's not the time, reply "later" and I'll check back next month. Either way, your video and fix list are still on their way.
>
> Tarun
> Founder & CEO, Arcady Media

**Replies to handle (by hand, from the reply-to inbox):**
- **"later":** tag `audit_later` and set a 30-day check-in.
- **"which one":** reply personally within the working day with one real observation from the store.
- **Two times offered:** book it in Calendly for them and confirm.

---

## 4. Check before sending
- **Enhanced Scents "$200K → $1.2M a month"** comes from their case-study card. Confirm whether it's email revenue or total store revenue, and adjust the line to match.
- **Tanoa quote:** now verbatim from the testimonial on arcadymedia.com.
- **Audit process:** the emails promise an outside-in audit for every request (sign up, browse, abandon a cart, check DNS authentication) and a video + fix list within 5 business days. The team needs to actually deliver this for every request, booked or not.
- **Call length:** set to 30 minutes. Change it in email 1 if the Calendly event is different.
- **Form values:** the `email_challenge` and `monthly_revenue` options must match section 2 exactly (they currently do), or the conditional blocks fall through to the default text.

---

## Sources
- [Klaviyo email benchmarks (2026, 183,000+ customers)](https://klaviyo.com/products/email-marketing/benchmarks)
- [Eightx: Klaviyo flow revenue contribution benchmarks](https://eightx.co/blog/average-klaviyo-flow-revenue-contribution-benchmarks)
- [Kixie: speed-to-lead statistics](https://www.kixie.com/sales-blog/speed-to-lead-response-time-statistics-that-drive-conversions/) · [Teamgate: lead response time study](https://teamgate.com/blog/lead-response-time-study)
- [Keap: lead magnet follow-up automation](https://keap.com/business-success-blog/sales/lead-magnet-landing-page-automation) · [Woodpecker: lead magnet email sequence](https://woodpecker.co/blog/how-to-build-an-effective-lead-magnet-email-sequence/)
- [Databox: HTML vs plain text emails](https://databox.com/html-vs-plain-text-emails) · [Prospeo: cold email format (44M emails)](https://prospeo.io/s/cold-email-format)
- [SalesHive: reducing B2B meeting no-shows](https://saleshive.com/blog/how-to-reduce-b2b-meeting-no-shows)
