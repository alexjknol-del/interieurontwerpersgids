# -*- coding: utf-8 -*-
"""Generator voor interieurontwerpersgids.be. Geen dependencies. Bouwt dist/."""
import os, shutil, html, datetime, re, json
from content import SITE, CHAPTERS, OVER

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
TODAY = datetime.date.today().isoformat()

CSS = r"""
:root{--bg:#fbfbfa;--bg2:#f0f1ef;--ink:#15181c;--muted:#5d646d;--line:#d7dbdf;--blue:#1e4a7a;--blue2:#163a60;--dark:#15181c;--darktext:#c9cfd6}
@media (prefers-color-scheme:dark){:root{--bg:#121417;--bg2:#1b1e23;--ink:#e6e8ea;--muted:#9aa3ad;--line:#2c3238;--blue:#7fb0e6;--blue2:#a6c9f0;--dark:#0b0d0f;--darktext:#8d959e}}
*{box-sizing:border-box}
html{background:var(--bg);color:var(--ink);font:16px/1.6 "Helvetica Neue",Helvetica,Arial,system-ui,sans-serif;-webkit-text-size-adjust:100%}
body{margin:0;display:grid;grid-template-columns:240px minmax(0,1fr);min-height:100vh}
a{color:var(--blue);text-decoration:none;border-bottom:1px solid transparent}
a:hover{border-bottom-color:currentColor}
.mono{font-family:"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.rail{border-right:1px solid var(--line);padding:28px 24px;position:sticky;top:0;height:100vh;overflow:auto;display:flex;flex-direction:column;gap:28px;background:var(--bg)}
.rail .logo{display:block;color:var(--ink);font-weight:700;font-size:15px;letter-spacing:-.01em;line-height:1.25;border:0}
.rail .logo span{display:block;font-weight:400;color:var(--muted);font-size:12px;margin-top:6px;letter-spacing:0}
.rail nav{display:flex;flex-direction:column;gap:6px}
.rail nav a{color:var(--ink);font-size:14px;padding:5px 0;border:0;border-left:2px solid transparent;padding-left:12px;margin-left:-14px}
.rail nav a.on,.rail nav a:hover{border-left-color:var(--blue);color:var(--blue)}
.rail .chap{display:flex;flex-direction:column;gap:2px}
.rail .chap a{color:var(--muted);font-size:12.5px;padding:4px 0;border:0;display:flex;gap:10px;line-height:1.35}
.rail .chap a b{font-weight:400;font-family:"SF Mono",Menlo,Consolas,monospace;font-size:11px;color:var(--blue);min-width:18px;padding-top:2px}
.rail .chap a.on,.rail .chap a:hover{color:var(--ink)}
.rail .chap h4{margin:12px 0 4px;font-size:11px;font-weight:400;color:var(--muted);letter-spacing:.1em;text-transform:uppercase}
.rail .chap h4:first-child{margin-top:0}
.topbar{display:none}
main{min-width:0}
.pad{padding:56px 64px;max-width:1100px}
h1{font-size:clamp(30px,3.6vw,46px);line-height:1.08;letter-spacing:-.02em;font-weight:700;margin:0 0 20px}
.lede{font-size:19px;line-height:1.5;color:var(--muted);max-width:38em;margin:0 0 40px}
.reg{border-top:1px solid var(--line)}
.reg .row{display:grid;grid-template-columns:70px 160px minmax(0,1fr) 120px;gap:24px;padding:22px 0;border-bottom:1px solid var(--line);color:var(--ink);align-items:baseline;border-bottom-color:var(--line)}
.reg .row:hover{background:var(--bg2)}
.reg .row .n{font-family:"SF Mono",Menlo,Consolas,monospace;font-size:22px;color:var(--blue);font-weight:400}
.reg .row .f{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-family:"SF Mono",Menlo,Consolas,monospace}
.reg .row .t{font-size:19px;font-weight:600;letter-spacing:-.01em;margin:0 0 4px}
.reg .row .d{color:var(--muted);font-size:14.5px;margin:0}
.reg .row .go{text-align:right;font-size:13px;color:var(--blue)}
.phases{display:grid;grid-template-columns:repeat(5,1fr);border:1px solid var(--line);margin:0 0 48px}
.phases div{padding:18px 18px 16px;border-right:1px solid var(--line)}
.phases div:last-child{border-right:0}
.phases b{display:block;font-family:"SF Mono",Menlo,Consolas,monospace;font-size:11px;color:var(--blue);margin-bottom:8px;font-weight:400;letter-spacing:.08em}
.phases span{font-size:13.5px;color:var(--muted);line-height:1.45;display:block}
.phases strong{display:block;font-size:14.5px;margin-bottom:4px}
article .head{display:grid;grid-template-columns:110px minmax(0,1fr);gap:24px;align-items:start;margin-bottom:34px}
article .head .big{font-family:"SF Mono",Menlo,Consolas,monospace;font-size:64px;line-height:1;color:var(--blue);font-weight:400;letter-spacing:-.04em}
article .head .big small{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-top:10px}
.fiche{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);margin:0 0 42px}
.fiche div{padding:16px 18px;border-right:1px solid var(--line)}
.fiche div:last-child{border-right:0}
.fiche b{display:block;font-family:"SF Mono",Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:400;margin-bottom:6px}
.fiche span{font-size:14px;line-height:1.45}
.steps{max-width:44em}
.step{display:grid;grid-template-columns:56px minmax(0,1fr);gap:18px;padding:30px 0;border-top:1px solid var(--line)}
.step .k{font-family:"SF Mono",Menlo,Consolas,monospace;font-size:13px;color:var(--blue);padding-top:6px}
.step h2{margin:0 0 12px;font-size:23px;letter-spacing:-.015em;font-weight:600;line-height:1.2}
.step p{margin:0 0 14px;font-size:16.5px;line-height:1.65}
.step p:last-child{margin-bottom:0}
.ref{margin:36px 0 0;border:1px solid var(--blue);padding:22px 24px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:20px;align-items:center;max-width:44em}
.ref b{display:block;font-size:16px;margin-bottom:4px}
.ref p{margin:0;color:var(--muted);font-size:14.5px}
.ref a{display:inline-block;background:var(--blue);color:#fff;padding:10px 16px;font-size:14px;border:0;white-space:nowrap}
.ref a:hover{background:var(--blue2)}
.nextrow{display:flex;justify-content:space-between;gap:24px;margin-top:48px;padding-top:22px;border-top:1px solid var(--line);max-width:44em}
.nextrow a{border:0;font-size:15px}
.nextrow a small{display:block;color:var(--muted);font-family:"SF Mono",Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;margin-bottom:4px}
.text{max-width:40em}
.text h2{font-size:22px;font-weight:600;margin:32px 0 10px;letter-spacing:-.01em}
.text p{margin:0 0 16px;font-size:16.5px;line-height:1.65}
footer{background:var(--dark);color:var(--darktext);padding:32px 64px;font-size:13.5px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px 32px}
footer a{color:var(--darktext);border:0;margin-right:18px}
footer a:hover{color:#fff}
@media (max-width:980px){body{display:block}.rail{display:none}.topbar{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:16px 20px;border-bottom:1px solid var(--line);flex-wrap:wrap}.topbar .logo{color:var(--ink);font-weight:700;font-size:15px;border:0}.topbar nav{display:flex;gap:16px;font-size:14px}.topbar nav a{color:var(--ink);border:0}.topbar nav a.on{color:var(--blue)}.pad{padding:32px 20px}.phases{grid-template-columns:1fr 1fr}.phases div{border-bottom:1px solid var(--line)}.phases div:nth-child(odd){border-right:1px solid var(--line)}.reg .row{display:block;padding:18px 0}.reg .row .n{display:block;margin-bottom:2px}.reg .row .f{display:block;margin-bottom:8px}.reg .row .go{display:block;text-align:left;margin-top:10px}.fiche{grid-template-columns:1fr 1fr}.fiche div{border-bottom:1px solid var(--line)}article .head{grid-template-columns:1fr;gap:12px}.ref{grid-template-columns:1fr}footer{padding:28px 20px}}
"""

