#!/usr/bin/env python3
"""Erzeugt die statischen HTML-Seiten der Budget-Event-Website aus scripts/content.py."""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from content import T, IMG, POSTERS, EXHIBITOR_NAMES, INSTAGRAM, WHATSAPP, MAPS_ATRIUM, FORM_ENDPOINT  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = html.escape

FLAG_DE = '<svg viewBox="0 0 5 3" aria-hidden="true"><rect width="5" height="1" fill="#000"/><rect y="1" width="5" height="1" fill="#D00"/><rect y="2" width="5" height="1" fill="#FFCE00"/></svg>'
FLAG_GB = '<svg viewBox="0 0 60 30" aria-hidden="true"><clipPath id="t"><path d="M30,15h30v15zv15h-30zh-30v-15zv-15h30z"/></clipPath><path d="M0,0v30h60v-30z" fill="#012169"/><path d="M0,0L60,30M60,0L0,30" stroke="#fff" stroke-width="6"/><path d="M0,0L60,30M60,0L0,30" clip-path="url(#t)" stroke="#C8102E" stroke-width="4"/><path d="M30,0v30M0,15h60" stroke="#fff" stroke-width="10"/><path d="M30,0v30M0,15h60" stroke="#C8102E" stroke-width="6"/></svg>'


def head(t, title, desc, path, alt_path):
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="alternate" hreflang="{t['lang']}" href="{path}">
<link rel="alternate" hreflang="{'en' if t['lang'] == 'de' else 'de'}" href="{alt_path}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{IMG['viv']}">
<link rel="preload" href="/assets/fonts/fraunces-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/style.css">
<script src="/assets/main.js" defer></script>
</head>
<body>"""


def nav(t, here, alt, on_home):
    links = "".join(
        f'<a href="{(t["home"] if not on_home else "") + h if not on_home else h}">{e(l)}</a>'.replace('href="/#', 'href="/#').replace('href="/en#', 'href="/en#')
        for l, h in t["nav"]
    )
    de_active = "is-active" if t["lang"] == "de" else ""
    en_active = "is-active" if t["lang"] == "en" else ""
    de_href = here if t["lang"] == "de" else alt
    en_href = here if t["lang"] == "en" else alt
    cta_target = "" if not on_home else ' target="_blank" rel="noopener"'
    return f"""<header class="nav">
  <div class="wrap nav__in">
    <a class="brand" href="{t['home']}"><span class="brand__name">Budget <em>Event</em></span><span class="label">great deals for you</span></a>
    <nav class="nav__links" aria-label="Hauptnavigation">{links}</nav>
    <div class="nav__right">
      <div class="lang" aria-label="Sprache">
        <a class="flag {de_active}" href="{de_href}" lang="de" aria-label="Deutsch">{FLAG_DE}</a>
        <a class="flag {en_active}" href="{en_href}" lang="en" aria-label="English">{FLAG_GB}</a>
      </div>
      <a class="btn btn--ink nav__cta" href="{t['exh']}"{cta_target}>{e(t['cta'])}</a>
    </div>
  </div>
</header>"""


def footer(t, on_home):
    cta_target = ' target="_blank" rel="noopener"' if on_home else ""
    return f"""<footer class="section section--ink" id="kontakt">
  <div class="wrap stack-40">
    <p class="label muted-light">{e(t['ft_label'])}</p>
    <h2 class="display light">{t['ft_h2']}</h2>
    <p class="body muted-light narrow">{e(t['ft_body'])}</p>
    <div class="row-btns">
      <a class="btn btn--crimson" href="{INSTAGRAM}" target="_blank" rel="noopener">{e(t['ft_ig'])}</a>
      <a class="btn btn--outline-light" href="{t['exh']}"{cta_target}>{e(t['cta'])}</a>
    </div>
    <div class="ft-bottom">
      <span class="label muted-light">© 2026 Budget Event · great deals for you</span>
      <span class="ft-links label"><a href="{t['imprint']}">{e(t['imprint_l'])}</a><a href="{t['privacy']}">{e(t['privacy_l'])}</a><span class="muted-light">{e(t['ft_region'])}</span></span>
    </div>
  </div>
