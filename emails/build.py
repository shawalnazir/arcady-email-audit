"""Build the 3 audit follow-up emails.

Outputs:
  klaviyo/email-N.html  full email HTML with Klaviyo tags (paste into a Klaviyo HTML template)
  preview/email-N.html  artifact preview (email only, sample data)
  public/email-N.html   standalone page for GitHub Pages (github.com/shawalnazir/arcady-emails)

Run: python3 build.py   (copy source: ../03-follow-up-emails.md)
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).parent

# Sample data for the previews
SAMPLE = {
    "first_name": "Alex",
    "store_url": "yourstore.com",
    "email_challenge": "Email drives too little of our revenue",
    "revenue_band": "$30K – $100K",
}

BOOK = ("https://calendly.com/arcady-media/intro-strategy-call?name={{ first_name|urlencode }}"
        "&email={{ email|urlencode }}&a1={{ person|lookup:'store_url'|urlencode }}"
        "&utm_source=klaviyo&utm_campaign=email-audit&utm_content=")

# Tokens: (klaviyo, preview)
T = {
    "name": ("{{ first_name|default:'there' }}", SAMPLE["first_name"]),
    "store": ("{{ person|lookup:'store_url' }}", SAMPLE["store_url"]),
    "band": ("{{ person|lookup:'monthly_revenue' }}", SAMPLE["revenue_band"]),
}

FONT = "Urbanist, 'Helvetica Neue', Helvetica, Arial, sans-serif"
INK, TEXT, MUTED, BLUE, LINE = "#141722", "#363635", "#6b6b6b", "#5176F9", "#e9e9e9"
P = f"margin:0 0 18px;font-family:{FONT};font-size:16px;line-height:1.65;color:{TEXT};"


def sub(s, mode):
    i = 0 if mode == "k" else 1
    for k, v in T.items():
        s = s.replace("[[" + k + "]]", v[i])
    return s


def p(text):
    return f'<p style="{P}">{text}</p>'


def b(text):
    return f'<strong style="color:{INK};">{text}</strong>'


def button(label, utm, mode):
    href = html.escape(BOOK + utm, quote=False) if mode == "k" else "#"
    return (
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:6px 0 26px;">'
        f'<tr><td align="center" bgcolor="{BLUE}" style="border-radius:999px;">'
        f'<a href="{href}" target="_blank" style="display:inline-block;padding:15px 30px;font-family:{FONT};'
        f'font-size:16px;font-weight:700;color:#ffffff;text-decoration:none;border-radius:999px;">{label} &rarr;</a>'
        '</td></tr></table>'
    )


def steps(items):
    rows = ""
    for n, (title, body) in enumerate(items, 1):
        rows += (
            '<tr><td valign="top" style="padding:0 14px 16px 0;width:28px;">'
            f'<div style="width:28px;height:28px;line-height:28px;border-radius:50%;background:{INK};color:#ffffff;'
            f'text-align:center;font-family:{FONT};font-size:13px;font-weight:700;">{n}</div></td>'
            f'<td valign="top" style="padding:3px 0 16px;font-family:{FONT};font-size:16px;line-height:1.6;color:{TEXT};">'
            f'{b(title)} {body}</td></tr>'
        )
    return f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 10px;">{rows}</table>'


def callout(inner):
    return (
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 22px;">'
        f'<tr><td style="background:#eef2ff;border-radius:12px;padding:18px 20px;font-family:{FONT};font-size:15.5px;'
        f'line-height:1.6;color:{TEXT};">{inner}</td></tr></table>'
    )


def conditional(prop, branches, default, sample_value, mode, wrap=lambda x: x):
    """branches: list of (value, text). Klaviyo gets if/elif/else, preview gets the sample's branch."""
    if mode == "p":
        for v, t in branches:
            if v == sample_value:
                return wrap(t)
        return wrap(default)
    out = ""
    for i, (v, t) in enumerate(branches):
        kw = "if" if i == 0 else "elif"
        out += f'{{% {kw} person|lookup:\'{prop}\' == "{v}" %}}{wrap(t)}'
    return out + f"{{% else %}}{wrap(default)}{{% endif %}}"


