"""Style « chrono » — hommage à la chronophotographie de Marey et aux étiquettes noires.
Pour un domaine à forte histoire familiale. Pellicule de photos en ouverture,
cuvées présentées comme des étiquettes avec fiche technique, frise chronologique.
"""
from core import e, a, tgt, logo, map_iframe, page

FONTS = "https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,600;1,6..96,400&family=Karla:wght@300;400;500;600&display=swap"

CSS = """
:root{--chalk:%(chalk)s;--ink:%(ink)s;--black:#000;--stone:%(stone)s;--vine:%(vine)s;--muted:%(muted)s;--rule:rgba(0,0,0,.14)}
body{background:var(--chalk);color:var(--ink);font:400 1.02rem/1.65 Karla,system-ui,sans-serif}
h1,h2,h3,.bod{font-family:"Bodoni Moda",Didot,serif;font-weight:400;line-height:1.05;letter-spacing:-.01em}
.w{max-width:1180px;margin:0 auto;padding:0 24px}
.btn{display:inline-block;padding:13px 24px;border:1px solid var(--ink);text-decoration:none;font-weight:500;font-size:.95rem;transition:background .2s,color .2s}
.btn.fill{background:var(--ink);color:var(--chalk)}.btn:hover{background:var(--ink);color:var(--chalk)}.btn.fill:hover{background:var(--vine);border-color:var(--vine)}
header{position:sticky;top:0;z-index:50;background:var(--chalk);border-bottom:1px solid var(--rule)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:20px;height:78px}
.logo-txt{font-family:"Bodoni Moda",serif;font-size:1.4rem}
nav.links{display:flex;gap:26px;font-size:.93rem}nav.links a{text-decoration:none;padding:6px 0;border-bottom:1px solid transparent}nav.links a:hover{border-color:var(--ink)}
.burger{display:none;background:none;border:1px solid var(--rule);padding:8px 12px;cursor:pointer}
@media(max-width:900px){nav.links{display:none;position:absolute;top:78px;left:0;right:0;flex-direction:column;gap:0;background:var(--chalk);border-bottom:1px solid var(--rule);padding:6px 24px 18px}
nav.links a{padding:13px 0;border-bottom:1px solid var(--rule)}header.open nav.links{display:flex}.burger{display:block}}
/* ouverture */
.hero{padding:clamp(48px,8vw,96px) 0 0}
.hero h1{font-size:clamp(3.2rem,11vw,9.5rem);font-weight:400;letter-spacing:-.03em}
.hero h1 span{display:block;font-style:italic;font-size:.42em;letter-spacing:0;color:var(--muted);margin-top:.35em}
.hero .lead{display:grid;grid-template-columns:1.1fr 1fr;gap:40px;align-items:end;margin-top:34px}
.hero .lead p{font-size:1.15rem;max-width:520px}
.hero .ctas{display:flex;gap:12px;flex-wrap:wrap;justify-content:flex-end}
@media(max-width:760px){.hero .lead{grid-template-columns:1fr}.hero .ctas{justify-content:flex-start}}
.film{margin-top:clamp(40px,6vw,70px);background:var(--black);padding:22px 0;position:relative;overflow:hidden}
.film::before,.film::after{content:"";position:absolute;left:0;right:0;height:10px;background:radial-gradient(circle,#efeeea 2.4px,transparent 2.8px) 0 0/22px 10px repeat-x;opacity:.75}
.film::before{top:5px}.film::after{bottom:5px}
.frames{display:grid;grid-template-columns:repeat(7,minmax(180px,1fr));gap:10px;padding:0 10px;overflow-x:auto;scrollbar-width:none}
.frames figure{position:relative;aspect-ratio:4/3;background:#222;opacity:0;animation:frame .5s ease-out forwards}
.frames figure:nth-child(2){animation-delay:.12s}.frames figure:nth-child(3){animation-delay:.24s}.frames figure:nth-child(4){animation-delay:.36s}.frames figure:nth-child(5){animation-delay:.48s}.frames figure:nth-child(6){animation-delay:.6s}
.frames img{width:100%%;height:100%%;object-fit:cover;filter:grayscale(.15)}
.frames figcaption{position:absolute;left:8px;bottom:6px;color:#efeeea;font:500 .72rem Karla,sans-serif;opacity:.85}
@keyframes frame{to{opacity:1}}
@media(prefers-reduced-motion:reduce){.frames figure{opacity:1}}
section{padding:clamp(70px,10vw,120px) 0}
.intro{display:grid;grid-template-columns:1fr 1.4fr;gap:clamp(30px,6vw,90px)}
.intro h2{font-size:clamp(2rem,4vw,3.2rem)}.intro p{margin-bottom:16px;max-width:62ch}
@media(max-width:800px){.intro{grid-template-columns:1fr}}
/* images ajoutées */
.intro figure img{width:100%%;aspect-ratio:4/3;object-fit:cover;background:#ddd;margin-top:26px}
.band-img{width:100%%;height:clamp(180px,26vw,360px);object-fit:cover;display:block;background:#ccc}
.tl-figs{display:flex;gap:16px;margin:-20px 0 40px}.tl-figs img{height:120px;width:auto;object-fit:contain;filter:grayscale(.2)}
.fams.tabs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:26px}
.fams button{border:1px solid var(--rule);background:#fff;padding:10px;cursor:pointer;text-align:center;font-size:.9rem}
.fams button[aria-pressed="true"]{border-color:var(--ink);box-shadow:inset 0 0 0 1px var(--ink)}
.fams img{width:100%%;height:150px;object-fit:contain;margin-bottom:8px}
@media(max-width:700px){.fams.tabs{grid-template-columns:repeat(2,minmax(0,1fr))}}
.visit .in img.vimg{width:100%%;max-height:260px;object-fit:cover;margin-bottom:22px;background:#ddd}
/* frise */
.timeline h2{font-size:clamp(2rem,4vw,3.2rem);margin-bottom:12px}.timeline>.w>p{color:var(--muted);max-width:60ch;margin-bottom:50px}
.tl{list-style:none;display:grid;grid-template-columns:repeat(5,1fr);border-top:1px solid var(--ink)}
.tl li{padding:20px 22px 0 0;position:relative}
.tl li::before{content:"";position:absolute;top:-5px;left:0;width:9px;height:9px;background:var(--ink);border-radius:50%%}
.tl time{font-family:"Bodoni Moda",serif;font-size:1.5rem;display:block}.tl h3{font-family:Karla,sans-serif;font-weight:600;font-size:1rem;margin:6px 0}
.tl p{font-size:.92rem;color:var(--muted)}
@media(max-width:960px){.tl{grid-template-columns:1fr;border-top:0;border-left:1px solid var(--ink)}.tl li{padding:0 0 30px 24px}.tl li::before{top:10px;left:-5px}}
/* légende */
.legend{background:var(--black);color:#efeeea}
.legend blockquote{font-family:"Bodoni Moda",serif;font-style:italic;font-size:clamp(1.8rem,4.2vw,3.4rem);line-height:1.2;max-width:22ch}
.legend p{margin-top:28px;max-width:56ch;opacity:.75}
/* méthodes */
.methods h2{font-size:clamp(2rem,4vw,3.2rem);max-width:18ch}
.mlist{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin-top:44px;border-top:1px solid var(--rule)}
.mlist div{padding:22px 22px 0 0}.mlist h3{font-family:Karla,sans-serif;font-weight:600;font-size:1.02rem;margin-bottom:6px}.mlist p{color:var(--muted);font-size:.94rem}
@media(max-width:860px){.mlist{grid-template-columns:1fr 1fr;row-gap:24px}}@media(max-width:520px){.mlist{grid-template-columns:1fr}}
/* étiquettes */
.wines h2{font-size:clamp(2.2rem,5vw,4rem)}.wines>.w>p{color:var(--muted);max-width:60ch;margin:12px 0 34px}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:36px}
.tabs button{background:none;border:1px solid var(--rule);padding:9px 16px;cursor:pointer;font-size:.92rem}
.tabs button[aria-pressed="true"]{background:var(--ink);color:var(--chalk);border-color:var(--ink)}
.labels{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:26px}
.lab{display:grid;grid-template-columns:96px 1fr;gap:18px;align-items:start}
.lab .bt{height:250px;display:flex;align-items:flex-end;justify-content:center}.lab .bt img{max-height:250px;width:auto;object-fit:contain}
.lab .bt svg{height:200px}
.tag{border:1px solid var(--ink);padding:5px}
.tag>div{border:1px solid var(--ink);padding:22px 22px 18px;text-align:center}
.lab.noir .tag{background:var(--black);border-color:var(--black);color:#efeeea}.lab.noir .tag>div{border-color:#efeeea}
.tag .ap{font-style:italic;font-family:"Bodoni Moda",serif;font-size:.98rem;opacity:.8}
.tag h3{font-size:1.75rem;margin:6px 0 4px}.tag .mono{font-size:.8rem;letter-spacing:.06em;opacity:.75}
.tag .line{font-family:"Bodoni Moda",serif;font-style:italic;font-size:1.1rem;margin:12px 0 0}
.tag dl{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;text-align:left;font-size:.84rem;margin-top:16px;padding-top:14px;border-top:1px solid currentColor}
.tag dt{opacity:.65}.tag dd{margin:0}
.tag .desc{font-size:.88rem;text-align:left;margin-top:14px;padding-top:12px;border-top:1px solid currentColor}
.lab[hidden]{display:none}
@media(max-width:420px){.lab{grid-template-columns:1fr}.lab .bt{height:160px}.lab .bt img{max-height:160px}}
/* galerie */
.gal h2{font-size:clamp(2rem,4vw,3.2rem);margin-bottom:26px}
.grid{columns:4 220px;column-gap:10px}
.grid button{display:block;width:100%%;border:0;padding:0;margin:0 0 10px;background:#ddd;cursor:zoom-in;break-inside:avoid}
.grid img{width:100%%;height:auto}.grid button[hidden]{display:none}
.more{margin-top:24px;background:none;border:1px solid var(--ink);padding:11px 20px;cursor:pointer}
/* visite */
.visit{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);border:1px solid var(--ink)}
.visit dd{overflow-wrap:anywhere}
.visit .in{padding:clamp(28px,5vw,56px)}
.visit h2{font-size:clamp(2rem,4vw,3rem);margin-bottom:12px}
.visit dl{display:grid;grid-template-columns:110px 1fr;gap:12px 16px;margin:26px 0}
.visit dt{color:var(--muted)}.visit dd a{text-decoration-color:var(--stone)}
.map{width:100%%;height:100%%;min-height:380px;border:0;filter:grayscale(1) contrast(1.05)}
form.mail{display:grid;gap:10px;margin-top:8px}
form.mail label{font-size:.88rem;color:var(--muted)}
form.mail input,form.mail textarea{width:100%%;border:1px solid var(--rule);background:#fff;padding:11px 12px;font:inherit}
form.mail textarea{min-height:110px}
@media(max-width:860px){.visit{grid-template-columns:minmax(0,1fr)}.visit dl{grid-template-columns:1fr;gap:2px}.visit dd{margin-bottom:10px}}
footer{border-top:1px solid var(--ink);padding:44px 0 100px;font-size:.9rem}
footer .w{display:flex;flex-wrap:wrap;justify-content:space-between;gap:24px}footer p{color:var(--muted)}
"""