def esc(s): return html.escape(s, quote=True)
def _j(s): return json.dumps(s, ensure_ascii=False)
def sid(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def ext(url, anchor):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, esc(anchor))

def linkify(text):
    return re.sub(r"https?://[^\s<>\"')]+(?<![.,])", lambda m: ext(m.group(0), m.group(0)), esc(text))

NAV = [("/", "Start"), ("/hoofdstukken/", "Hoofdstukken"), ("/over/", "Over de gids"), ("/contact/", "Contact")]

def navlinks(active):
    return "".join('<a href="%s"%s>%s</a>' % (h, ' class="on"' if h == active else "", t) for h, t in NAV)

def chapter_rail(active_slug=""):
    out = []
    last = None
    for c in CHAPTERS:
        if c["fase"] != last:
            out.append("<h4>%s</h4>" % esc(c["fase"]))
            last = c["fase"]
        out.append('<a href="/hoofdstukken/%s/"%s><b>%s</b><span>%s</span></a>' % (c["slug"], ' class="on"' if c["slug"] == active_slug else "", c["nr"], esc(c["title"])))
    return "".join(out)

def layout(title, meta, body, path, active="", active_slug="", extra_head=""):
    canonical = SITE["url"] + path
    return """<!DOCTYPE html>
<html lang="nl-BE">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_BE">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>%s</style>
%s
</head>
<body>
<aside class="rail">
<a class="logo" href="/">Interieurontwerpers<br>gids.be<span>%s</span></a>
<nav>%s</nav>
<div class="chap">%s</div>
</aside>
<main>
<div class="topbar"><a class="logo" href="/">Interieurontwerpersgids.be</a><nav>%s</nav></div>
%s
<footer>
<div>&copy; %s Interieurontwerpersgids.be</div>
<div><a href="/over/">Over de gids</a><a href="/contact/">Contact</a><a href="/privacybeleid/">Privacybeleid</a><a href="/cookiebeleid/">Cookiebeleid</a><a href="/sitemap.xml">Sitemap</a></div>
</footer>
</main>
</body>
</html>""" % (esc(title), esc(meta), canonical, esc(title), esc(meta), canonical, CSS, extra_head,
              esc(SITE["tagline"]), navlinks(active), chapter_rail(active_slug), navlinks(active), body, datetime.date.today().year)

