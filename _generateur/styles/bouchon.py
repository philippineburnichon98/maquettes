"""Style « bouchon » — nappe à carreaux, ardoise à la craie, carte imprimée.
Pour un bouchon lyonnais ou une brasserie traditionnelle. Vidéo ou photo en ouverture,
ardoise du midi, carte complète sur feuille posée sur la nappe, module de réservation intégré,
cave, groupes, galerie, infos pratiques.
"""
from core import e, a, tgt, logo, map_iframe, page

FONTS = "https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Caveat:wght@500;700&family=Libre+Franklin:wght@400;500;600;700&display=swap"

CSS = """
:root{--red:%(red)s;--white:#fff;--slate:%(slate)s;--chalk:%(chalk)s;--mustard:%(mustard)s;--ink:%(ink)s;--muted:%(muted)s;--rule:rgba(0,0,0,.12)}
body{background:var(--white);color:var(--ink);font:400 1rem/1.6 "Libre Franklin",system-ui,sans-serif}
.slab{font-family:"Alfa Slab One",Rockwell,serif;font-weight:400;line-height:1.02}
.gingham{background-color:#fff;background-image:linear-gradient(90deg,rgba(180,35,44,.5) 50%%,transparent 50%%),linear-gradient(rgba(180,35,44,.5) 50%%,transparent 50%%);background-size:28px 28px}
.strip{height:10px}
.w{max-width:1200px;margin:0 auto;padding:0 22px}
.btn{display:inline-block;padding:13px 22px;background:var(--red);color:#fff;text-decoration:none;font-weight:600;border:2px solid var(--red);border-radius:3px}
.btn:hover{background:#8f1a22;border-color:#8f1a22}.btn.line{background:none;color:var(--ink);border-color:var(--ink)}.btn.line:hover{background:var(--ink);color:#fff}
header{position:sticky;top:0;z-index:50;background:#fff;border-bottom:1px solid var(--rule)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:18px;height:76px}
.logo-txt{font-family:"Alfa Slab One",serif;font-size:1.3rem;color:var(--red)}
nav.links{display:flex;align-items:center;gap:22px;font-weight:500;font-size:.95rem}nav.links a{text-decoration:none}nav.links a:not(.btn):hover{color:var(--red)}
.burger{display:none;background:none;border:2px solid var(--ink);padding:7px 12px;font-weight:600;cursor:pointer}
@media(max-width:900px){nav.links{display:none;position:absolute;top:76px;left:0;right:0;flex-direction:column;align-items:stretch;gap:0;background:#fff;padding:8px 22px 18px;border-bottom:1px solid var(--rule)}
nav.links a{padding:12px 0;border-bottom:1px solid var(--rule)}nav.links .btn{margin-top:10px;text-align:center}header.open nav.links{display:flex}.burger{display:block}}
.hero{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:clamp(24px,4vw,56px);padding:clamp(36px,6vw,70px) 0;align-items:center}
.hero h1{font-size:clamp(2.6rem,6.4vw,5.4rem);color:var(--red)}
.hero p.lead{font-size:1.15rem;margin:20px 0 26px;max-width:46ch}
.hero .ctas{display:flex;gap:12px;flex-wrap:wrap}
.media{position:relative;border:10px solid #fff;outline:1px solid var(--rule);box-shadow:14px 14px 0 var(--red)}
.media video,.media img{width:100%%;aspect-ratio:4/5;object-fit:cover;background:#ddd}
@media(max-width:860px){.hero{grid-template-columns:minmax(0,1fr)}.media{box-shadow:8px 8px 0 var(--red)}.media video,.media img{aspect-ratio:4/3}}
.ardoise{margin-top:34px;background:var(--slate);color:var(--chalk);padding:24px 26px 20px;border:9px solid #8a6a43;border-radius:4px;max-width:440px;box-shadow:inset 0 0 40px rgba(0,0,0,.35)}
.ardoise h2{font-family:Caveat,cursive;font-weight:700;font-size:2rem;line-height:1}
.ardoise .when{font-family:Caveat,cursive;font-size:1.25rem;opacity:.8;margin-bottom:10px}
.ardoise ul{list-style:none;font-family:Caveat,cursive;font-size:1.5rem}
.ardoise li{display:flex;justify-content:space-between;gap:12px;border-bottom:1px dashed rgba(236,236,228,.3);padding:3px 0}
.facts{background:var(--ink);color:#fff}
.facts ul{list-style:none;display:flex;flex-wrap:wrap;justify-content:center;gap:10px 34px;padding:18px 22px;font-weight:500;font-size:.95rem}
.facts li::before{content:"";display:inline-block;width:8px;height:8px;background:var(--red);margin-right:10px;vertical-align:middle;border-radius:50%%}
section{padding:clamp(64px,9vw,110px) 0}
h2.big{font-size:clamp(2.1rem,4.6vw,3.6rem);color:var(--ink)}
.story{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:clamp(28px,5vw,70px);align-items:center}
.story img{width:100%%;aspect-ratio:1;object-fit:cover;background:#ddd}
.story p{margin-top:16px;max-width:60ch}.story .sig{font-family:Caveat,cursive;font-size:1.7rem;color:var(--red);margin-top:18px}
@media(max-width:820px){.story{grid-template-columns:minmax(0,1fr)}}
/* carte */
.carte{padding:clamp(40px,7vw,90px) 0}
.sheet{max-width:860px;margin:0 auto;background:#fffdf8;color:var(--ink);padding:clamp(28px,5vw,64px);box-shadow:0 30px 60px -30px rgba(0,0,0,.45);position:relative}
.sheet>header{position:static;border:0;text-align:center;margin-bottom:26px;background:none}
.sheet h2{font-size:clamp(2.2rem,5vw,3.4rem);color:var(--red)}.sheet .sub{color:var(--muted);margin-top:6px}
.sheet h3{font-family:"Alfa Slab One",serif;font-weight:400;font-size:1.25rem;color:var(--red);margin:30px 0 8px;text-align:center}
.dish{display:flex;align-items:baseline;gap:8px;padding:6px 0}
.dish span:first-child{font-weight:500}.dish i{flex:1;border-bottom:2px dotted rgba(0,0,0,.25);transform:translateY(-4px)}.dish small{color:var(--muted);white-space:nowrap}
.stamp{margin:34px auto 0;max-width:420px;border:3px solid var(--red);padding:18px 22px;text-align:center;transform:rotate(-1.5deg);color:var(--red)}
.stamp b{font-family:"Alfa Slab One",serif;font-weight:400;font-size:1.6rem;display:block}.stamp p{color:var(--ink);font-size:.93rem;margin-top:6px}
.sheet .note{text-align:center;color:var(--muted);font-size:.88rem;margin-top:22px}
/* cave */
.cave{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.3fr);gap:clamp(28px,5vw,70px)}
.cave table{width:100%%;border-collapse:collapse;font-size:.97rem}
.cave th{text-align:left;font-weight:500;padding:11px 0;border-bottom:1px solid var(--rule)}.cave td{text-align:right;padding:11px 0;border-bottom:1px solid var(--rule);white-space:nowrap;color:var(--muted)}
@media(max-width:820px){.cave{grid-template-columns:minmax(0,1fr)}}
/* réservation */
.resa{background:var(--chalk)}
.resa .box{max-width:780px;margin:30px auto 0;background:#fff;border:1px solid var(--rule);padding:10px}
.resa iframe{display:block;width:100%%;height:680px;border:0}
.resa .fb{text-align:center;margin-top:14px;color:var(--muted);font-size:.9rem}
/* groupes */
.groups{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:clamp(28px,5vw,70px);align-items:start}
.groups ul{list-style:none;margin-top:22px}.groups li{padding:12px 0;border-bottom:1px solid var(--rule)}
.groups .cap{font-family:"Alfa Slab One",serif;font-size:clamp(3rem,8vw,5.5rem);color:var(--red);line-height:1}
@media(max-width:820px){.groups{grid-template-columns:minmax(0,1fr)}}
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px;margin-top:30px}
.gal button{border:0;padding:0;background:#ddd;cursor:zoom-in;aspect-ratio:1}.gal img{width:100%%;height:100%%;object-fit:cover}
/* infos */
.infos{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);border:2px solid var(--ink)}
.infos .in{padding:clamp(26px,5vw,52px)}.infos dl{display:grid;grid-template-columns:110px minmax(0,1fr);gap:12px 16px;margin:22px 0}
.infos dt{font-weight:600}.infos dd{overflow-wrap:anywhere}
.map{width:100%%;height:100%%;min-height:380px;border:0}
@media(max-width:820px){.infos{grid-template-columns:minmax(0,1fr)}.infos dl{grid-template-columns:1fr;gap:2px}.infos dd{margin-bottom:10px}}
footer{background:var(--ink);color:#e9e5df;padding:40px 0 100px;font-size:.9rem}footer .w{display:flex;flex-wrap:wrap;justify-content:space-between;gap:20px}
footer a{color:#fff}footer .logo-txt{color:#fff}
"""


