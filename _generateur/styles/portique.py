"""Style « portique » — un cabinet d'avocats vu comme une façade de pierre à arcades.

Pour un cabinet installé dans une ville au patrimoine architectural marqué (ici Chambéry :
portiques de la rue de Boigne, fontaine des Éléphants, molasse des façades sardes). Ton sobre,
conforme à la communication réglementée des avocats : pas d'avis, pas de chiffres, pas de promesse.
Élément mémorable : les domaines d'intervention rangés sous une rangée d'arcades en pierre ; chaque
arcade est un bouton qui affiche la description du domaine sous la corniche (accessible au clavier,
aria-expanded). Photos de la ville en bandeau, parcours de l'avocat avec portrait, honoraires
seulement s'ils figurent sur le site d'origine, prise de rendez-vous (lien existant, sinon tel/mailto),
pied de page réglementaire (barreau, forme sociale, SIRET/RCS).

Thème (d["theme"]) : plaster (fond), stone (pierre), green (couleur principale), slate (texte),
bronze (accent rare), ochre (fond secondaire), serif, sans, fonts (URL Google Fonts).
"""
from core import e, a, tgt, logo, map_iframe, page

CSS = """
:root{--plaster:%(plaster)s;--stone:%(stone)s;--green:%(green)s;--slate:%(slate)s;--bronze:%(bronze)s;--ochre:%(ochre)s;
--serif:%(serif)s;--sans:%(sans)s;--muted:color-mix(in srgb,var(--slate) 72%%,var(--plaster))}
body{background:var(--plaster);color:var(--slate);font:400 1.02rem/1.68 var(--sans)}
a{color:var(--green)}
.w{max-width:1180px;margin:0 auto;padding:0 24px}
h1,h2,h3{font-family:var(--serif);font-weight:500;line-height:1.1}
h2{font-size:clamp(2rem,4.2vw,3.1rem);margin-bottom:20px}
header.hd{background:var(--plaster);border-bottom:6px solid var(--stone);position:sticky;top:0;z-index:40}
header.hd .w{display:flex;align-items:center;justify-content:space-between;gap:18px;min-height:76px}
.logo-txt{font-family:var(--serif);font-size:1.45rem;color:var(--slate);font-weight:600;letter-spacing:.01em}
.brand{text-decoration:none}.brand small{display:block;font:500 .8rem var(--sans);color:var(--muted)}
nav.nv{display:flex;gap:24px;font-weight:500;font-size:.95rem}nav.nv a{text-decoration:none;color:var(--slate);white-space:nowrap;padding:6px 0;border-bottom:2px solid transparent}
nav.nv a:hover{border-color:var(--bronze)}
.call{background:var(--green);color:#fff!important;text-decoration:none;font-weight:600;font-size:.92rem;padding:11px 16px;white-space:nowrap}
.call:hover{background:var(--slate)}
.burger{display:none;background:none;border:1px solid var(--slate);padding:8px 12px;font-weight:600;cursor:pointer}
@media(max-width:920px){nav.nv{display:none;position:absolute;left:0;right:0;top:82px;background:var(--plaster);flex-direction:column;gap:0;padding:4px 24px 14px;border-bottom:6px solid var(--stone)}
nav.nv a{padding:12px 0;border-bottom:1px solid var(--stone)}header.open nav.nv{display:flex}.burger{display:block}header.hd .call{display:none}}
/* fronton */
.front{padding:clamp(48px,7vw,90px) 0 0}
.front .w{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:clamp(28px,5vw,64px);align-items:end}
.front .bar{font-weight:600;color:var(--green)}
.front h1{font-size:clamp(2.5rem,6.2vw,4.8rem);margin:12px 0 20px}
.front .lead{font-size:1.15rem;max-width:46ch;color:var(--muted)}
.front .ctas{display:flex;gap:12px;flex-wrap:wrap;margin:28px 0 clamp(30px,5vw,60px)}
.btn{display:inline-block;padding:13px 20px;border:2px solid var(--green);color:var(--green);font-weight:600;text-decoration:none}
.btn.full{background:var(--green);color:#fff}.btn:hover{background:var(--slate);border-color:var(--slate);color:#fff}
.front figure{position:relative}.front figure img{width:100%%;aspect-ratio:4/3;object-fit:cover;border-radius:999px 999px 0 0;background:var(--stone)}
.front figcaption{font-size:.85rem;color:var(--muted);padding:8px 0 0}
.cornice{height:22px;background:var(--stone);border-top:2px solid color-mix(in srgb,var(--stone) 70%%,var(--slate));box-shadow:inset 0 -6px 0 color-mix(in srgb,var(--stone) 80%%,#fff)}
@media(max-width:820px){.front .w{grid-template-columns:minmax(0,1fr)}}
section{padding:clamp(62px,9vw,110px) 0}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(28px,5vw,70px);align-items:start}
.two p{margin-bottom:14px;max-width:62ch}
.two .side{background:var(--ochre);padding:28px 28px 22px;border-top:4px solid var(--bronze)}
.two .side h3{font-size:1.5rem;margin-bottom:10px}
.two .side ul{list-style:none}.two .side li{padding:7px 0;border-bottom:1px solid color-mix(in srgb,var(--stone) 70%%,transparent)}
@media(max-width:820px){.two{grid-template-columns:minmax(0,1fr)}}
/* arcades */
.arcade-wrap{background:var(--ochre)}
.arcade-wrap .intro{max-width:62ch;margin-bottom:34px}
.arcade{display:grid;grid-template-columns:repeat(var(--n),minmax(0,1fr));gap:0;background:var(--stone);padding:16px 16px 0;border-bottom:0}
.arch{appearance:none;border:0;background:var(--plaster);cursor:pointer;margin:0 8px;min-height:230px;border-radius:999px 999px 0 0;
display:flex;flex-direction:column;justify-content:flex-end;align-items:center;text-align:center;padding:60px 14px 22px;position:relative;
box-shadow:inset 0 10px 22px -10px rgba(0,0,0,.28);transition:background .25s}
.arch span{font-family:var(--serif);font-size:1.22rem;line-height:1.2;color:var(--slate)}
.arch::after{content:"";position:absolute;bottom:0;left:50%%;width:28px;height:4px;background:transparent;transform:translateX(-50%%)}
.arch:hover{background:color-mix(in srgb,var(--plaster) 85%%,var(--stone))}
.arch[aria-expanded="true"]{background:var(--green)}.arch[aria-expanded="true"] span{color:#fff}
.arch[aria-expanded="true"]::after{background:var(--bronze)}
.arch:focus-visible{outline:3px solid var(--bronze);outline-offset:-6px}
.panel{background:var(--plaster);border:6px solid var(--stone);border-top:0;padding:30px clamp(20px,4vw,44px)}
.panel h3{font-size:1.7rem;margin-bottom:10px;color:var(--green)}.panel p{max-width:70ch}
.panel[hidden]{display:none}
@media(max-width:820px){.arcade{grid-template-columns:minmax(0,1fr);padding:10px 10px 0}.arch{min-height:0;margin:0 0 10px;border-radius:60px 60px 0 0;padding:26px 14px 16px}}
.lang{margin-top:22px;font-weight:600}
/* avocat */
.bio{display:grid;grid-template-columns:minmax(0,320px) minmax(0,1fr);gap:clamp(28px,5vw,64px);align-items:start}
.bio img{width:100%%;aspect-ratio:4/5;object-fit:cover;border-radius:999px 999px 0 0;background:var(--stone)}
.bio .role{color:var(--green);font-weight:600;margin-bottom:16px}
.steps{list-style:none;margin-top:22px;border-left:3px solid var(--stone)}
.steps li{padding:8px 0 8px 20px;position:relative}.steps li::before{content:"";position:absolute;left:-8px;top:16px;width:13px;height:13px;border-radius:50%%;background:var(--plaster);border:3px solid var(--bronze)}
.steps b{color:var(--green)}
@media(max-width:760px){.bio{grid-template-columns:minmax(0,1fr)}.bio img{max-width:300px}}
/* ville */
.city{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.city button{border:0;padding:0;background:none;cursor:zoom-in;text-align:left}
.city img{width:100%%;aspect-ratio:4/3;object-fit:cover;border-radius:999px 999px 0 0}
.city span{display:block;font-size:.88rem;color:var(--muted);padding-top:8px}
@media(max-width:700px){.city{grid-template-columns:minmax(0,1fr)}}
/* contact */
.ct{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0;border:6px solid var(--stone);background:var(--plaster)}
.ct .in{padding:clamp(26px,4vw,48px)}.ct dl{display:grid;grid-template-columns:130px minmax(0,1fr);gap:10px 18px;margin:20px 0 26px}
.ct dt{font-weight:600}.ct .map{width:100%%;height:100%%;min-height:360px;border:0}
.fees{margin-top:24px;padding:18px 20px;background:var(--ochre);font-size:.95rem}
@media(max-width:820px){.ct{grid-template-columns:minmax(0,1fr)}.ct dl{grid-template-columns:minmax(0,1fr);gap:0}.ct dd{margin-bottom:10px}}
footer.ft{background:var(--slate);color:color-mix(in srgb,var(--plaster) 85%%,var(--slate));padding:52px 0 110px;font-size:.9rem}
footer.ft a{color:#fff}footer.ft .g{display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:30px}footer.ft h3{color:#fff;font-size:1.3rem;margin-bottom:10px}
footer.ft .legal{margin-top:30px;padding-top:16px;border-top:1px solid rgba(255,255,255,.2);font-size:.82rem}
@media(max-width:760px){footer.ft .g{grid-template-columns:minmax(0,1fr)}}
"""