def write(path, content):
    full = os.path.join(OUT, path.strip("/"), "index.html") if path != "/" else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)

def summ(c):
    s = c["meta"].split(": ", 1)[-1].split(". ")[0].rstrip(".")
    return s[0].upper() + s[1:] + "."

def register():
    rows = []
    for c in CHAPTERS:
        rows.append('<a class="row" href="/hoofdstukken/%s/"><span class="n">%s</span><span class="f">%s</span><span><span class="t" style="display:block">%s</span><span class="d" style="display:block">%s</span></span><span class="go">Lees hoofdstuk</span></a>'
                    % (c["slug"], c["nr"], esc(c["fase"]), esc(c["title"]), esc(summ(c))))
    return '<div class="reg">%s</div>' % "".join(rows)

PHASES = [("01", "Voorbereiding", "Briefing, opmeting en plattegrond op schaal."),
          ("02-03", "Vaste inrichting", "Keuken en badkamer, de duurste en meest technische delen."),
          ("04-06", "Afwerking", "Kleurplan, lichtplan en raamdecoratie op tekening."),
          ("07-08", "Uitvoering", "Materiaalstaat, planning, montage en bevestiging."),
          ("09-11", "Inrichting", "Klokken, styling, accessoires en de buitenruimte.")]

def home():
    ph = "".join("<div><b>%s</b><strong>%s</strong><span>%s</span></div>" % (n, esc(t), esc(d)) for n, t, d in PHASES)
    body = """<div class="pad">
<p class="mono">Gids in elf hoofdstukken</p>
<h1>Hoe een interieurontwerp tot stand komt, stap voor stap.</h1>
<p class="lede">Van de briefing tot de laatste vaas: de werkwijze van de interieurontwerper, met de maten, documenten en vuistregels per fase. Geschreven voor wie een ontwerper inschakelt en voor wie het zelf gestructureerd wil aanpakken.</p>
<div class="phases">%s</div>
<p class="mono" style="margin:0 0 12px">Register</p>
%s
</div>""" % (ph, register())
    write("/", layout("Interieurontwerpersgids.be | Hoe een interieurontwerp tot stand komt", SITE["description"], body, "/", "/"))

