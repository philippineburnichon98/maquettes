"""Style « affiche » — affiche d'exposition, couleurs franches, typographie énorme.
Pour un lieu au ton audacieux. Ouverture en affiche, bandeau défilant (plats, produits),
carte en catalogue, menu en bloc couleur, équipe présentée comme un générique, galerie en mosaïque.
"""
from core import e, a, tgt, logo, map_iframe, page

FONTS = "https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter+Tight:wght@400;500;600&display=swap"

CSS = """
:root{--blue:%(blue)s;--sun:%(sun)s;--paper:%(paper)s;--ink:%(ink)s;--muted:%(muted)s;--rule:rgba(27,27,34,.14)}
body{background:var(--paper);color:var(--ink);font:400 1.02rem/1.6 "Inter Tight",system-ui,sans-serif}
.sy{font-family:Syne,sans-serif;font-weight:800;letter-spacing:-.02em;line-height:.95}
.w{max-width:1240px;margin:0 auto;padding:0 22px}
.btn{display:inline-block;padding:14px 24px;border-radius:999px;background:var(--sun);color:var(--ink);font-weight:600;text-decoration:none;border:2px solid var(--sun)}
.btn:hover{background:var(--ink);border-color:var(--ink);color:#fff}.btn.ghost{background:none;color:#fff;border-color:#fff}.btn.ghost:hover{background:#fff;color:var(--blue)}
header{position:sticky;top:0;z-index:50;background:#fff;border-bottom:2px solid var(--ink)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:18px;height:74px}
.logo-txt{font-family:Syne,sans-serif;font-weight:800;font-size:1.2rem}
nav.links{display:flex;align-items:center;gap:24px;font-weight:500}nav.links a{text-decoration:none}nav.links a:not(.btn):hover{color:var(--blue)}
nav.links .btn{padding:10px 18px}
.burger{display:none;background:var(--ink);color:#fff;border:0;padding:9px 14px;border-radius:999px;font-weight:600;cursor:pointer}
@media(max-width:900px){nav.links{display:none;position:absolute;top:74px;left:0;right:0;flex-direction:column;align-items:stretch;gap:0;background:#fff;padding:8px 22px 18px;border-bottom:2px solid var(--ink)}
nav.links a{padding:13px 0;border-bottom:1px solid var(--rule)}nav.links .btn{margin-top:10px;text-align:center}header.open nav.links{display:flex}.burger{display:block}}
.poster{background:var(--blue);color:#fff;overflow:hidden}
.poster .w{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:clamp(24px,4vw,60px);align-items:end;padding-top:clamp(40px,7vw,90px);padding-bottom:clamp(40px,7vw,90px)}
.poster h1{font-size:clamp(3rem,7.6vw,7rem);hyphens:manual}
.poster h1 .amp{color:var(--sun);display:inline-block;font-weight:600}
.poster p{font-size:1.15rem;max-width:44ch;margin:28px 0 30px;opacity:.95}
.poster .ctas{display:flex;gap:12px;flex-wrap:wrap}
.arch{position:relative}
.arch img{width:100%%;aspect-ratio:3/4;object-fit:cover;border-radius:999px 999px 0 0;background:#3a55d6}
.seal{position:absolute;left:-26px;bottom:34px;width:132px;height:132px;border-radius:50%%;background:var(--sun);color:var(--ink);display:grid;place-items:center;text-align:center;font:700 .8rem/1.15 Syne,sans-serif;padding:16px;transform:rotate(-10deg)}
@media(max-width:860px){.poster .w{grid-template-columns:minmax(0,1fr)}.arch{max-width:420px}.seal{left:auto;right:-6px;width:110px;height:110px}}
.marquee{background:var(--sun);border-bottom:2px solid var(--ink);overflow:hidden;white-space:nowrap}
.marquee div{display:inline-block;padding:16px 0;font:700 1.35rem Syne,sans-serif;animation:mq 50s linear infinite}
.marquee span{margin:0 22px}.marquee span::after{content:"✳";margin-left:44px;color:var(--blue)}
.marquee:hover div{animation-play-state:paused}
@keyframes mq{to{transform:translateX(-50%%)}}
section{padding:clamp(70px,10vw,120px) 0}
h2.t{font-size:clamp(2.4rem,6vw,5rem)}
.maison{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:clamp(28px,5vw,80px);align-items:center}
.maison p{margin-top:16px;max-width:56ch}
.duo{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px}.duo img{width:100%%;aspect-ratio:3/4;object-fit:cover;background:#ddd}.duo img:last-child{margin-top:60px}
@media(max-width:860px){.maison{grid-template-columns:minmax(0,1fr)}}
/* carte */
.carte{background:#fff;border-top:2px solid var(--ink);border-bottom:2px solid var(--ink)}
.carte .top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:20px;margin-bottom:46px}
.carte .top p{max-width:46ch;color:var(--muted)}
.cat{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:46px 60px}
.cat h3{font:800 clamp(1.8rem,3.4vw,2.6rem)/1 Syne,sans-serif;color:var(--blue);margin-bottom:14px}
.cat ul{list-style:none}.cat li{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding:10px 0;border-bottom:1px solid var(--rule)}
.cat li b{font-weight:500}.cat li span{font-weight:600;white-space:nowrap}
@media(max-width:760px){.cat{grid-template-columns:minmax(0,1fr)}}
.formule{margin-top:60px;background:var(--sun);padding:clamp(26px,5vw,54px);display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.3fr);gap:30px;align-items:center}
.formule .p{font:800 clamp(3rem,8vw,6rem)/.9 Syne,sans-serif}.formule .p small{display:block;font:600 1rem "Inter Tight",sans-serif;margin-top:10px}
.formule h3{font:800 1.8rem Syne,sans-serif;margin-bottom:10px}.formule li{margin:6px 0 0 18px}
@media(max-width:760px){.formule{grid-template-columns:minmax(0,1fr)}}
.carte .note{margin-top:26px;color:var(--muted);font-size:.92rem}
/* équipe */
.credits{text-align:center}
.credits p.k{color:var(--muted);margin-bottom:26px}
.credits ul{list-style:none}.credits li{font:800 clamp(1.8rem,5vw,3.6rem)/1.15 Syne,sans-serif}
.credits li small{display:block;font:500 1rem "Inter Tight",sans-serif;color:var(--blue);margin:4px 0 22px}
.mosaic{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:220px;gap:10px;margin-top:34px}
.mosaic button{border:0;padding:0;background:#ddd;cursor:zoom-in;overflow:hidden}.mosaic img{width:100%%;height:100%%;object-fit:cover}
.mosaic button:nth-child(1){grid-column:span 2;grid-row:span 2}.mosaic button:nth-child(6){grid-column:span 2}
@media(max-width:760px){.mosaic{grid-template-columns:1fr 1fr;grid-auto-rows:160px}.mosaic button:nth-child(6){grid-column:span 1}}
.labels{display:flex;flex-wrap:wrap;gap:12px;margin-top:22px}.labels span{border:2px solid var(--ink);border-radius:999px;padding:8px 16px;font-weight:600}
.infos{background:var(--blue);color:#fff}
.infos .w{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(28px,5vw,60px)}
.infos dl{display:grid;grid-template-columns:110px minmax(0,1fr);gap:12px 16px;margin:26px 0}.infos dt{opacity:.75}.infos dd{overflow-wrap:anywhere}
.infos .map{width:100%%;min-height:380px;height:100%%;border:0;border:2px solid #fff}
@media(max-width:820px){.infos .w{grid-template-columns:minmax(0,1fr)}.infos dl{grid-template-columns:1fr;gap:2px}.infos dd{margin-bottom:10px}}
footer{background:var(--ink);color:#ddd;padding:38px 0 100px;font-size:.9rem}footer .w{display:flex;flex-wrap:wrap;justify-content:space-between;gap:20px}footer .logo-txt{color:#fff}
"""


