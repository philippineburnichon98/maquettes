"""Style « établi » — l'atelier du menuisier, de l'ébéniste ou du charpentier.

Fond clair de bois raboté, titres en grotesque large, légendes en machine à écrire comme les
étiquettes posées sur les pièces en atelier (lieu + description). Navigation en mètre pliant
(segments jaunes gradués), réalisations rangées par ouvrage, avec pour chaque chantier le
lieu en étiquette. Élément mémorable : le comparateur avant/après que l'on fait glisser,
chantier par chantier.

Paramétrage (d["theme"]) : bg, ink, wood, deep, rule (jaune du mètre), soft, fonts, display,
mono (familles CSS), opening ("atelier" : titre et photo côte à côte ; "plein" : photo pleine
largeur sous le titre).
"""
from core import e, a, tgt, logo, map_iframe, page

CSS = """
:root{--bg:%(bg)s;--ink:%(ink)s;--wood:%(wood)s;--deep:%(deep)s;--rule:%(rule)s;--soft:%(soft)s;--display:%(display)s;--mono:%(mono)s}
body{background:var(--bg);color:var(--ink);font:400 1.02rem/1.62 var(--display);overflow-x:hidden}
.w{max-width:1220px;margin:0 auto;padding:0 22px}
h1,h2,h3{font-family:var(--display);font-weight:800;line-height:1.02;letter-spacing:-.02em}
h2{font-size:clamp(2rem,4.8vw,3.4rem);margin-bottom:16px}
h3{font-size:1.35rem;margin-bottom:8px}
.mono{font-family:var(--mono);font-size:.82rem;letter-spacing:.02em}
.btn{display:inline-block;padding:13px 22px;background:var(--deep);color:#fff;border:2px solid var(--deep);font-weight:700;text-decoration:none;border-radius:3px}
.btn:hover{background:var(--wood);border-color:var(--wood);color:var(--ink)}
.btn.light{background:transparent;color:var(--deep)}.btn.light:hover{background:var(--rule);border-color:var(--rule);color:var(--ink)}
header{background:var(--bg);position:sticky;top:0;z-index:50;box-shadow:0 1px 0 rgba(0,0,0,.08)}
.top{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:70px}
.top .logo-img{max-width:min(260px,58vw);object-fit:contain}
.logo-txt{font-weight:800;font-size:1.15rem}
.top .call{font-weight:700;text-decoration:none;white-space:nowrap}
/* mètre pliant */
.metre{background:var(--rule);border-top:2px solid var(--ink);border-bottom:2px solid var(--ink);overflow-x:auto;scrollbar-width:none}
.metre::-webkit-scrollbar{display:none}
.metre ol{list-style:none;display:flex;min-width:max-content;max-width:1220px;margin:0 auto}
.metre li{flex:1 0 auto;border-right:2px solid var(--ink);position:relative}
.metre li:first-child{border-left:2px solid var(--ink)}
.metre a{display:block;padding:16px 18px 9px;font:600 .9rem var(--mono);text-decoration:none;color:var(--ink);white-space:nowrap;
background-image:repeating-linear-gradient(90deg,var(--ink) 0 1px,transparent 1px 10px);background-size:100%% 7px;background-repeat:no-repeat;background-position:0 0}
.metre a:hover,.metre a:focus-visible{background-color:#fff6c9}
.metre li span{position:absolute;right:5px;bottom:2px;font:500 .62rem var(--mono);opacity:.7}
/* ouverture */
.hero{padding:clamp(40px,7vw,90px) 0}
.hero .w{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:clamp(26px,5vw,70px);align-items:center}
.hero h1{font-size:clamp(2.4rem,5.6vw,4.8rem)}
.hero .lead{font-size:1.15rem;max-width:50ch;margin:22px 0 26px}
.hero .ctas{display:flex;flex-wrap:wrap;gap:12px}
.hero figure img{width:100%%;aspect-ratio:4/3;object-fit:cover;background:var(--soft);border-radius:3px}
.hero figcaption,.tag{display:inline-block;margin-top:10px;background:#fff;border:1px solid rgba(0,0,0,.18);padding:3px 9px;font:500 .8rem var(--mono)}
.opening-plein .hero .w{grid-template-columns:minmax(0,1fr)}
.opening-plein .hero figure img{aspect-ratio:21/9}
@media(max-width:860px){.hero .w{grid-template-columns:minmax(0,1fr)}.opening-plein .hero figure img{aspect-ratio:4/3}}
.facts{display:flex;flex-wrap:wrap;gap:0;margin-top:30px;border-top:2px solid var(--ink)}
.facts div{flex:1 1 160px;padding:12px 16px 0 0}.facts b{display:block;font-size:1.5rem;font-weight:800}.facts small{display:block;font:500 .8rem/1.4 var(--mono)}
/* sections */
section{padding:clamp(60px,9vw,110px) 0}
.alt{background:var(--soft)}
.dark{background:var(--deep);color:#fff}.dark .tag{color:var(--ink)}
.intro{max-width:64ch;margin-bottom:12px}
.cols{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px 50px;margin-top:20px}
@media(max-width:860px){.cols{grid-template-columns:minmax(0,1fr)}}
.block{margin-top:44px}
.block>p{max-width:64ch;margin-bottom:14px}
.shelf{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%%,210px),1fr));gap:18px}
.shelf button{display:block;width:100%%;border:0;padding:0;background:var(--soft);cursor:zoom-in;text-align:left;color:inherit;font:inherit}
.alt .shelf button{background:#fff}
.shelf img{width:100%%;aspect-ratio:4/3;object-fit:cover}
.shelf .cap{display:block;padding:8px 2px 0;font-size:.9rem;line-height:1.35}
.shelf .cap i{display:block;font:normal 500 .74rem var(--mono);opacity:.75;margin-bottom:2px}
.more{margin-top:14px}.more summary{display:inline-block;cursor:pointer;font:600 .85rem var(--mono);padding:8px 14px;border:2px solid currentColor;border-radius:3px;margin-bottom:14px;list-style:none}
.more summary::-webkit-details-marker{display:none}.more[open] summary{background:var(--rule);color:var(--ink);border-color:var(--rule)}
@media(max-width:560px){.shelf{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}}
/* avant/après */
.pairs{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%%,360px),1fr));gap:30px}
.cmp{position:relative;overflow:hidden;aspect-ratio:4/3;background:#2a2a2a;border-radius:3px;--p:50%%;touch-action:pan-y}
.cmp img{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover}
.cmp .after{clip-path:inset(0 0 0 var(--p))}
.cmp .bar{position:absolute;top:0;bottom:0;left:var(--p);width:3px;margin-left:-1px;background:var(--rule);pointer-events:none}
.cmp .bar::after{content:"◂ ▸";position:absolute;top:50%%;left:50%%;transform:translate(-50%%,-50%%);background:var(--rule);color:var(--ink);font:700 .8rem var(--mono);padding:8px 9px;border-radius:999px;white-space:nowrap}
.cmp input{position:absolute;inset:0;width:100%%;height:100%%;opacity:0;cursor:ew-resize;margin:0}
.cmp input:focus-visible+.bar{outline:3px solid #fff}
.cmp .lb1,.cmp .lb2{position:absolute;bottom:10px;background:rgba(0,0,0,.65);color:#fff;font:500 .74rem var(--mono);padding:3px 8px;pointer-events:none}
.cmp .lb1{left:10px}.cmp .lb2{right:10px}
.pair h3{font-size:1.1rem;margin-top:12px}.pair p{font:500 .8rem var(--mono);opacity:.8}
/* RGE */
.rge{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%%,280px),1fr));gap:18px;margin:26px 0 10px}
.rge div{border:2px solid #fff;padding:18px 20px}.rge b{display:block;font:700 1.35rem var(--mono);color:var(--rule)}
.list{list-style:none;columns:2 260px;column-gap:40px;margin-top:16px}.list li{padding:6px 0;border-bottom:1px solid rgba(255,255,255,.25);break-inside:avoid}
/* contact */
.contact .w{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(26px,5vw,60px)}
.contact dl{display:grid;grid-template-columns:110px minmax(0,1fr);gap:10px 16px;margin:22px 0 28px}.contact dt{font:600 .85rem var(--mono);padding-top:2px}.contact dd{overflow-wrap:anywhere}
.contact .map{width:100%%;min-height:380px;height:100%%;border:2px solid var(--ink);background:var(--soft)}
@media(max-width:860px){.contact .w{grid-template-columns:minmax(0,1fr)}.contact dl{grid-template-columns:minmax(0,1fr);gap:2px}.contact dd{margin-bottom:10px}}
footer{background:var(--ink);color:#eee;padding:40px 0 110px;font-size:.9rem}footer .w{display:flex;flex-wrap:wrap;gap:20px 40px;justify-content:space-between}
footer a{color:#fff}footer .logo-txt{color:#fff}footer p{max-width:48ch}
"""


