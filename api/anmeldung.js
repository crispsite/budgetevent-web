// Vercel Serverless Function: nimmt Aussteller-Anmeldungen entgegen und verschickt sie per E-Mail (Resend).
// Benötigte Umgebungsvariablen in Vercel:
//   RESEND_API_KEY  – API-Schlüssel von resend.com
//   ANMELDUNG_TO    – Empfänger, z. B. info@budgetevent.ch (mehrere mit Komma)
//   ANMELDUNG_FROM  – Absender auf verifizierter Domain, z. B. "Budget Event <anmeldung@budgetevent.ch>"

const REQUIRED = ["paket", "company", "person", "email", "phone", "offer", "bedingungen"];
const LABELS = { paket: "Paket", company: "Firma / Aussteller", person: "Kontaktperson", email: "E-Mail", phone: "Telefon / WhatsApp", offer: "Angebot", message: "Nachricht", sprache: "Sprache", bedingungen: "Bedingungen" };

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "method_not_allowed" });
  const body = typeof req.body === "string" ? JSON.parse(req.body || "{}") : (req.body || {});

  if (body.website) return res.status(200).json({ ok: true }); // Spam-Falle
  const missing = REQUIRED.filter((k) => !String(body[k] || "").trim());
  if (missing.length) return res.status(400).json({ error: "missing_fields", fields: missing });
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(body.email)) return res.status(400).json({ error: "invalid_email" });

  const { RESEND_API_KEY, ANMELDUNG_TO, ANMELDUNG_FROM } = process.env;
  if (!RESEND_API_KEY || !ANMELDUNG_TO) return res.status(503).json({ error: "not_configured" });

  const rows = Object.keys(LABELS).filter((k) => body[k]).map((k) => `<tr><td style="padding:6px 12px 6px 0;color:#6E645B">${LABELS[k]}</td><td style="padding:6px 0"><strong>${esc(body[k])}</strong></td></tr>`).join("");
  const html = `<div style="font-family:Arial,sans-serif;font-size:15px;color:#15110E"><h2 style="margin:0 0 12px">Neue Aussteller-Anmeldung – Vivaaha 2027</h2><table>${rows}</table></div>`;

  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: ANMELDUNG_FROM || "Budget Event <onboarding@resend.dev>",
      to: ANMELDUNG_TO.split(",").map((s) => s.trim()),
      reply_to: body.email,
      subject: `Aussteller-Anmeldung: ${String(body.company).slice(0, 80)} – ${body.paket}`,
      html,
    }),
  });
  if (!r.ok) return res.status(502).json({ error: "mail_failed" });
  return res.status(200).json({ ok: true });
}