PHOTO_K = "[TARUN_PHOTO_URL]"  # upload img/tarun.png to Klaviyo's image library and paste its URL here
ADDRESS = "292 Adelaide St W, Suite 600, Toronto, ON M5V 1P6, Canada"
MAPS = "https://maps.google.com/?q=292+Adelaide+St+W+Suite+600+Toronto+ON+M5V+1P6"


def photo_src(mode):
    if mode == "k":
        return PHOTO_K
    import base64
    return "data:image/png;base64," + base64.b64encode((HERE / "img" / "tarun.png").read_bytes()).decode()


def signoff(lead="Talk soon,", mode="k"):
    lead_html = f"{lead}<br>" if lead else ""
    s = f"font-family:{FONT};font-size:13.5px;line-height:1.55;"
    return (
        p(f"{lead_html}Tarun<br><span style=\"color:{MUTED};\">Founder &amp; CEO, Arcady Media</span>")
    )


def ps(text):
    return (f'<p style="margin:8px 0 0;padding-top:18px;border-top:1px solid {LINE};font-family:{FONT};'
            f'font-size:15px;line-height:1.6;color:{MUTED};">{b("P.S.")} {text}</p>')


def faq(q, a):
    return (f'<p style="margin:0 0 6px;font-family:{FONT};font-size:16px;font-weight:700;color:{INK};">{q}</p>'
            f'<p style="{P}">{a}</p>')


# ---------- Email bodies ----------

# Keys match the form's "Biggest email challenge" options exactly (site/index.html, site/assets/apply.js)
CHALLENGES = [
    ("Email drives too little of our revenue", "You said email drives too little of your revenue. That's usually a flows problem, not a campaigns problem. Across Klaviyo's 183,000+ brands, automated flows bring in about <strong>41% of email revenue from just 5% of sends</strong>. Your audit shows which of your flows are missing or underperforming."),
    ("Flows are missing or out of date", "You said your flows need work. We'll start with the four that usually hold the most money: welcome, abandoned cart, browse abandonment and post-purchase."),
    ("Low open rates or landing in spam", "You said deliverability is a problem. We'll check your authentication (SPF, DKIM, DMARC), how much and how often you send, and how clean your list is, before anything else."),
    ("Our list isn't growing", "You said your list isn't growing. We'll look at your sign-up pop-up, the offer behind it, and what a new subscriber gets in their first week."),
    ("We rely too much on discounts", "You said you lean on discounts. We'll show you where flows and better offers can do that job instead, so you protect your margin."),
    ("No time or team to run it", "You said you don't have the time or team for email. That's fine. The audit needs nothing from you, and the walkthrough call is 30 minutes."),
    ("We don't send email yet", "You said you don't send email yet. Good news: your fix list becomes a build list, with the flows that make the most money first."),
]
CHALLENGE_DEFAULT = "Your audit covers your flows, campaigns, list growth and deliverability, so you'll see where the biggest gains are."


def email1(mode):
    return "".join([
        p("Hi [[name]],"),
        p("Thanks for requesting a free email audit for [[store]]. It's already started."),
        p("Here's how it works:"),
        steps([
            ("Today, we go through your store as a customer would.", "We sign up, browse, leave a cart and see what lands in our inbox (and when). We also check your sending setup."),
            ("Within 5 business days, you get your audit:", "a recorded video walkthrough and a fix list, ranked by how much revenue each fix is worth."),
            ("Then we walk you through it on a 30-minute call:", "the three changes we'd make first and what they're worth. You keep everything whether or not we work together."),
        ]),
        button("Book your audit call", "e1", mode),
        conditional("email_challenge", CHALLENGES, CHALLENGE_DEFAULT, SAMPLE["email_challenge"], mode, wrap=callout),
        p("Pick any slot from next week on, so your audit is ready before we talk."),
        signoff(mode=mode),
        ps("None of the times work? Reply with two times that suit you and we'll make one of them happen."),
    ])


def leak(n, title, body):
    return (
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 12px;">'
        f'<tr><td style="border:1px solid {LINE};border-radius:12px;padding:16px 18px;font-family:{FONT};font-size:15.5px;line-height:1.6;color:{TEXT};">'
        f'<div style="font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{BLUE};margin-bottom:4px;">Leak {n}</div>'
        f'{b(title)} {body}</td></tr></table>'
    )