</footer>
</body>
</html>"""


def home(t):
    here, alt = t["home"], t["other_home"]
    exh_target = ' target="_blank" rel="noopener"'
    facts = "".join(f'<div class="fact"><span class="h3">{e(a)}</span><span class="label muted">{e(b)}</span></div>' for a, b in t["facts"])
    rows = "".join(f'<div class="drow"><span class="label muted-light">{e(a)}</span><span class="body light">{e(b)}</span></div>' for a, b in t["viv_rows"])
    sponsors = "".join(f'<div class="sponsor"><span class="label muted-light">{e(a)}</span><span class="body light strong">{e(b)}</span></div>' for a, b in t["sponsors"])
    events = ""
    for key, d, y, title, desc, loc, pill, hot in t["events"]:
        events += f"""<article class="event">
      <img class="event__img" src="{IMG[key]}" alt="{e(title)}" loading="lazy" width="96" height="140">
      <div class="event__date"><span class="h3 crimson tnum">{e(d)}</span><span class="label muted">{e(y)}</span></div>
      <div class="event__info"><h3 class="h3">{e(title)}</h3><p class="body muted">{e(desc)}</p></div>
      <div class="event__loc"><span class="body strong">{e(loc)}</span><span class="pill {'pill--crimson' if hot else ''}">{e(pill)}</span></div>
    </article>"""
    cards = "".join(
        f'<article class="xcard"><img src="{POSTERS[i]}" alt="Vivaaha 2027 – {e(n)}" loading="lazy" width="320" height="400"><span class="label crimson">{e(t["ex_cats"][i])}</span><h3 class="h3">{e(n)}</h3></article>'
        for i, n in enumerate(EXHIBITOR_NAMES)
    )
    rb = "".join(f'<span class="rpill">{e(x)}</span>' for x in t["rb_items"])
    return f"""{head(t, t['title'], t['desc'], here, alt)}
{nav(t, here, alt, True)}
<main>
<section class="section hero">
  <div class="wrap hero__cols">
    <div class="stack-28 hero__text">
      <p class="label crimson">{e(t['hero_label'])}</p>
      <h1 class="display">{t['hero_h1']}</h1>
      <p class="body muted narrow">{e(t['hero_body'])}</p>
      <div class="row-btns">
        <a class="btn btn--crimson" href="#events">{e(t['hero_btn'])}</a>
        <a class="btn btn--outline" href="{t['exh']}"{exh_target}>{e(t['cta'])}</a>
      </div>
    </div>
    <img class="hero__img" src="{IMG['hero']}" alt="{e(t['hero_img_alt'])}" width="460" height="560">
  </div>
  <div class="wrap facts">{facts}</div>
</section>

<section class="section section--ink" id="vivaaha">
  <div class="wrap stack-56">
    <span class="pill pill--crimson">{e(t['viv_badge'])}</span>
    <div class="viv__cols">
      <div class="stack-24 viv__text">
        <h2 class="h2 light">Vivaaha 2027</h2>
        <p class="h3 muted-light">{e(t['viv_sub'])}</p>
        <p class="body muted-light narrow">{e(t['viv_body'])}</p>
        <div class="drows">{rows}</div>
        <div class="row-btns">
          <a class="btn btn--crimson" href="{t['exh']}"{exh_target}>{e(t['cta'])}</a>
          <a class="btn btn--ivory" href="{MAPS_ATRIUM}" target="_blank" rel="noopener">{e(t['viv_route'])}</a>
          <a class="btn btn--outline-light" href="{INSTAGRAM}" target="_blank" rel="noopener">{e(t['viv_ig'])}</a>
        </div>
      </div>
      <img class="viv__poster" src="{IMG['viv']}" alt="Vivaaha 2027 – South Indian Wedding Expo" loading="lazy" width="380" height="676">
    </div>
    <div class="sponsors">{sponsors}</div>
  </div>
</section>

<section class="section" id="events">
  <div class="wrap stack-48">
    <div class="stack-16"><p class="label crimson">{e(t['ev_label'])}</p><h2 class="h2">{e(t['ev_h2'])}</h2><p class="body muted narrow">{e(t['ev_body'])}</p></div>
    <div class="events">{events}</div>
  </div>
</section>