JS = """const H=document.querySelector('header.hd'),B=H.querySelector('.burger');B.onclick=()=>{const o=H.classList.toggle('open');B.setAttribute('aria-expanded',o)};
H.querySelectorAll('nav a').forEach(x=>x.onclick=()=>{H.classList.remove('open');B.setAttribute('aria-expanded',false)});
const A=[...document.querySelectorAll('.arch')];A.forEach(b=>b.onclick=()=>{A.forEach(x=>{const on=x===b;x.setAttribute('aria-expanded',on);document.getElementById(x.getAttribute('aria-controls')).hidden=!on})});"""


def render(d):
    t = d["theme"]
    css = CSS % t
    c = d["contact"]
    rdv = d.get("booking") or [f'Appeler le {c["phone"]}', f'tel:{c["tel"]}']
    nav = "".join(f'<a href="#{i}">{e(l)}</a>' for i, l in d["nav"])
    head = f'''<header class="hd"><div class="w"><a class="brand" href="#cabinet">{logo(d)}<small>{e(d.get("tagline", ""))}</small></a>
<nav class="nv" aria-label="Menu principal">{nav}</nav><a class="call" href="{a(rdv[1])}"{tgt(rdv[1])}>{e(rdv[0])}</a>
<button class="burger" aria-expanded="false" aria-label="Ouvrir le menu">Menu</button></div></header>'''
    h = d["hero"]
    fig = ""
    if h.get("img"):
        fig = f'<figure><img src="{a(h["img"])}" alt="{a(h.get("alt", ""))}" referrerpolicy="no-referrer" onerror="this.parentElement.remove()"><figcaption>{e(h.get("caption", ""))}</figcaption></figure>'
    hero = f'''<section class="front" id="cabinet" style="padding-bottom:0"><div class="w"><div><p class="bar">{e(h["bar"])}</p><h1>{e(h["title"])}</h1>
<p class="lead">{e(h["lead"])}</p><div class="ctas"><a class="btn full" href="{a(rdv[1])}"{tgt(rdv[1])}>{e(rdv[0])}</a>
<a class="btn" href="mailto:{a(c["email"])}">Écrire au cabinet</a></div></div>{fig}</div><div class="cornice"></div></section>'''

    s = d["story"]
    paras = "".join(f"<p>{e(x)}</p>" for x in s["paras"])
    side = s.get("side")
    side_html = ""
    if side:
        side_html = f'<aside class="side"><h3>{e(side["title"])}</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in side["items"])}</ul></aside>'
    story = f'<section id="conseiller"><div class="w two"><div><h2>{e(s["title"])}</h2>{paras}</div>{side_html}</div></section>'

    k = d["domains"]
    n = len(k["items"])
    arches = "".join(f'<button class="arch" aria-expanded="{"true" if i == 0 else "false"}" aria-controls="dom-{i}"><span>{e(x["title"])}</span></button>' for i, x in enumerate(k["items"]))
    panels = "".join(f'<div class="panel" id="dom-{i}" role="region" aria-label="{a(x["title"])}"{"" if i == 0 else " hidden"}><h3>{e(x["title"])}</h3><p>{e(x["text"])}</p></div>' for i, x in enumerate(k["items"]))
    lang = f'<p class="lang">{e(k["lang"])}</p>' if k.get("lang") else ""
    dom = f'''<section class="arcade-wrap" id="domaines"><div class="w"><div class="intro"><h2>{e(k["title"])}</h2><p>{e(k.get("lead", ""))}</p></div>
<div class="arcade" style="--n:{n}">{arches}</div>{panels}{lang}</div></section>'''

    p = d["lawyer"]
    steps = "".join(f"<li><b>{e(x[0])}</b> {e(x[1])}</li>" for x in p["steps"])
    pimg = f'<img src="{a(p["img"])}" alt="{a(p["name"])}" referrerpolicy="no-referrer" onerror="this.remove()">' if p.get("img") else ""
    law = f'''<section id="avocat"><div class="w bio"><div>{pimg}</div><div><h2>{e(p["name"])}</h2><p class="role">{e(p["role"])}</p>
{"".join(f"<p>{e(x)}</p>" for x in p["paras"])}<ol class="steps">{steps}</ol></div></div></section>'''

    city = ""
    if d.get("city"):
        cy = d["city"]
        items = "".join(f'<button data-full="{a(x["src"])}" data-cap="{a(x["caption"])}" data-alt="{a(x["caption"])}" aria-label="Agrandir : {a(x["caption"])}"><img src="{a(x["src"])}" alt="{a(x["caption"])}" loading="lazy" referrerpolicy="no-referrer"><span>{e(x["caption"])}</span></button>' for x in cy["photos"])
        city = f'<section id="chambery" style="padding-top:0"><div class="w"><h2>{e(cy["title"])}</h2><div class="city">{items}</div></div></section>'

    rows = "".join(f"<dt>{e(r[0])}</dt><dd>{r[1]}</dd>" for r in c["rows"])
    fees = f'<p class="fees"><strong>Honoraires.</strong> {e(c["fees"])}</p>' if c.get("fees") else ""
    ct = f'''<section id="contact" style="padding-top:0"><div class="w"><div class="ct"><div class="in"><h2>{e(c["title"])}</h2><p>{e(c.get("text", ""))}</p>
<dl>{rows}</dl><div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn full" href="{a(rdv[1])}"{tgt(rdv[1])}>{e(rdv[0])}</a>
<a class="btn" href="mailto:{a(c["email"])}">Demander un rendez-vous par e-mail</a></div>{fees}</div>{map_iframe(c["map_q"])}</div></div></section>'''

    f = d["footer"]
    foot = f'''<footer class="ft"><div class="w"><div class="g"><div><h3>{e(d["brand"])}</h3><p>{e(f["about"])}</p></div>
<div><h3>Nous joindre</h3><p>{e(c["address"])}<br><a href="tel:{a(c["tel"])}">{e(c["phone"])}</a><br><a href="mailto:{a(c["email"])}">{e(c["email"])}</a></p></div>
<div><h3>Profession réglementée</h3><p>{e(f["bar"])}</p><p><a href="{a(f["bar_url"])}"{tgt(f["bar_url"])}>{e(f["bar_label"])}</a></p></div></div>
<p class="legal">{"<br>".join(e(x) for x in f["legal"])}</p></div></footer>'''
    body = head + "<main>" + hero + story + dom + law + city + ct + "</main>" + foot
    return page(d, css, body, t["fonts"], JS)