def stat(num, label):
    return (f'<td valign="top" width="50%" style="padding:16px 18px;background:#f3f3f3;border-radius:12px;font-family:{FONT};">'
            f'<div style="font-size:24px;font-weight:800;color:{INK};letter-spacing:-.02em;line-height:1.1;">{num}</div>'
            f'<div style="margin-top:6px;font-size:14px;line-height:1.5;color:{TEXT};">{label}</div></td>')


def email2(mode):
    return "".join([
        p("Hi [[name]],"),
        p("While we work on your audit, here's a preview. These are the three leaks we find most often when we open up a store's email:"),
        leak(1, "The welcome flow is one email.", "A discount code, then nothing. That's the moment a new subscriber is most interested, and most brands stop talking to them."),
        leak(2, "Abandoned cart goes out once, or too late.", "One reminder a day later catches only a fraction of carts. A short series that starts within the hour catches far more."),
        leak(3, "Nothing happens after the first order.", "No thank-you, no “how to use it”, no reminder to reorder. So all of the email revenue depends on campaigns and discounts."),
        '<div style="height:10px;line-height:10px;">&nbsp;</div>',
        p("Fixing these doesn't need more traffic or more ad spend. It turns the customers you already paid for into more revenue. That's how flows make about 41% of email revenue from just 5% of the emails sent (Klaviyo's 2026 benchmarks)."),
        p("Here's what it looks like when the fixes are done properly:"),
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 22px;border-collapse:separate;border-spacing:0;">'
        '<tr>' + stat("$200K &rarr; $1.2M", "a month for Enhanced Scents") + '<td width="12" style="width:12px;">&nbsp;</td>'
        + stat("3x repeat rate", "and $639K from email for Spornia") + '</tr></table>',
        p("Your audit will show which of these leaks [[store]] has. On the call, we'll walk you through what fixing each one is worth."),
        button("Book your audit call", "e2", mode),
        signoff(lead="", mode=mode),
        ps("Curious which leak you have? Reply “which one” and I'll tell you the first thing I noticed on your site."),
    ])


BANDS_SMALL = [("Under $30K", "At your stage, a few well-built flows can make a real difference. If email isn't the right lever yet, we'll tell you straight.")]
BAND_DEFAULT = "Yes. At [[band]] a month, small gains in flow performance add up to real money."


def email3(mode):
    band_text = conditional("monthly_revenue", BANDS_SMALL, BAND_DEFAULT, SAMPLE["revenue_band"], mode)
    return "".join([
        p("Hi [[name]],"),
        p("I haven't seen a booking for your audit walkthrough, so I'll keep this short. These are the questions people usually ask before they book:"),
        faq("“Is this a sales call in disguise?”", "It's an audit first. You get the video and the fix list either way, and you can make the changes yourself. On the call we walk you through the findings. If you'd like help after that, we'll talk about it. If not, that's fine."),
        faq("“Do I need to give you access to Klaviyo?”", "No. We do the audit from the outside, as a customer would. If you want us to go deeper, you can share your screen on the call."),
        faq("“Is my store big enough?”", band_text),
        p(f"Brands that have done this with us say it better than I can. Tanoa's marketing director: {b('“We thought retail was our best channel until we doubled our online revenue in the first 60 days with Arcady Media.”')}"),
        p("If you'd like us to walk you through it, here's the link:"),
        button("Book your audit call", "e3", mode),
        p("If now's not the time, reply “later” and I'll check back next month. Either way, your video and fix list are still on their way."),
        signoff(lead="", mode=mode),
    ])


EMAILS = [
    dict(n=1, fn=email1, when="Sends immediately on form submit",
         subject="Got your audit request for [[store]]",
         ab="[[name_ab1]], your email audit is one step away",
         preheader="Your audit has started. Here's what happens next."),
    dict(n=2, fn=email2, when="Sends 24 hours later, only if no call is booked",
         subject="The 3 leaks we find in most email audits",
         ab="Where [[store]] is leaving email revenue",
         preheader="None of them need more ad spend to fix."),
    dict(n=3, fn=email3, when="Sends 48 hours after the request, only if no call is booked",
         subject="Should I keep a call slot for your audit?",
         ab="[[name_ab3]], still want your audit?",
         preheader="No pressure either way. Just let me know."),
]
T["name_ab1"] = ("{{ first_name|default:'Hey' }}", SAMPLE["first_name"])
T["name_ab3"] = ("{{ first_name|default:'Quick one' }}", SAMPLE["first_name"])