<section class="section section--paper" id="aussteller">
  <div class="wrap stack-48">
    <div class="stack-16"><p class="label crimson">{e(t['ex_label'])}</p><h2 class="h2">{e(t['ex_h2'])}</h2><p class="body muted narrow">{e(t['ex_body'])}</p></div>
    <div class="xgrid">{cards}
      <a class="xcard xcard--cta" href="{t['exh']}"{exh_target}><span class="label">{e(t['ex_cta_l'])}</span><span class="h3">{e(t['ex_cta_t'])}</span></a>
    </div>
  </div>
</section>

<section class="section" id="rueckblick">
  <div class="wrap stack-48">
    <div class="stack-16"><p class="label crimson">{e(t['rb_label'])}</p><h2 class="h2">{e(t['rb_h2'])}</h2><p class="body muted">{e(t['rb_body'])}</p></div>
    <article class="rb-card">
      <img src="{IMG['zh']}" alt="Cook with Pugazh – Zürich" loading="lazy" width="200" height="356">
      <div class="stack-12"><span class="label crimson">{e(t['rb_zh_l'])}</span><h3 class="h3">{e(t['rb_zh_t'])}</h3><p class="body muted">{e(t['rb_zh_b'])}</p></div>
    </article>
    <div class="gallery">
      <img src="{IMG['g1']}" alt="Cook with Pugazh Zürich" loading="lazy"><img src="{IMG['g2']}" alt="Cook with Pugazh Zürich" loading="lazy"><img src="{IMG['g3']}" alt="Cook with Pugazh Zürich" loading="lazy">
    </div>
    <p class="label muted">{e(t['rb_credit'])}</p>
    <div class="rpills">{rb}</div>
  </div>
</section>
</main>
{footer(t, True)}"""


def exhibitors(t):
    here, alt = t["exh"], t["other_exh"]
    offers = "".join(f'<div class="offer"><span class="label muted-light">{e(a)}</span><span class="body light">{e(b)}</span></div>' for a, b in t["x_offers"])
    rules = "".join(f'<li>{e(r)}</li>' for r in t["x_rules"])
    facts = "".join(f'<div class="drow drow--stack"><span class="label muted-light">{e(a)}</span><span class="body light">{e(b)}</span></div>' for a, b in t["x_facts"])
    packs = ""
    for i, (title, price, desc) in enumerate(t["packs"]):
        val = f"{title} ({price})"
        packs += f"""<label class="pack">
          <input type="radio" name="paket" value="{e(val)}" required data-label="{e(title)} – {e(price)}">
          <span class="pack__box">
            <span class="label crimson">{e(title)}</span>
            <span class="h3 tnum">{e(price)}</span>
            <span class="small muted">{e(desc)}</span>
          </span>
        </label>"""
    f = t["fields"]

    def field(name, typ, required=True, half=False, area=False):
        lab, ph = f[name]
        star = " *" if required else ""
        req = " required" if required else ""
        ctl = (f'<textarea name="{name}" rows="4" placeholder="{e(ph)}"{req}></textarea>' if area else
               f'<input type="{typ}" name="{name}" placeholder="{e(ph)}" autocomplete="{ {"company": "organization", "person": "name", "email": "email", "phone": "tel"}.get(name, "off") }"{req}>')
        return f'<label class="field{" field--half" if half else ""}"><span class="label muted">{e(lab)}{star}</span>{ctl}</label>'

    return f"""{head(t, t['x_title'], t['x_desc'], here, alt)}
{nav(t, here, alt, False)}
<main>
<section class="section section--ink">
  <div class="wrap stack-48">
    <a class="label muted-light backlink" href="{t['home']}">{e(t['back'])}</a>
    <div class="stack-16">
      <p class="label crimson-light">{e(t['x_label'])}</p>
      <h1 class="h2 light">{e(t['x_h2'])}</h1>
      <p class="body muted-light narrow">{e(t['x_intro'])}</p>
    </div>
    <div class="offers">{offers}</div>
    <div class="x__cols">
      <div class="stack-32 x__info">
        <div class="stack-16"><h2 class="h3 light">{e(t['x_rules_h'])}</h2><ul class="rules">{rules}</ul></div>
        <div class="drows">{facts}</div>
        <div class="stack-12">
          <span class="label muted-light">{e(t['x_contact_h'])}</span>
          <span class="h3 light">{e(t['x_contact_n'])}</span>
          <div class="row-btns"><a class="btn btn--ivory" href="{WHATSAPP}" target="_blank" rel="noopener">{e(t['x_wa'])}</a><a class="btn btn--outline-light" href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></div>
        </div>
      </div>
      <div class="formcard" id="anmeldung">
        <div class="stack-8"><h2 class="h3">{e(t['f_h'])}</h2><p class="body muted">{e(t['f_sub'])}</p></div>
        <form class="form" action="{FORM_ENDPOINT}" method="post" data-ok="{e(t['ok'])}" data-err="{e(t['err'])}" data-sending="{e(t['sending'])}" data-none="{e(t['none_selected'])}" novalidate>
          <input type="hidden" name="sprache" value="{t['lang']}">
          <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
          <fieldset class="stack-12"><legend class="label crimson">{e(t['f_s1'])}</legend>
            <div class="packs">{packs}</div>
            <p class="small muted">{e(t['pack_hint'])}</p>
          </fieldset>
          <fieldset class="stack-16"><legend class="label crimson">{e(t['f_s2'])}</legend>
            <div class="fields">{field('company', 'text', half=True)}{field('person', 'text', half=True)}{field('email', 'email', half=True)}{field('phone', 'tel', half=True)}{field('offer', 'text')}{field('message', 'text', required=False, area=True)}</div>
          </fieldset>
          <fieldset class="stack-12"><legend class="label crimson">{e(t['f_s3'])}</legend>
            <div class="summary"><span class="label muted">{e(t['selected'])}</span><strong class="summary__val" data-summary>{e(t['none_selected'])}</strong></div>
            <label class="check"><input type="checkbox" name="bedingungen" value="akzeptiert" required><span class="body">{e(t['terms'])}</span></label>
            <button class="btn btn--crimson btn--block" type="submit">{e(t['send'])}</button>
            <p class="small muted">{e(t['privacy_note'])} <a href="{t['privacy']}">{e(t['privacy_l'])}</a></p>
            <p class="form__msg" role="status" aria-live="polite"></p>
          </fieldset>
        </form>
      </div>
    </div>
  </div>
