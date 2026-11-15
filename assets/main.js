// Aussteller-Formular: Paket-Zusammenfassung und Versand ohne Seitenwechsel
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form.form");
  if (!form) return;
  const summary = form.querySelector("[data-summary]");
  const msg = form.querySelector(".form__msg");
  const btn = form.querySelector("button[type=submit]");
  const btnLabel = btn.textContent;

  form.addEventListener("change", (ev) => {
    if (ev.target.name === "paket") summary.textContent = ev.target.dataset.label;
  });

  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    form.classList.add("was-validated");
    msg.textContent = ""; msg.className = "form__msg";
    if (!form.checkValidity()) {
      const first = form.querySelector(":invalid");
      if (first) first.focus();
      if (!form.querySelector("input[name=paket]:checked")) summary.textContent = form.dataset.none;
      return;
    }
    btn.disabled = true; btn.textContent = form.dataset.sending;
    try {
      const data = Object.fromEntries(new FormData(form).entries());
      const res = await fetch(form.action, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
      if (!res.ok) throw new Error("HTTP " + res.status);
      form.reset(); form.classList.remove("was-validated");
      summary.textContent = form.dataset.none;
      msg.textContent = form.dataset.ok; msg.classList.add("is-ok");
    } catch (err) {
      msg.textContent = form.dataset.err; msg.classList.add("is-err");
    } finally {
      btn.disabled = false; btn.textContent = btnLabel;
    }
  });
});