def shell(inner, preheader, mode):
    unsub = "{% unsubscribe 'Unsubscribe' %}" if mode == "k" else '<a href="#" style="color:#98989a;">Unsubscribe</a>'
    addr = "{{ organization.full_address }}" if mode == "k" else "Arcady Media, " + ADDRESS
    return (
        f'<div style="display:none;max-height:0;overflow:hidden;opacity:0;mso-hide:all;">{preheader}&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</div>'
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#f3f3f3" style="background:#f3f3f3;">'
        '<tr><td align="center" style="padding:32px 12px;">'
        '<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:#ffffff;border-radius:16px;">'
        '<tr><td style="padding:34px 40px 30px;" class="em-pad">'
        f'<div style="margin:0 0 26px;font-family:{FONT};font-size:17px;font-weight:800;letter-spacing:-.01em;color:{INK};">'
        f'<span style="color:{BLUE};">&#9679;</span>&nbsp;Arcady Media</div>'
        f'{inner}'
        '</td></tr></table>'
        f'<p style="margin:18px 0 0;font-family:{FONT};font-size:12px;line-height:1.6;color:#98989a;text-align:center;">'
        f'You&rsquo;re getting this because you requested a free email audit from Arcady Media.<br>{addr} &middot; {unsub}</p>'
        '</td></tr></table>'
    )


def klaviyo_doc(e):
    inner = sub(e["fn"]("k"), "k")
    pre = sub(e["preheader"], "k")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<title>{html.escape(sub(e['subject'], 'k'))}</title>
<link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;700;800&display=swap" rel="stylesheet">
<style>
  body {{ margin:0; padding:0; background:#f3f3f3; }}
  a {{ color:{BLUE}; }}
  @media (max-width:620px) {{ .em-pad {{ padding:28px 22px 24px !important; }} }}
</style>
</head>
<body>
{shell(inner, pre, "k")}
</body>
</html>
"""


def preview_page(e, klaviyo_html):
    inner = sub(e["fn"]("p"), "p")
    pre = sub(e["preheader"], "p")
    return f"""<title>Arcady Audit Email {e['n']}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;600;700;800&display=swap">
<style>
/* Layout: the email alone, exactly as it renders in an inbox */
:root {{ --bg: #f3f3f3; }}
body {{ background: var(--bg); }}
.mail {{ max-width: 680px; margin: 0 auto; }}
.mail table {{ max-width: 100%; }}
@media (max-width: 620px) {{ .mail td.em-pad {{ padding: 26px 20px !important; }} }}
</style>
<div class="mail">{shell(inner, pre, "p")}</div>
"""


def public_page(e):
    inner = sub(e["fn"]("p"), "p")
    pre = sub(e["preheader"], "p")
    subj = html.escape(sub(e["subject"], "p"))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{subj}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;600;700;800&display=swap">
<style>
  body {{ margin:0; background:#f3f3f3; }}
  .mail {{ max-width:680px; margin:0 auto; }}
  .mail table {{ max-width:100%; }}
  @media (max-width:620px) {{ .mail td.em-pad {{ padding:26px 20px !important; }} }}
</style>
</head>
<body>
<div class="mail">{shell(inner, pre, "p")}</div>
</body>
</html>
"""


def main():
    (HERE / "klaviyo").mkdir(exist_ok=True)
    (HERE / "preview").mkdir(exist_ok=True)
    (HERE / "public").mkdir(exist_ok=True)
    for e in EMAILS:
        k = klaviyo_doc(e)
        (HERE / "klaviyo" / f"email-{e['n']}.html").write_text(k)
        (HERE / "preview" / f"email-{e['n']}.html").write_text(preview_page(e, k))
        (HERE / "public" / f"email-{e['n']}.html").write_text(public_page(e))
        print("built email", e["n"])


main()
