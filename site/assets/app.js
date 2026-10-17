(function () {
  // Reveal on scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  // Opt-in / application forms
  var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var urlRe = /^(https?:\/\/)?([a-z0-9-]+\.)+[a-z]{2,}(\/\S*)?$/i;

  function normaliseUrl(v) {
    v = v.trim().replace(/\s+/g, '');
    if (v && !/^https?:\/\//i.test(v)) v = 'https://' + v;
    return v;
  }

  function check(field) {
    var input = field.querySelector('input, select');
    var v = input.value.trim();
    var ok = v !== '';
    if (ok && input.type === 'email') ok = emailRe.test(v);
    if (ok && input.name === 'store_url') ok = urlRe.test(v.replace(/\s+/g, ''));
    field.classList.toggle('has-error', !ok);
    input.setAttribute('aria-invalid', ok ? 'false' : 'true');
    return ok;
  }

  document.querySelectorAll('form[data-audit-form]').forEach(function (form) {
    var fields = form.querySelectorAll('.field');
    fields.forEach(function (f) {
      var input = f.querySelector('input, select');
      input.addEventListener('blur', function () { if (input.value) check(f); });
      input.addEventListener('input', function () { if (f.classList.contains('has-error')) check(f); });
      input.addEventListener('change', function () { if (f.classList.contains('has-error')) check(f); });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var allOk = true, firstBad = null;
      fields.forEach(function (f) {
        if (!check(f)) { allOk = false; if (!firstBad) firstBad = f; }
      });
      if (!allOk) { firstBad.querySelector('input, select').focus(); return; }

      var urlInput = form.querySelector('[name="store_url"]');
      urlInput.value = normaliseUrl(urlInput.value);

      var btn = form.querySelector('button[type="submit"]');
      var label = btn.querySelector('.btn-label');
      var errorBox = form.querySelector('.form-error');
      btn.disabled = true; label.textContent = 'Sending...';
      errorBox.classList.remove('show');

      var data = new FormData(form);
      var lead = {
        name: data.get('name').trim(),
        email: data.get('email').trim(),
        store: urlInput.value.replace(/^https?:\/\//i, '').replace(/\/$/, ''),
        revenue: data.get('monthly_revenue'),
        challenge: data.get('email_challenge')
      };
      var first = lead.name.split(' ')[0];
      var qualified = lead.revenue !== 'Under $30K';

      // Hook for analytics / pixels added later
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({
        event: 'audit_optin', funnel: form.getAttribute('name'),
        qualified: qualified, monthly_revenue: lead.revenue, email_challenge: lead.challenge
      });

      function done() {
        try { sessionStorage.setItem('arcadyLead', JSON.stringify(lead)); } catch (err) {}
        var next = '/thank-you/?name=' + encodeURIComponent(first);
        if (form.dataset.route === 'vsl' && qualified) {
          next = '/vsl/book/?name=' + encodeURIComponent(lead.name) + '&email=' + encodeURIComponent(lead.email);
        }
        window.location.href = next;
      }

      // Local preview has no Netlify Forms backend: skip the POST
      if (/^(localhost|127\.0\.0\.1)$/.test(location.hostname)) { done(); return; }

      // Save to Netlify Forms, but never block the visitor: move on after the save or after 2.5s
      var post = fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(data).toString()
      }).then(function (res) {
        if (!res.ok) console.warn('Form save failed: ' + res.status + '. Is Netlify form detection on?');
      }).catch(function (err) { console.warn('Form save failed', err); });
      Promise.race([post, new Promise(function (r) { setTimeout(r, 2500); })]).then(done);
    });
  });
})();