def _shelf(items, first=4):
    if len(items) > first + 1:
        rest = items[first:]
        return (_shelf(items[:first], first=len(items)) +
                f'<details class="more"><summary>Voir les {len(rest)} autres photos</summary>{_shelf(rest, first=len(rest))}</details>')
    out = []
    for it in items:
        src, place, cap = (list(it) + ["", ""])[:3]
        label = " : ".join(x for x in (place, cap) if x)
        out.append(f'<button data-full="{a(src)}" data-cap="{a(label)}" data-alt="{a(label)}" aria-label="Agrandir : {a(label or "photo")}">'
                   f'<img src="{a(src)}" alt="{a(label)}" loading="lazy" referrerpolicy="no-referrer">'
                   f'<span class="cap">{f"<i>{e(place)}</i>" if place else ""}{e(cap)}</span></button>')
    return '<div class="shelf">' + "".join(out) + "</div>"


def _section(s, cls=""):
    blocks = ""
    for b in s.get("blocks", []):
        paras = "".join(f"<p>{e(p)}</p>" for p in b.get("paras", []))
        blocks += f'<div class="block"><h3>{e(b["title"])}</h3>{paras}{_shelf(b.get("items", []))}</div>'
    paras = "".join(f'<p class="intro">{e(p)}</p>' for p in s.get("paras", []))
    return f'<section id="{a(s["id"])}" class="{cls}"><div class="w"><h2>{e(s["title"])}</h2>{paras}{blocks}</div></section>'


