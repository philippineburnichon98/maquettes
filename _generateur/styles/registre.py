"""Style « registre » — une étude notariale présentée comme un feuillet de registre des minutes.

Pour un office notarial au ton sobre. Chaque section est un feuillet : une marge à gauche porte
la mention marginale (nom de la section, renvois), le corps est réglé de filets fins couleur encre.
Élément mémorable : la filiation de l'étude tenue comme un registre réglé (dates en marge,
successions d'études), accompagnée d'un sceau gaufré en CSS (seul moment animé, respecte
prefers-reduced-motion). Compétences en articles d'acte, informations pratiques en tableau,
prise de rendez-vous par téléphone ou e-mail (ou lien existant), pied de page réglementaire
(chambre des notaires, SIRET, médiateur).

Thème (d["theme"]) : paper, ink, river (couleur principale), stone, wax (accent rare, sceau),
rule (filets), serif, sans, fonts (URL Google Fonts).
"""
from core import e, a, tgt, logo, map_iframe, page

CSS = """
:root{--paper:%(paper)s;--ink:%(ink)s;--river:%(river)s;--stone:%(stone)s;--wax:%(wax)s;--rule:%(rule)s;
--serif:%(serif)s;--sans:%(sans)s;--muted:color-mix(in srgb,var(--ink) 68%%,var(--paper))}
body{background:var(--paper);color:var(--ink);font:400 1.06rem/1.7 var(--serif)}
a{color:var(--river)}a:hover{color:var(--wax)}
.w{max-width:1120px;margin:0 auto;padding:0 24px}
.sans{font-family:var(--sans)}
header.top{border-bottom:1px solid var(--ink);background:var(--paper);position:sticky;top:0;z-index:40}
header.top .w{display:flex;align-items:center;justify-content:space-between;gap:20px;min-height:74px}
.logo-txt{font-family:var(--serif);font-weight:600;font-size:1.12rem;color:var(--ink);line-height:1.15;display:block}
.brand small{display:block;font:500 .78rem/1.3 var(--sans);color:var(--muted);margin-top:3px}
.brand{text-decoration:none}
nav.nv{display:flex;gap:22px;font:500 .92rem var(--sans)}nav.nv a{color:var(--ink);text-decoration:none;white-space:nowrap;padding:6px 0;border-bottom:1px solid transparent}
nav.nv a:hover{border-color:var(--river);color:var(--river)}
.rdv{font:600 .9rem var(--sans);background:var(--river);color:#fff!important;text-decoration:none;padding:10px 16px;border-radius:2px;white-space:nowrap}
.rdv:hover{background:var(--ink)}
.burger{display:none;font:600 .9rem var(--sans);background:none;border:1px solid var(--ink);padding:8px 12px;cursor:pointer}
@media(max-width:900px){nav.nv{display:none;position:absolute;left:0;right:0;top:74px;background:var(--paper);flex-direction:column;gap:0;padding:4px 24px 14px;border-bottom:1px solid var(--ink)}
nav.nv a{padding:12px 0;border-bottom:1px solid var(--rule)}header.open nav.nv{display:flex}.burger{display:block}header.top .rdv{display:none}}
/* feuillet */
.f{display:grid;grid-template-columns:200px minmax(0,1fr);gap:0 44px;padding:clamp(54px,8vw,96px) 0;border-bottom:1px solid var(--rule)}
.f>.mg{border-right:1px solid var(--wax);padding-right:22px;text-align:right;font:italic 400 1.02rem/1.4 var(--serif);color:var(--wax)}
.f>.mg span{display:block;font:500 .82rem/1.4 var(--sans);font-style:normal;color:var(--muted);margin-top:8px}
.f h2{font-weight:500;font-size:clamp(1.8rem,3.4vw,2.6rem);line-height:1.15;margin-bottom:22px;max-width:24ch}
.f p{max-width:64ch;margin-bottom:14px}
@media(max-width:760px){.f{grid-template-columns:minmax(0,1fr)}.f>.mg{border-right:0;border-bottom:1px solid var(--wax);text-align:left;padding:0 0 10px;margin-bottom:22px}}
/* en-tête d'acte */
.acte{padding:clamp(56px,9vw,110px) 0 clamp(40px,6vw,70px);border-bottom:3px double var(--ink)}
.acte .w{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:30px 60px;align-items:center}
.acte .who{font:500 .98rem/1.5 var(--sans);color:var(--muted)}
.acte h1{font-weight:500;font-size:clamp(2.3rem,6vw,4.4rem);line-height:1.04;margin:14px 0 20px;color:var(--ink)}
.acte .lead{font-size:1.18rem;max-width:52ch}
.acte .ctas{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}
.btn{display:inline-block;font:600 .95rem var(--sans);padding:13px 20px;border:1px solid var(--river);color:var(--river);text-decoration:none;border-radius:2px}
.btn.full{background:var(--river);color:#fff}.btn:hover{background:var(--ink);border-color:var(--ink);color:#fff}
.seal{width:190px;height:190px;border-radius:50%%;display:grid;place-items:center;text-align:center;position:relative;
background:radial-gradient(circle at 38%% 32%%,color-mix(in srgb,var(--paper) 70%%,#fff),var(--paper) 62%%,color-mix(in srgb,var(--stone) 55%%,var(--paper)));
box-shadow:inset 3px 3px 6px rgba(255,255,255,.9),inset -4px -4px 8px rgba(0,0,0,.13),0 1px 0 rgba(0,0,0,.05);color:color-mix(in srgb,var(--ink) 55%%,var(--paper));animation:press 1.1s ease-out both .3s}
.seal::before{content:"";position:absolute;inset:12px;border-radius:50%%;border:1px dashed color-mix(in srgb,var(--ink) 30%%,transparent)}
.seal div{font:600 .72rem/1.35 var(--sans);letter-spacing:.06em;padding:0 30px}.seal b{display:block;font:500 1.9rem/1.1 var(--serif);letter-spacing:0;margin:4px 0;color:var(--wax)}
@keyframes press{from{transform:scale(1.12);opacity:0;box-shadow:none}to{transform:none;opacity:1}}
@media(max-width:760px){.acte .w{grid-template-columns:minmax(0,1fr)}.seal{width:150px;height:150px}.seal b{font-size:1.5rem}}
/* registre réglé */
.ledger{border-top:2px solid var(--ink);margin-top:10px}
.ledger li{list-style:none;display:grid;grid-template-columns:150px minmax(0,1fr);gap:20px;padding:16px 0;border-bottom:1px solid var(--rule)}
.ledger time{font:600 .92rem/1.5 var(--sans);color:var(--river)}
.ledger .now time{color:var(--wax)}.ledger .now strong{font-weight:600}
@media(max-width:560px){.ledger li{grid-template-columns:minmax(0,1fr);gap:2px}}
.quote{font-size:1.25rem;font-style:italic;border-left:3px solid var(--river);padding:6px 0 6px 20px;margin:26px 0;max-width:56ch}
/* articles */
.arts{counter-reset:art;display:grid;gap:0;border-top:1px solid var(--ink)}
.arts article{display:grid;grid-template-columns:minmax(0,15ch) minmax(0,1fr);gap:24px;padding:22px 0;border-bottom:1px solid var(--rule)}
.arts h3{font-weight:600;font-size:1.2rem;line-height:1.3;color:var(--river)}
.arts p{margin:0}
@media(max-width:640px){.arts article{grid-template-columns:minmax(0,1fr);gap:6px}}
.inline-list{margin-top:26px;padding:18px 20px;background:color-mix(in srgb,var(--stone) 22%%,var(--paper));font:400 .98rem/1.65 var(--sans)}
/* pratique */
.prat{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:34px}
.prat table{width:100%%;border-collapse:collapse;font:400 .98rem/1.5 var(--sans)}
.prat th,.prat td{text-align:left;vertical-align:top;padding:11px 0;border-bottom:1px solid var(--rule)}.prat th{font-weight:600;width:42%%;padding-right:14px}
.prat .map{width:100%%;height:100%%;min-height:320px;border:1px solid var(--ink);filter:grayscale(.5)}
.coord{font:400 1rem/1.6 var(--sans);margin:20px 0}.coord a{font-weight:600}
@media(max-width:820px){.prat{grid-template-columns:minmax(0,1fr)}}
.news{list-style:none;border-top:1px solid var(--ink)}.news li{padding:12px 0;border-bottom:1px solid var(--rule)}
.links2{columns:2 240px;list-style:none;font:400 .98rem/1.5 var(--sans)}.links2 li{padding:6px 0;break-inside:avoid}
footer.ft{background:var(--ink);color:color-mix(in srgb,var(--paper) 86%%,var(--ink));padding:54px 0 110px;font:400 .9rem/1.6 var(--sans)}
footer.ft a{color:#fff}footer.ft .g{display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:32px}
footer.ft h3{font:500 1.15rem var(--serif);color:#fff;margin-bottom:10px}
footer.ft .legal{margin-top:34px;padding-top:18px;border-top:1px solid rgba(255,255,255,.2);font-size:.82rem;opacity:.85}
@media(max-width:760px){footer.ft .g{grid-template-columns:minmax(0,1fr)}}
"""