def index():
    body = """<div class="pad">
<p class="mono">Alle hoofdstukken</p>
<h1>Elf hoofdstukken in de volgorde van het ontwerpproces</h1>
<p class="lede">Elk hoofdstuk begint met een fiche: de fase, het resultaat, wie erbij betrokken is en de meest gemaakte fout. Daarna volgt het artikel in genummerde stappen.</p>
%s
</div>""" % register()
    write("/hoofdstukken/", layout("Alle hoofdstukken | Interieurontwerpersgids.be", "Overzicht van de elf hoofdstukken: briefing, keuken, badkamer, kleurplan, lichtplan, raamdecoratie, materialen, montage, klokken, styling en buitenruimte.", body, "/hoofdstukken/", "/hoofdstukken/"))

def chapter(i, c):
    prev = CHAPTERS[i - 1] if i > 0 else None
    nxt = CHAPTERS[i + 1] if i < len(CHAPTERS) - 1 else None
    fiche = "".join("<div><b>%s</b><span>%s</span></div>" % (esc(k), esc(v)) for k, v in c["fiche"])
    steps = []
    for n, (h, paras) in enumerate(c["steps"], 1):
        steps.append('<section class="step" id="%s"><div class="k">%s.%d</div><div><h2>%s</h2>%s</div></section>' % (
            sid(h), c["nr"], n, esc(h), "".join("<p>%s</p>" % linkify(p) for p in paras)))
    ref = ""
    if c["partner"]:
        p = c["partner"]
        ref = '<div class="ref"><div><b>%s</b><p>%s</p></div>%s</div>' % (esc(p["name"]), esc(p["blurb"]), ext(p["url"], p["anchor"]))
    nr = '<div class="nextrow"><div>%s</div><div style="text-align:right">%s</div></div>' % (
        ('<a href="/hoofdstukken/%s/"><small>Vorige</small>%s %s</a>' % (prev["slug"], prev["nr"], esc(prev["title"]))) if prev else "",
        ('<a href="/hoofdstukken/%s/"><small>Volgende</small>%s %s</a>' % (nxt["slug"], nxt["nr"], esc(nxt["title"]))) if nxt else "")
    body = """<div class="pad"><article>
<div class="head"><div class="big">%s<small>%s</small></div><div><h1>%s</h1><p class="lede" style="margin-bottom:0">%s</p></div></div>
<div class="fiche">%s</div>
<div class="steps">%s</div>
%s
%s
</article></div>""" % (c["nr"], esc(c["fase"]), esc(c["h1"]), esc(c["intro"]), fiche, "".join(steps), ref, nr)
    schema = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article","headline":%s,"description":%s,"inLanguage":"nl-BE","datePublished":"%s","mainEntityOfPage":"%s","publisher":{"@type":"Organization","name":"Interieurontwerpersgids.be","url":"%s"}}</script>' % (
        _j(c["h1"]), _j(c["meta"]), TODAY, SITE["url"] + "/hoofdstukken/%s/" % c["slug"], SITE["url"])
    ttl = "%s | Interieurontwerpersgids.be" % c["title"]
    write("/hoofdstukken/%s/" % c["slug"], layout(ttl, c["meta"], body, "/hoofdstukken/%s/" % c["slug"], "/hoofdstukken/", c["slug"], schema))

def simple(path, title, meta, h1, inner, active=""):
    body = '<div class="pad"><div class="text"><h1>%s</h1>%s</div></div>' % (esc(h1), inner)
    write(path, layout(title, meta, body, path, active))

def over():
    simple("/over/", OVER["title"] + " | Interieurontwerpersgids.be", OVER["meta"], OVER["title"], "".join("<p>%s</p>" % linkify(p) for p in OVER["paragraphs"]), "/over/")

def contact():
    inner = """<p>Interieurontwerpersgids.be is bereikbaar per e-mail op <a href="mailto:info@interieurontwerpersgids.be">info@interieurontwerpersgids.be</a>.</p>
<p>Het adres is bedoeld voor vragen over de inhoud, meldingen van fouten en suggesties voor nieuwe hoofdstukken. Berichten worden gelezen en waar nodig beantwoord.</p>
<p>De gids ontwerpt zelf geen interieurs en verkoopt niets. Vragen over een bestelling of een offerte horen bij de leverancier of het merk waarnaar in een hoofdstuk wordt verwezen.</p>"""
    simple("/contact/", "Contact | Interieurontwerpersgids.be", "Contact met Interieurontwerpersgids.be verloopt per e-mail via info@interieurontwerpersgids.be. Geen formulier, geen telefoon.", "Contact", inner, "/contact/")

