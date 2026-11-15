# Budget Event – Website

Statische Website (DE/EN) für Budget Event, gehostet auf Vercel. Erstellt von CrispSite.

## Struktur
- `scripts/content.py` – alle Texte, Bilder und Pakete (DE/EN)
- `scripts/build.py` – erzeugt die HTML-Seiten (`python3 scripts/build.py`)
- `assets/` – CSS, JavaScript, selbst gehostete Schriften (Inter, Fraunces – SIL Open Font License)
- `api/anmeldung.js` – Aussteller-Formular → E-Mail via Resend

## Seiten
`/` · `/en` · `/aussteller` · `/en/exhibitors` · `/impressum` · `/datenschutz`

## Vercel – Umgebungsvariablen für das Formular
| Variable | Beispiel |
|---|---|
| `RESEND_API_KEY` | `re_…` |
| `ANMELDUNG_TO` | `info@budgetevent.ch` |
| `ANMELDUNG_FROM` | `Budget Event <anmeldung@budgetevent.ch>` |

## Offen vor Go-live
- Impressum und Datenschutzerklärung mit echten Angaben füllen
- Bilder liegen noch auf framerusercontent.com → ins Repo übernehmen