def render(d):
    t = d["theme"]
    css = CSS % t
    metre = "".join(f'<li><a href="#{a(i)}">{e(l)}</a><span>{(k + 1) * 10}</span></li>' for k, (i, l) in enumerate(d["nav"]))
    h = d["hero"]
    facts = "".join(f"<div><b>{e(x[0])}</b><small>{e(x[1])}</small></div>" for x in h.get("facts", []))
    pairs = ""
    plist = d.get("pairs", [])
    for k, p in enumerate(plist):
        if k == 6:
            pairs += f'</div><details class="more" style="margin-top:30px"><summary>Voir les {len(plist) - 6} autres avant / après</summary><div class="pairs">'
        pairs += f'''<div class="pair"><div class="cmp"><img src="{a(p["before"])}" alt="Avant : {a(p["title"])}" loading="lazy" referrerpolicy="no-referrer">
<img class="after" src="{a(p["after"])}" alt="Après : {a(p["title"])}" loading="lazy" referrerpolicy="no-referrer">
<input type="range" min="0" max="100" value="50" aria-label="Comparer avant et après : {a(p["title"])}"><span class="bar"></span><span class="lb1">Avant</span><span class="lb2">Après</span></div>
<h3>{e(p["title"])}</h3><p>{e(p["place"])}</p></div>'''
    if len(plist) > 6:
        pairs += '</div></details><div hidden>'
    sections = "".join(_section(s, "alt" if k % 2 == 0 else "") for k, s in enumerate(d["sections"]))
    r = d["rge"]
    certs = "".join(f"<div><b>{e(c[0])}</b>{e(c[1])}</div>" for c in r["certs"])
    rlist = "".join(f"<li>{e(x)}</li>" for x in r["list"])
    rge = f'''<section id="rge" class="dark"><div class="w"><h2>{e(r["title"])}</h2>{"".join(f'<p class="intro">{e(p)}</p>' for p in r["paras"])}
<div class="rge">{certs}</div><ul class="list">{rlist}</ul><div class="block">{_shelf(r["items"])}</div></div></section>'''
    extra = "".join(_section(s, "alt" if k % 2 == 0 else "") for k, s in enumerate(d.get("after_sections", [])))
    before = "".join(_section(s, "alt") for s in d.get("before_sections", []))
    c = d["contact"]
    rows = "".join(f"<dt>{e(k)}</dt><dd>{v}</dd>" for k, v in c["rows"])
    f = d["footer"]
    body = f'''<header id="top"><div class="w top"><a href="#accueil" aria-label="{a(d["brand"])}, retour en haut">{logo(d)}</a><a class="call" href="tel:{a(c["tel_href"])}">{e(c["tel"])}</a></div>
<nav class="metre" aria-label="Navigation principale"><ol>{metre}</ol></nav></header>
<main>
<section class="hero" id="accueil"><div class="w"><div><h1>{e(h["title"])}</h1><p class="lead">{e(h["lead"])}</p>
<div class="ctas"><a class="btn" href="#devis">Demander un devis</a><a class="btn light" href="#avant-apres">Voir les avant / après</a></div><div class="facts">{facts}</div></div>
<figure><img src="{a(h["img"])}" alt="{a(h.get("alt", ""))}" referrerpolicy="no-referrer"><figcaption>{e(h.get("cap", ""))}</figcaption></figure></div></section>
{before}
<section id="avant-apres"><div class="w"><h2>{e(d["pairs_title"])}</h2><p class="intro">{e(d["pairs_lead"])}</p><div class="pairs" style="margin-top:28px">{pairs}</div></div></section>
{sections}
{rge}
{extra}
<section class="contact alt" id="devis"><div class="w"><div><h2>{e(c["title"])}</h2><p class="intro">{e(c["text"])}</p><dl>{rows}</dl>
<div class="ctas" style="display:flex;flex-wrap:wrap;gap:12px"><a class="btn" href="tel:{a(c["tel_href"])}">Appeler pour un devis</a><a class="btn light" href="mailto:{a(c["mail"])}?subject=Demande%20de%20devis">Demander un devis par e-mail</a></div></div>
{map_iframe(c["map_q"])}</div></section>
</main>
<footer><div class="w"><div>{logo(d, 34)}<p style="margin-top:12px">{e(f["about"])}</p></div><p>{"<br>".join(f["lines"])}</p></div></footer>'''
    js = """
document.querySelectorAll('.cmp').forEach(c=>{const r=c.querySelector('input');const s=()=>c.style.setProperty('--p',r.value+'%');r.addEventListener('input',s);s();
c.querySelectorAll('img').forEach(i=>i.addEventListener('error',()=>c.closest('.pair').remove()))});
"""
    html = page(d, css, body, t["fonts"], js)
    return html.replace("<body", f'<body class="opening-{a(t.get("opening", "atelier"))}"', 1)