def privacy():
    inner = """<p>Interieurontwerpersgids.be verwerkt zo weinig mogelijk persoonsgegevens. Hieronder staat wat er wel en niet gebeurt.</p>
<h2>Bezoek</h2>
<p>De site bestaat uit vaste pagina's zonder accounts, formulieren of nieuwsbrief. De site verzamelt zelf geen persoonsgegevens. De hostingpartij kan technische gegevens zoals IP-adres en tijdstip kort bewaren in logbestanden om de dienst te beveiligen.</p>
<h2>E-mail</h2>
<p>Wie mailt naar info@interieurontwerpersgids.be deelt een e-mailadres en de inhoud van het bericht. Die gegevens dienen alleen om te antwoorden, worden niet gedeeld met derden en worden verwijderd zodra ze niet meer nodig zijn.</p>
<h2>Verwijzingen</h2>
<p>De gids verwijst naar leveranciers en merken. Op hun sites geldt hun eigen privacybeleid, waar Interieurontwerpersgids.be geen invloed op heeft.</p>
<h2>Rechten</h2>
<p>Iedereen kan inzage, verbetering of verwijdering vragen van persoonsgegevens die Interieurontwerpersgids.be zou bewaren, via info@interieurontwerpersgids.be. Klachten kunnen bij de Gegevensbeschermingsautoriteit, %s.</p>""" % ext("https://www.gegevensbeschermingsautoriteit.be/", "https://www.gegevensbeschermingsautoriteit.be/")
    simple("/privacybeleid/", "Privacybeleid | Interieurontwerpersgids.be", "Hoe Interieurontwerpersgids.be omgaat met gegevens van bezoekers en van wie een e-mail stuurt. Geen accounts, geen formulieren.", "Privacybeleid", inner)

def cookies():
    inner = """<p>Interieurontwerpersgids.be plaatst zelf geen cookies. Er draaien geen statistiekscripts, geen advertenties en geen ingesloten inhoud van andere platformen.</p>
<h2>Technisch noodzakelijk</h2>
<p>De hostingpartij kan een technisch noodzakelijke cookie plaatsen om de verbinding te beveiligen. Zo'n cookie bevat geen persoonsgegevens en volgt bezoekers niet.</p>
<h2>Andere sites</h2>
<p>Wie doorklikt naar een leverancier of merk, komt op een site met een eigen cookiebeleid. Daar kunnen wel cookies geplaatst worden.</p>
<h2>Beheer</h2>
<p>Cookies zijn in elke browser te bekijken en te verwijderen via de instellingen onder privacy of sitegegevens.</p>"""
    simple("/cookiebeleid/", "Cookiebeleid | Interieurontwerpersgids.be", "Interieurontwerpersgids.be plaatst zelf geen cookies. Wat de hostingpartij kan doen en hoe cookies beheerd worden in de browser.", "Cookiebeleid", inner)

def notfound():
    body = '<div class="pad"><div class="text"><h1>Pagina niet gevonden</h1><p>Deze pagina bestaat niet. Alle hoofdstukken staan in <a href="/hoofdstukken/">het register</a>.</p></div></div>'
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(layout("Pagina niet gevonden | Interieurontwerpersgids.be", "Deze pagina bestaat niet.", body, "/404.html"))

def extras():
    urls = ["/", "/hoofdstukken/", "/over/", "/contact/", "/privacybeleid/", "/cookiebeleid/"] + ["/hoofdstukken/%s/" % c["slug"] for c in CHAPTERS]
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
            "<url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n" % (SITE["url"], u, TODAY) for u in urls) + "</urlset>\n")
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE["url"])
    open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="#1e4a7a"/><path d="M8 24V8h4v12h6v4z" fill="#fff"/><rect x="20" y="8" width="4" height="4" fill="#fff"/></svg>')
    open(os.path.join(OUT, "_headers"), "w", encoding="utf-8").write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: DENY\n")

def main():
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    home(); index()
    for i, c in enumerate(CHAPTERS): chapter(i, c)
    over(); contact(); privacy(); cookies(); notfound(); extras()
    print("gebouwd:", sum(len(f) for _, _, f in os.walk(OUT)), "bestanden")

if __name__ == "__main__":
    main()