JS = """const H=document.querySelector('header.top'),B=H.querySelector('.burger');B.onclick=()=>{const o=H.classList.toggle('open');B.setAttribute('aria-expanded',o)};
H.querySelectorAll('nav a').forEach(x=>x.onclick=()=>{H.classList.remove('open');B.setAttribute('aria-expanded',false)});"""


def _sheet(sid, margin, sub, inner):
    sub_html = f"<span>{e(sub)}</span>" if sub else ""
    return f'<section id="{sid}"><div class="w f"><div class="mg">{e(margin)}{sub_html}</div><div>{inner}</div></div></section>'


def render(d):
    t = d["theme"]
    css = CSS % t
    c = d["contact"]
    rdv = d.get("booking") or [f'Prendre rendez-vous au {c["phone"]}', f'tel:{c["tel"]}']
    nav = "".join(f'<a href="#{i}">{e(l)}</a>' for i, l in d["nav"])
    head = f'''<header class="top"><div class="w"><a class="brand" href="#etude">{logo(d)}<small>{e(d.get("tagline", ""))}</small></a>
<nav class="nv" aria-label="Menu principal">{nav}</nav><a class="rdv" href="{a(rdv[1])}"{tgt(rdv[1])}>{e(rdv[0])}</a>
<button class="burger" aria-expanded="false" aria-label="Ouvrir le menu">Menu</button></div></header>'''
    h = d["hero"]
    seal = d.get("seal")
    seal_html = f'<div class="seal" aria-hidden="true"><div>{e(seal[0])}<b>{e(seal[1])}</b>{e(seal[2])}</div></div>' if seal else ""
    hero = f'''<section class="acte" id="etude"><div class="w"><div><p class="who">{e(h["who"])}</p><h1>{e(h["title"])}</h1>
<p class="lead">{e(h["lead"])}</p><div class="ctas"><a class="btn full" href="{a(rdv[1])}"{tgt(rdv[1])}>{e(rdv[0])}</a>
<a class="btn" href="mailto:{a(c["email"])}">Écrire à l'étude</a></div></div>{seal_html}</div></section>'''

    p = d["presentation"]
    lis = "".join(f'<li class="{"now" if x.get("now") else ""}"><time>{e(x["date"])}</time><div>{x["text"]}</div></li>' for x in p["ledger"])
    paras = "".join(f"<p>{e(x)}</p>" for x in p["paras"])
    quote = f'<p class="quote">{e(p["quote"])}</p>' if p.get("quote") else ""
    pres = _sheet("presentation", p["margin"], p.get("sub"), f'<h2>{e(p["title"])}</h2>{paras}{quote}<ol class="ledger" aria-label="Filiation de l\'étude">{lis}</ol>')

    k = d["competences"]
    arts = "".join(f'<article><h3>{e(x["title"])}</h3><p>{e(x["text"])}</p></article>' for x in k["items"])
    il = f'<p class="inline-list">{e(k["list"])}</p>' if k.get("list") else ""
    comp = _sheet("competences", k["margin"], k.get("sub"), f'<h2>{e(k["title"])}</h2><div class="arts">{arts}</div>{il}')

    rows = "".join(f"<tr><th scope=\"row\">{e(r[0])}</th><td>{e(r[1])}</td></tr>" for r in c["hours"])
    pr = _sheet("contact", "Informations pratiques", c.get("sub"), f'''<h2>{e(c["title"])}</h2><div class="prat"><div>
<p class="coord">{e(c["name"])}<br>{e(c["address"])}<br>Tél. <a href="tel:{a(c["tel"])}">{e(c["phone"])}</a><br>
<a href="mailto:{a(c["email"])}">{e(c["email"])}</a></p><table>{rows}</table>
<div class="ctas" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:24px"><a class="btn full" href="{a(rdv[1])}"{tgt(rdv[1])}>{e(rdv[0])}</a>
<a class="btn" href="mailto:{a(c["email"])}">Demander un rendez-vous par e-mail</a></div></div>{map_iframe(c["map_q"])}</div>''')

    n = d.get("news")
    news = ""
    if n:
        items = "".join(f"<li>{e(x)}</li>" for x in n["titles"])
        news = _sheet("informations", n["margin"], n.get("sub"), f'''<h2>{e(n["title"])}</h2><p>{e(n.get("text", ""))}</p>
<ul class="news">{items}</ul><p style="margin-top:20px"><a class="btn" href="{a(n["url"])}"{tgt(n["url"])}>Lire les actualités juridiques sur le site actuel</a></p>''')
    lk = d.get("useful")
    useful = ""
    if lk:
        ul = "".join(f'<li><a href="{a(u)}"{tgt(u)}>{e(l)}</a></li>' for l, u in lk["items"])
        useful = _sheet("liens", lk["margin"], None, f'<h2>{e(lk["title"])}</h2><ul class="links2">{ul}</ul>')

    f = d["footer"]
    legal = "<br>".join(e(x) for x in f["legal"])
    foot = f'''<footer class="ft"><div class="w"><div class="g"><div><h3>{e(d["brand"])}</h3><p>{e(f["about"])}</p></div>
<div><h3>Nous joindre</h3><p>{e(c["address"])}<br><a href="tel:{a(c["tel"])}">{e(c["phone"])}</a><br><a href="mailto:{a(c["email"])}">{e(c["email"])}</a></p></div>
<div><h3>Profession réglementée</h3><p>{e(f["chamber"])}</p></div></div><p class="legal">{legal}</p></div></footer>'''
    body = head + "<main>" + hero + pres + comp + pr + news + useful + "</main>" + foot
    return page(d, css, body, t["fonts"], JS)