</section>
</main>
{footer(t, False)}"""


def legal(kind):
    t = T["de"]
    if kind == "impressum":
        title, body = "Impressum", """
<p class="body">Angaben gemäss § 5 DDG und Art. 3 Abs. 1 lit. s UWG:</p>
<p class="body"><strong>[Name / Firma des Veranstalters]</strong><br>[Strasse Nr.]<br>[PLZ Ort]<br>[Land]</p>
<p class="body">E-Mail: [E-Mail-Adresse]<br>Telefon: [Telefonnummer]</p>
<p class="body">[Falls vorhanden: Handelsregister, UID / USt-IdNr.]</p>
<p class="body">Verantwortlich für den Inhalt: [Name]</p>
<p class="small muted">Website: CrispSite</p>"""
    else:
        title, body = "Datenschutzerklärung", """
<p class="body">Diese Datenschutzerklärung wird vor der Veröffentlichung vervollständigt (Verantwortlicher, Zweck, Rechtsgrundlagen, Empfänger wie Hosting und E-Mail-Versand, Aufbewahrung, Rechte der betroffenen Personen nach DSG und DSGVO).</p>
<p class="body">Kurz vorab: Diese Website verwendet keine Tracking-Cookies und lädt keine Schriften von Google. Angaben aus dem Aussteller-Formular werden ausschliesslich zur Bearbeitung der Anmeldung verwendet.</p>"""
    return f"""{head(t, title + ' | Budget Event', title, '/' + kind, '/' + kind)}
{nav(t, '/' + kind, '/' + kind, False)}
<main><section class="section"><div class="wrap stack-24 legal"><a class="label muted backlink" href="/">← Zur Startseite</a><h1 class="h2">{title}</h1>{body}</div></section></main>
{footer(t, False)}"""


def write(path, content):
    full = os.path.join(ROOT, path.lstrip("/"), "index.html") if not path.endswith(".html") else os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)
    print("✓", full.replace(ROOT, ""))


if __name__ == "__main__":
    write("/index.html", home(T["de"]))
    write("/en", home(T["en"]))
    write("/aussteller", exhibitors(T["de"]))
    write("/en/exhibitors", exhibitors(T["en"]))
    write("/impressum", legal("impressum"))
    write("/datenschutz", legal("datenschutz"))