def bottle(color):
    return (f'<svg viewBox="0 0 40 120" aria-hidden="true"><path d="M16 2h8v30c0 6 10 10 10 22v58a6 6 0 0 1-6 6H12a6 6 0 0 1-6-6V54c0-12 10-16 10-22z" fill="{color}"/>'
            f'<rect x="10" y="66" width="20" height="26" fill="#000"/></svg>')


def render(d):
    t = d["theme"]
    css = CSS % t
    nav = "".join(f'<a href="#{i}">{e(l)}</a>' for i, l in d["nav"])
    h = d["hero"]
    frames = "".join(f'<figure><img src="{a(f)}" alt="" loading="eager" referrerpolicy="no-referrer"><figcaption>{n + 1}</figcaption></figure>'
                     for n, f in enumerate(h["frames"]))
    intro = d["intro"]
    tl = "".join(f'<li><time>{e(x["when"])}</time><h3>{e(x["who"])}</h3><p>{e(x["text"])}</p></li>' for x in d["timeline"]["items"])
    meth = "".join(f'<div><h3>{e(m[0])}</h3><p>{e(m[1])}</p></div>' for m in d["methods"]["items"])
    tabs = '<button aria-pressed="true" data-f="all">Toute la cave</button>' + "".join(
        f'<button aria-pressed="false" data-f="{k}">{e(v)}</button>' for k, v in d["wines"]["tabs"])
    fimgs = d["wines"].get("tab_imgs", {})
    fams = ""
    if fimgs:
        fams = '<div class="fams tabs" role="group" aria-label="Filtrer la cave">' + '<button aria-pressed="true" data-f="all" style="display:none">Toute la cave</button>' + "".join(
            f'<button aria-pressed="false" data-f="{k}"><img src="{a(fimgs[k])}" alt="" loading="lazy" referrerpolicy="no-referrer">{e(v)}</button>' for k, v in d["wines"]["tabs"]) + '</div><p style="margin:-10px 0 26px"><button class="more" type="button" id="allwines" style="margin:0">Voir toute la cave</button></p>'
    labs = []
    for w in d["wines"]["items"]:
        sheet = "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in w.get("sheet", []))
        sheet = f"<dl>{sheet}</dl>" if sheet else ""
        desc = f'<p class="desc">{e(w["desc"])}</p>' if w.get("desc") else ""
        col = "#3b0d15" if w.get("noir") else "#d9c27a"
        img = (f'<img src="{a(w["img"])}" alt="{a(w["name"])}" loading="lazy" referrerpolicy="no-referrer" onerror="this.outerHTML=this.dataset.s" data-s="{a(bottle(col))}">'
               if w.get("img") else bottle(col))
        labs.append(f'''<article class="lab{' noir' if w.get('noir') else ''}" data-cat="{w["cat"]}"><div class="bt">{img}</div>
<div class="tag"><div><p class="ap">{e(w["app"])}</p><h3>{e(w["name"])}</h3>{f'<p class="mono">{e(w["mono"])}</p>' if w.get("mono") else ""}
{f'<p class="line">{e(w["line"])}</p>' if w.get("line") else ""}{sheet}{desc}</div></div></article>''')
    gtabs = "".join(f'<button aria-pressed="{"true" if n == 0 else "false"}" data-g="{k}">{e(v["label"])}</button>' for n, (k, v) in enumerate(d["gallery"]["sets"].items()))
    gimgs = ""
    for k, v in d["gallery"]["sets"].items():
        for p in v["photos"]:
            gimgs += (f'<button data-set="{k}" data-full="{a(p["full"])}" data-alt="{a(p.get("alt", ""))}" data-cap="{a(p.get("alt", ""))}" aria-label="Agrandir la photo">'
                      f'<img src="{a(p["thumb"])}" alt="{a(p.get("alt", ""))}" loading="lazy" referrerpolicy="no-referrer"></button>')
    v = d["visit"]
    rows = "".join(f"<dt>{e(k)}</dt><dd>{val}</dd>" for k, val in v["rows"])
    body = f'''<header id="top"><div class="w nav"><a href="#accueil" aria-label="{a(d["brand"])}, accueil">{logo(d)}</a>
<nav class="links" aria-label="Navigation principale">{nav}</nav><button class="burger" aria-expanded="false">Menu</button></div></header>
<main>
<section class="hero" id="accueil" style="padding-bottom:0"><div class="w"><h1>{e(h["title"])}<span>{e(h["sub"])}</span></h1>
<div class="lead"><p>{e(h["lead"])}</p><div class="ctas"><a class="btn fill" href="{a(h["cta1"][1])}">{e(h["cta1"][0])}</a><a class="btn" href="{a(h["cta2"][1])}">{e(h["cta2"][0])}</a></div></div></div>
<div class="film" aria-label="Le domaine en images"><div class="frames">{frames}</div></div></section>
<section id="domaine"><div class="w intro"><div><h2>{e(intro["title"])}</h2>{f'<figure><img src="{a(intro["img"])}" alt="{a(intro.get("alt", ""))}" loading="lazy" referrerpolicy="no-referrer"></figure>' if intro.get("img") else ""}</div><div>{"".join(f"<p>{p}</p>" for p in intro["paras"])}</div></div></section>
<section class="timeline" id="histoire" style="padding-top:0"><div class="w"><h2>{e(d["timeline"]["title"])}</h2><p>{e(d["timeline"]["lead"])}</p>{('<div class="tl-figs">' + "".join(f'<img src="{a(u)}" alt="" loading="lazy" referrerpolicy="no-referrer">' for u in d["timeline"].get("imgs", [])) + '</div>') if d["timeline"].get("imgs") else ""}<ol class="tl">{tl}</ol></div></section>
<section class="legend"><div class="w"><blockquote>{e(d["legend"]["quote"])}</blockquote><p>{e(d["legend"]["text"])}</p></div></section>
{f'<img class="band-img" src="{a(d["bands"][0])}" alt="" loading="lazy" referrerpolicy="no-referrer">' if d.get("bands") else ""}<section class="methods" id="methodes"><div class="w"><h2>{e(d["methods"]["title"])}</h2><p style="color:var(--muted);max-width:60ch;margin-top:12px">{e(d["methods"]["lead"])}</p><div class="mlist">{meth}</div></div></section>
<section class="wines" id="vins" style="padding-top:0"><div class="w"><h2>{e(d["wines"]["title"])}</h2><p>{e(d["wines"]["lead"])}</p>
{fams if fams else f'<div class="tabs" role="group" aria-label="Filtrer la cave">{tabs}</div>'}<div class="labels">{"".join(labs)}</div>
{f'<p style="color:var(--muted);font-size:.9rem;margin-top:30px">{e(d["wines"]["note"])}</p>' if d["wines"].get("note") else ""}</div></section>
<section class="gal" id="photos" style="padding-top:0"><div class="w"><h2>{e(d["gallery"]["title"])}</h2><div class="tabs" role="group" aria-label="Choisir une série">{gtabs}</div>
<div class="grid">{gimgs}</div><button class="more" type="button">Voir plus de photos</button></div></section>
{f'<img class="band-img" src="{a(d["bands"][1])}" alt="" loading="lazy" referrerpolicy="no-referrer" style="margin-bottom:clamp(60px,9vw,110px)">' if len(d.get("bands", [])) > 1 else ""}<section id="visite" style="padding-top:0"><div class="w"><div class="visit"><div class="in">{f'<img class="vimg" src="{a(v["img"])}" alt="{a(v.get("alt", ""))}" loading="lazy" referrerpolicy="no-referrer">' if v.get("img") else ""}<h2>{e(v["title"])}</h2><p>{e(v["text"])}</p><dl>{rows}</dl>
<form class="mail" data-to="{a(v["email"])}"><label for="f-nom">Votre nom</label><input id="f-nom" name="nom" autocomplete="name" required>
<label for="f-msg">Votre message</label><textarea id="f-msg" name="msg" required placeholder="Par exemple : nous aimerions venir déguster le samedi 14 au matin, à deux."></textarea>
<button class="btn fill" type="submit">Écrire au domaine</button></form></div>{map_iframe(v["map_q"])}</div></div></section>
</main>
<footer><div class="w"><div>{logo(d, 40)}<p style="margin-top:12px">{e(d["footer"]["about"])}</p></div>
<div><p>{"<br>".join(d["footer"]["contact"])}</p></div><p style="max-width:34ch">{e(d["footer"]["legal"])}</p></div></footer>'''
    js = """
const H=document.getElementById('top'),B=H.querySelector('.burger');B.onclick=()=>{const o=H.classList.toggle('open');B.setAttribute('aria-expanded',o)};
H.querySelectorAll('nav a').forEach(l=>l.onclick=()=>{H.classList.remove('open');B.setAttribute('aria-expanded',false)});
document.querySelectorAll('#vins .tabs button').forEach(b=>b.onclick=()=>{document.querySelectorAll('#vins .tabs button').forEach(x=>x.setAttribute('aria-pressed',x===b));
 const f=b.dataset.f;document.querySelectorAll('.lab').forEach(l=>l.hidden=!(f==='all'||l.dataset.cat===f))});
const aw=document.getElementById('allwines');if(aw)aw.onclick=()=>{document.querySelectorAll('#vins .tabs button').forEach(x=>x.setAttribute('aria-pressed',x.dataset.f==='all'));document.querySelectorAll('.lab').forEach(l=>l.hidden=false)};
let gset=document.querySelector('#photos .tabs button').dataset.g,shown=12;const more=document.querySelector('#photos .more');
const gal=()=>{let n=0;document.querySelectorAll('#photos .grid button').forEach(b=>{const ok=b.dataset.set===gset;b.hidden=!(ok&&n<shown);if(ok)n++});more.hidden=n<=shown};
document.querySelectorAll('#photos .tabs button').forEach(b=>b.onclick=()=>{document.querySelectorAll('#photos .tabs button').forEach(x=>x.setAttribute('aria-pressed',x===b));gset=b.dataset.g;shown=12;gal()});
more.onclick=()=>{shown+=12;gal()};gal();
document.querySelectorAll('form.mail').forEach(f=>f.onsubmit=ev=>{ev.preventDefault();const s=encodeURIComponent('Demande de '+f.nom.value);
 location.href='mailto:'+f.dataset.to+'?subject='+s+'&body='+encodeURIComponent(f.msg.value+'\\n\\n'+f.nom.value)});
"""
    return page(d, css, body, FONTS, js)
