// VSL application: one question per screen, Typeform-style.
// Under $30K/month → /thank-you/ (still gets the audit), otherwise → /vsl/book/ (Calendly).
// Answers post to Netlify Forms ("vsl-application").

(() => {
  const REVENUE = [
    { value: "Under $30K", qualifies: false },
    { value: "$30K – $100K", qualifies: true },
    { value: "$100K – $250K", qualifies: true },
    { value: "$250K – $500K", qualifies: true },
    { value: "$500K – $1M", qualifies: true },
    { value: "$1M+", qualifies: true },
  ];

  const STEPS = [
    { id: "store_url", type: "url", label: "What's your store URL?", placeholder: "yourbrand.com", autocomplete: "url", help: "We'll start the audit from here." },
    {
      id: "bottleneck", type: "choice", label: "What's your biggest bottleneck in scaling right now?",
      options: [
        "Ad costs rising, ROAS dropping",
        "Customers buy once and don't come back",
        "Site traffic doesn't convert",
        "Not enough traffic",
        "No time or team to do it all",
        "Something else",
      ],
    },
    { id: "monthly_revenue", type: "choice", label: "What's your store's monthly revenue?", options: REVENUE.map((r) => r.value) },
    {
      id: "email_challenge", type: "choice", label: "And your biggest email challenge?",
      options: [
        "Email drives too little of our revenue",
        "Flows are missing or out of date",
        "Low open rates or landing in spam",
        "Our list isn't growing",
        "We rely too much on discounts",
        "We don't send email yet",
        "Something else",
      ],
    },
    { id: "name", type: "text", label: "Almost done. What's your name?", placeholder: "Type your full name", autocomplete: "name" },
    { id: "email", type: "email", label: (a) => `Thanks${a.name ? ", " + a.name.split(/\s+/)[0] : ""}. What's your best email?`, placeholder: "name@yourbrand.com", autocomplete: "email", help: "Your audit gets sent here." },
    { id: "phone", type: "tel", label: "And your phone number?", placeholder: "+1 555 000 0000", autocomplete: "tel", help: "Only used to reach you about your audit." },
  ];

  const box = document.getElementById("apply");
  if (!box) return;
  const stage = document.getElementById("apply-stage");
  const bar = document.getElementById("apply-progress");
  const back = document.getElementById("apply-back");
  const answers = {};
  const utm = Object.fromEntries(["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "fbclid"]
    .map((k) => [k, new URLSearchParams(location.search).get(k) || ""]).filter(([, v]) => v));
  let index = 0;
  let lastFocus = null;

  const letters = "ABCDEFGH";
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function render() {
    const step = STEPS[index];
    const label = typeof step.label === "function" ? step.label(answers) : step.label;
    const value = answers[step.id] || "";
    let field = "";

    if (step.type === "choice") {
      field = `<div class="apply__choices" role="radiogroup" aria-label="${esc(label)}">${step.options
        .map((o, i) => `<button type="button" class="apply__choice${value === o ? " is-selected" : ""}" data-value="${esc(o)}" role="radio" aria-checked="${value === o}"><span class="apply__key">${letters[i]}</span>${esc(o)}</button>`)
        .join("")}</div>`;
    } else {
      const type = step.type === "url" ? "text" : step.type;
      const mode = { url: "url", email: "email", tel: "tel" }[step.type] || "text";
      field = `<input class="apply__input" id="apply-field" type="${type}" inputmode="${mode}" autocomplete="${step.autocomplete}" placeholder="${esc(step.placeholder)}" value="${esc(value)}">`;
    }

    const isLast = index === STEPS.length - 1;
    stage.innerHTML = `
      <div class="apply__q">
        <label class="apply__label" for="apply-field"><span class="apply__num">${index + 1}</span><span>${esc(label)}<span class="apply__req" aria-hidden="true"> *</span></span></label>
        ${step.help ? `<p class="apply__help">${esc(step.help)}</p>` : ""}
        ${field}
        <p class="apply__error" id="apply-error" role="alert"></p>
        ${step.type === "choice" ? "" : `<div class="apply__actions"><button type="submit" class="apply__ok">${isLast ? "Submit" : "OK"}</button><span class="apply__hint">press <b>Enter ↵</b></span></div>`}
      </div>`;

    bar.style.width = `${(index / STEPS.length) * 100}%`;
    back.disabled = index === 0;
    stage.querySelector(".apply__q").classList.add("is-in");
    const first = stage.querySelector("#apply-field") || stage.querySelector(".apply__choice");
    first?.focus({ preventScroll: true });
  }

  function error(msg) {
    const el = document.getElementById("apply-error");
    if (el) el.textContent = msg;
  }

  function validate(step, value) {
    const v = value.trim();
    if (!v) return "Please fill this in.";
    if (step.type === "url" && !/^(https?:\/\/)?([a-z0-9-]+\.)+[a-z]{2,}(\/\S*)?$/i.test(v.replace(/\s+/g, ""))) return "Hmm, that doesn't look like a web address. Try yourbrand.com";
    if (step.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return "Hmm, that email doesn't look right.";
    if (step.type === "tel" && v.replace(/\D/g, "").length < 7) return "Please enter a valid phone number.";
    return "";
  }

  function next() {
    if (index === STEPS.length - 1) {
      const tier = REVENUE.find((r) => r.value === answers.monthly_revenue);
      return finish(Boolean(tier?.qualifies));
    }
    index += 1;
    render();
  }

  function submitText() {
    const step = STEPS[index];
    const field = document.getElementById("apply-field");
    const value = field ? field.value : "";
    const problem = validate(step, value);
    if (problem) return error(problem);
    let v = value.trim();
    if (step.type === "url") {
      v = v.replace(/\s+/g, "");
      if (!/^https?:\/\//i.test(v)) v = "https://" + v;
    }
    answers[step.id] = v;
    next();
  }

  function choose(value) {
    answers[STEPS[index].id] = value;
    stage.querySelectorAll(".apply__choice").forEach((b) => {
      const on = b.dataset.value === value;
      b.classList.toggle("is-selected", on);
      b.setAttribute("aria-checked", String(on));
    });
    setTimeout(next, 280);
  }

  async function finish(qualified) {
    bar.style.width = "100%";
    stage.innerHTML = `<div class="apply__q is-in"><p class="apply__label">${qualified ? "Great, your store looks like a fit. Taking you to the calendar…" : "Thanks, submitting your application…"}</p></div>`;

    // Hook for analytics / pixels added later
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: "audit_optin", funnel: "vsl-application", qualified, monthly_revenue: answers.monthly_revenue, bottleneck: answers.bottleneck, email_challenge: answers.email_challenge });

    const store = (answers.store_url || "").replace(/^https?:\/\//i, "").replace(/\/$/, "");
    try {
      sessionStorage.setItem("arcadyLead", JSON.stringify({
        name: answers.name, email: answers.email, store, revenue: answers.monthly_revenue, challenge: answers.email_challenge,
      }));
    } catch {}

    // Local preview has no Netlify Forms backend
    if (!/^(localhost|127\.0\.0\.1)$/.test(location.hostname)) {
      const body = new URLSearchParams({ "form-name": "vsl-application", ...answers, ...utm, qualified: qualified ? "yes" : "no" });
      try {
        await Promise.race([
          fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body }),
          new Promise((r) => setTimeout(r, 2500)),
        ]);
      } catch {
        // A failed submission must never block the visitor.
      }
    }

    const first = (answers.name || "").split(/\s+/)[0];
    if (!qualified) {
      location.href = `/thank-you/?name=${encodeURIComponent(first)}`;
      return;
    }
    const params = new URLSearchParams({ name: answers.name || "", email: answers.email || "" });
    location.href = `/vsl/book/?${params}`;
  }

  function open(trigger) {
    lastFocus = trigger;
    index = 0;
    box.hidden = false;
    document.body.style.overflow = "hidden";
    render();
  }

  function close() {
    box.hidden = true;
    document.body.style.overflow = "";
    lastFocus?.focus();
  }

  document.addEventListener("click", (e) => {
    const trigger = e.target.closest("[data-apply]");
    if (trigger) {
      e.preventDefault();
      open(trigger);
    }
  });

  stage.addEventListener("submit", (e) => {
    e.preventDefault();
    submitText();
  });

  stage.addEventListener("click", (e) => {
    const c = e.target.closest(".apply__choice");
    if (c) choose(c.dataset.value);
  });

  document.addEventListener("keydown", (e) => {
    if (box.hidden) return;
    if (e.key === "Escape") return close();
    const step = STEPS[index];
    if (step?.type === "choice" && !e.metaKey && !e.ctrlKey && !e.altKey) {
      const i = letters.indexOf(e.key.toUpperCase());
      if (i >= 0 && i < step.options.length) choose(step.options[i]);
    }
  });

  back.addEventListener("click", () => {
    if (index > 0) {
      index -= 1;
      render();
    }
  });
  document.getElementById("apply-close").addEventListener("click", close);

  if (location.hash === "#apply") open(null);
})();