def render(d):
    css = CSS % d["theme"]
    nav = "".join(f'<a href="#{i}">{e(l)}</a>' for i, l in d["nav"]) + f'<a class="btn" href="#reserver">Réserver</a>'
    h = d["hero"]
    media = (f'<video autoplay muted loop playsinline poster="{a(h["poster"])}" aria-label="{a(h.get("media_alt", ""))}"><source src="{a(h["video"])}" type="video/mp4"></video>'
             if h.get("video") else f'<img src="{a(h["poster"])}" alt="{a(h.get("media_alt", ""))}" referrerpolicy="no-referrer">')
    ard = d.get("ardoise")
    ardoise = ""
    if ard:
        lis = "".join(f'<li><span>{e(x[0])}</span><span>{e(x[1])}</span></li>' for x in ard["items"])
        ardoise = f'<div class="ardoise"><h2>{e(ard["title"])}</h2><p class="when">{e(ard["when"])}</p><ul>{lis}</ul></div>'
    facts = "".join(f"<li>{e(f)}</li>" for f in d["facts"])
    s = d["story"]
    m = d["menu"]
    secs = ""
    for sec in m["sections"]:
        secs += f'<h3>{e(sec["title"])}</h3>' + "".join(
            f'<div class="dish"><span>{e(it[0])}</span><i></i><small>{e(it[1]) if len(it) > 1 else ""}</small></div>' for it in sec["items"])
    st = m.get("stamp")
    stamp = f'<div class="stamp"><b>{e(st["title"])}</b><span class="slab" style="font-size:2.4rem;display:block">{e(st["price"])}</span><p>{e(st["text"])}</p></div>' if st else ""
    cave = d["cave"]
    rows = "".join(f'<tr><th scope="row">{e(r[0])}</th><td>{e(r[1])}</td></tr>' for r in cave["rows"])
    g = d["groups"]
    gl = "".join(f"<li>{e(x)}</li>" for x in g["items"])
    gal = "".join(f'<button data-full="{a(p)}" aria-label="Agrandir la photo"><img src="{a(p)}" alt="" loading="lazy" referrerpolicy="no-referrer"></button>' for p in d["photos"])
    inf = d["infos"]
    irows = "".join(f"<dt>{e(k)}</dt><dd>{v}</dd>" for k, v in inf["rows"])
    b = d["booking"]
    body = f'''<div class="strip gingham" aria-hidden="true"></div>
<header id="top"><div class="w nav"><a href="#accueil" aria-label="{a(d["brand"])}, accueil">{logo(d)}</a>
<nav class="links" aria-label="Navigation principale">{nav}</nav><button class="burger" aria-expanded="false">Menu</button></div></header>
<main>
<div class="w hero" id="accueil"><div><h1 class="slab">{e(h["title"])}</h1><p class="lead">{e(h["lead"])}</p>
<div class="ctas"><a class="btn" href="#reserver">Réserver une table</a><a class="btn line" href="#carte">Voir la carte</a></div>{ardoise}</div>
<div class="media">{media}</div></div>
<div class="facts"><ul>{facts}</ul></div>
<section id="maison"><div class="w story"><img src="{a(s["img"])}" alt="{a(s.get("alt", ""))}" loading="lazy" referrerpolicy="no-referrer">
<div><h2 class="big slab">{e(s["title"])}</h2>{"".join(f"<p>{p}</p>" for p in s["paras"])}<p class="sig">{e(s.get("sign", ""))}</p></div></div></section>
<section class="carte gingham" id="carte"><div class="w"><div class="sheet"><header><h2 class="slab">{e(m["title"])}</h2><p class="sub">{e(m["sub"])}</p></header>
{secs}{stamp}<p class="note">{e(m.get("note", ""))}</p></div></div></section>
<section id="cave"><div class="w cave"><div><h2 class="big slab">{e(cave["title"])}</h2><p style="margin-top:14px;max-width:46ch">{e(cave["lead"])}</p></div>
<table><caption class="sr">Prix des vins à la bouteille</caption><tbody>{rows}</tbody></table></div></section>
<section class="resa" id="reserver"><div class="w"><h2 class="big slab" style="text-align:center">{e(b["title"])}</h2><p style="text-align:center;margin-top:10px">{e(b["lead"])}</p>
<div class="box"><iframe src="{a(b["url"])}" title="Réservation en ligne" loading="lazy"></iframe></div>
<p class="fb">Le module ne s'affiche pas ? <a href="{a(b["url"])}" target="_blank" rel="noopener">Réserver dans un nouvel onglet</a></p></div></section>
<section id="groupes"><div class="w groups"><div><h2 class="big slab">{e(g["title"])}</h2><p style="margin-top:14px;max-width:52ch">{e(g["lead"])}</p><ul>{gl}</ul>
<p style="margin-top:24px"><a class="btn" href="{a(g["cta"][1])}">{e(g["cta"][0])}</a></p></div>
<div><p class="cap">{e(g["capacity"])}</p><p style="margin-top:8px;font-weight:500">{e(g["capacity_label"])}</p><img src="{a(g["img"])}" alt="" loading="lazy" referrerpolicy="no-referrer" style="margin-top:26px;width:100%;aspect-ratio:4/3;object-fit:cover;background:#ddd"></div></div></section>
<section id="photos" style="padding-top:0"><div class="w"><h2 class="big slab">{e(d["photos_title"])}</h2><div class="gal">{gal}</div></div></section>
<section id="infos" style="padding-top:0"><div class="w"><div class="infos"><div class="in"><h2 class="big slab">{e(inf["title"])}</h2><dl>{irows}</dl><a class="btn" href="#reserver">Réserver une table</a></div>{map_iframe(inf["map_q"])}</div></div></section>
</main>
<footer><div class="w"><div>{logo(d, 40)}<p style="margin-top:10px;max-width:40ch">{e(d["footer"]["about"])}</p></div><p>{"<br>".join(d["footer"]["contact"])}</p><p style="max-width:34ch">{e(d["footer"]["legal"])}</p></div></footer>
<div class="strip gingham" aria-hidden="true"></div>'''
    js = """
const H=document.getElementById('top'),B=H.querySelector('.burger');B.onclick=()=>{const o=H.classList.toggle('open');B.setAttribute('aria-expanded',o)};
H.querySelectorAll('nav a').forEach(l=>l.onclick=()=>{H.classList.remove('open');B.setAttribute('aria-expanded',false)});
const v=document.querySelector('.media video');if(v&&matchMedia('(prefers-reduced-motion: reduce)').matches){v.removeAttribute('autoplay');v.pause()}
"""
    return page(d, css, body, FONTS, js)