def render(d):
    css = CSS % d["theme"]
    nav = "".join(f'<a href="#{i}">{e(l)}</a>' for i, l in d["nav"]) + '<a class="btn" href="#infos">Réserver</a>'
    h = d["hero"]
    title = e(h["title"]).replace("&amp;", '<span class="amp">&amp;</span>')
    mq = "".join(f"<span>{e(x)}</span>" for x in d["marquee"]) * 2
    m = d["maison"]
    c = d["carte"]
    cats = ""
    for sec in c["sections"]:
        cats += f'<div><h3>{e(sec["title"])}</h3><ul>' + "".join(
            f'<li><b>{e(it[0])}</b><span>{e(it[1]) if len(it) > 1 else ""}</span></li>' for it in sec["items"]) + "</ul></div>"
    f = c["formule"]
    fl = "".join(f"<li>{e(x)}</li>" for x in f["choices"])
    team = "".join(f'<li>{e(p[0])}<small>{e(p[1])}</small></li>' for p in d["team"]["people"])
    mos = "".join(f'<button data-full="{a(p["full"])}" aria-label="Agrandir la photo"><img src="{a(p["thumb"])}" alt="" loading="lazy" referrerpolicy="no-referrer"></button>' for p in d["photos"])
    inf = d["infos"]
    rows = "".join(f"<dt>{e(k)}</dt><dd>{v}</dd>" for k, v in inf["rows"])
    labels = "".join(f"<span>{e(x)}</span>" for x in d["labels"])
    body = f'''<header id="top"><div class="w nav"><a href="#accueil" aria-label="{a(d["brand"])}, accueil">{logo(d)}</a>
<nav class="links" aria-label="Navigation principale">{nav}</nav><button class="burger" aria-expanded="false">Menu</button></div></header>
<main>
<section class="poster" id="accueil" style="padding:0"><div class="w"><div><h1 class="sy">{title}</h1><p>{e(h["lead"])}</p>
<div class="ctas"><a class="btn" href="#carte">Voir la carte</a><a class="btn ghost" href="#infos">Réserver une table</a></div></div>
<div class="arch"><img src="{a(h["img"])}" alt="{a(h.get("alt", ""))}" referrerpolicy="no-referrer"><div class="seal">{e(h["seal"])}</div></div></div></section>
<div class="marquee" aria-hidden="true"><div>{mq}</div></div>
<section id="maison"><div class="w maison"><div><h2 class="t sy">{e(m["title"])}</h2>{"".join(f"<p>{p}</p>" for p in m["paras"])}<div class="labels">{labels}</div></div>
<div class="duo"><img src="{a(m["imgs"][0])}" alt="" loading="lazy" referrerpolicy="no-referrer"><img src="{a(m["imgs"][1])}" alt="" loading="lazy" referrerpolicy="no-referrer"></div></div></section>
<section class="carte" id="carte"><div class="w"><div class="top"><h2 class="t sy">{e(c["title"])}</h2><p>{e(c["lead"])}</p></div>
<div class="cat">{cats}</div>
<div class="formule"><div class="p">{e(f["price"])}<small>{e(f["price_label"])}</small></div><div><h3>{e(f["title"])}</h3><p>{e(f["text"])}</p><ul>{fl}</ul></div></div>
<p class="note">{e(c["note"])}</p></div></section>
<section class="credits" id="equipe"><div class="w"><h2 class="t sy" style="margin-bottom:14px">{e(d["team"]["title"])}</h2><p class="k">{e(d["team"]["lead"])}</p><ul>{team}</ul></div></section>
<section id="photos" style="padding-top:0"><div class="w"><h2 class="t sy">{e(d["photos_title"])}</h2><div class="mosaic">{mos}</div></div></section>
<section class="infos" id="infos"><div class="w"><div><h2 class="t sy">{e(inf["title"])}</h2><p style="margin-top:14px;max-width:44ch">{e(inf["text"])}</p><dl>{rows}</dl>
<a class="btn" href="{a(inf["cta"][1])}">{e(inf["cta"][0])}</a></div>{map_iframe(inf["map_q"])}</div></section>
</main>
<footer><div class="w"><div>{logo(d, 30)}<p style="margin-top:10px">{e(d["footer"]["about"])}</p></div><p>{"<br>".join(d["footer"]["contact"])}</p><p style="max-width:34ch">{e(d["footer"]["legal"])}</p></div></footer>'''
    js = """
const H=document.getElementById('top'),B=H.querySelector('.burger');B.onclick=()=>{const o=H.classList.toggle('open');B.setAttribute('aria-expanded',o)};
H.querySelectorAll('nav a').forEach(l=>l.onclick=()=>{H.classList.remove('open');B.setAttribute('aria-expanded',false)});
"""
    return page(d, css, body, FONTS, js)
