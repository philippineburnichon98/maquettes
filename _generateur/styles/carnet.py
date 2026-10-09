"""Style « carnet » — le carnet de chantier de l'artisan (peintre, plâtrier, plombier…).

Page claire posée sur un papier quadrillé ou carrelé (au choix du thème), titres en grosse
linéale et annotations manuscrites comme au crayon. Les prestations sont une liste à cocher,
la zone d'intervention est entourée à la main, les photos de chantier sont scotchées.
Élément mémorable : le « bon de devis » détachable (bord pointillé, ciseaux) avec appel et
e-mail, qui revient en bas de page.

Paramétrage (d["theme"]) : paper, ink, accent, accent2, soft, grid ("quadrille" ou "carrelage"),
fonts (URL Google Fonts), display, body, hand (familles CSS), opening ("liste" ou "photo").
"""
from core import e, a, tgt, logo, map_iframe, page

CSS = """
:root{--paper:%(paper)s;--ink:%(ink)s;--accent:%(accent)s;--accent2:%(accent2)s;--soft:%(soft)s;--line:%(line)s;
--display:%(display)s;--body:%(body)s;--hand:%(hand)s}
body{background:var(--paper);color:var(--ink);font:400 1.03rem/1.62 var(--body);overflow-x:hidden}
body.quadrille{background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:26px 26px}
body.carrelage{background-image:linear-gradient(var(--line) 2px,transparent 2px),linear-gradient(90deg,var(--line) 2px,transparent 2px);background-size:84px 84px}
.w{max-width:1180px;margin:0 auto;padding:0 22px}
h1,h2,h3{font-family:var(--display);line-height:1.02;letter-spacing:-.015em}
h2{font-size:clamp(2.1rem,5vw,3.6rem);margin-bottom:18px}
.hand{font-family:var(--hand);color:var(--accent2);font-size:1.45rem;line-height:1.2}
.btn{display:inline-block;padding:13px 22px;border:2px solid var(--ink);background:var(--ink);color:var(--paper);font-weight:700;text-decoration:none;border-radius:4px}
.btn:hover{background:var(--accent);border-color:var(--accent);color:var(--ink)}
.btn.line{background:transparent;color:var(--ink)}.btn.line:hover{background:var(--accent)}
header{position:sticky;top:0;z-index:50;background:var(--paper);border-bottom:2px solid var(--ink)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:72px}
.nav .logo-img{max-width:min(240px,55vw);object-fit:contain}
.logo-txt{font-family:var(--display);font-weight:800;font-size:1.15rem}
.logo-box{display:inline-flex;align-items:center;padding:6px 10px;border-radius:4px;background:%(logo_bg)s}
nav.links{display:flex;gap:22px;align-items:center;font-weight:600}nav.links a{text-decoration:none}
nav.links a:not(.btn):hover{text-decoration:underline;text-decoration-color:var(--accent);text-decoration-thickness:3px}
nav.links .btn{padding:9px 16px}
.burger{display:none;border:2px solid var(--ink);background:none;padding:8px 13px;font-weight:700;border-radius:4px;cursor:pointer}
@media(max-width:900px){nav.links{display:none;position:absolute;left:0;right:0;top:100%%;flex-direction:column;align-items:stretch;gap:0;background:var(--paper);border-bottom:2px solid var(--ink);padding:6px 22px 18px}
nav.links a{padding:12px 0;border-bottom:1px solid var(--line)}nav.links .btn{margin-top:12px;text-align:center}header.open nav.links{display:flex}.burger{display:block}}
/* ouverture */
.open-hero{padding:clamp(40px,7vw,90px) 0 clamp(50px,7vw,90px)}
.open-hero .w{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:clamp(26px,5vw,70px);align-items:start}
.open-hero h1{font-size:clamp(2.6rem,6.6vw,5.6rem);font-weight:800}
.open-hero h1 mark{background:linear-gradient(transparent 66%%,var(--accent) 66%%,var(--accent) 92%%,transparent 92%%);color:inherit;padding:0 .05em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.opening-photo .open-hero h1{font-size:clamp(2.3rem,5vw,4.2rem)}
.open-hero .lead{font-size:1.15rem;max-width:48ch;margin:22px 0 26px}
.open-hero .ctas{display:flex;flex-wrap:wrap;gap:12px}
.badges{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}.badges span{border:2px solid var(--ink);padding:5px 12px;border-radius:999px;font-weight:600;font-size:.92rem;background:var(--paper)}
.hero-photo{position:relative;margin-top:10px}
.hero-photo img{width:100%%;aspect-ratio:4/5;object-fit:cover;border:8px solid #fff;box-shadow:0 18px 40px -22px rgba(0,0,0,.45);transform:rotate(1.6deg);background:var(--soft)}
.hero-photo .tape{position:absolute;top:-14px;left:38%%;width:110px;height:30px;background:var(--accent);opacity:.82;transform:rotate(-4deg)}
.hero-photo .hand{position:absolute;left:-8px;bottom:-34px;transform:rotate(-3deg);background:var(--paper);padding:2px 8px}
.opening-photo .open-hero{padding-top:0}
.opening-photo .cover{height:clamp(240px,42vw,460px);background:var(--soft) center/cover no-repeat;border-bottom:2px solid var(--ink);position:relative}
.opening-photo .cover::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 40%%,rgba(0,0,0,.35))}
.opening-photo .open-hero .w{margin-top:-70px;position:relative;z-index:2}
.opening-photo .sheet{background:var(--paper);border:2px solid var(--ink);padding:clamp(22px,4vw,44px)}
@media(max-width:860px){.open-hero .w{grid-template-columns:minmax(0,1fr)}.hero-photo{max-width:420px}}
/* bon de devis */
.coupon{position:relative;background:#fff;border:2px dashed var(--ink);padding:26px 24px 22px;border-radius:6px}
.coupon::before{content:"✂";position:absolute;top:-15px;left:18px;background:var(--paper);padding:0 6px;font-size:1.2rem;line-height:1}
.coupon h2,.coupon h3{font-size:1.7rem;margin-bottom:8px}
.coupon p{margin-bottom:14px}
.coupon .tel{display:block;font:800 clamp(1.7rem,3.6vw,2.3rem)/1.1 var(--display);text-decoration:none;margin:6px 0 14px;color:var(--ink)}
.coupon .tel:hover{color:var(--accent2)}
.coupon .row{display:flex;flex-wrap:wrap;gap:10px}
.coupon small{display:block;margin-top:14px;color:var(--ink);opacity:.8}
/* sections */
section{padding:clamp(60px,9vw,110px) 0}
.sheetbg{background:var(--paper);border-top:2px solid var(--ink);border-bottom:2px solid var(--ink)}
.intro{max-width:60ch;margin-bottom:34px}
.todo{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%%,300px),1fr));gap:26px 40px}
.todo h3{font-size:1.45rem;margin-bottom:10px;padding-bottom:8px;border-bottom:3px solid var(--accent);display:inline-block}
.todo ul{list-style:none}
.todo li{position:relative;padding:7px 0 7px 34px;border-bottom:1px dashed var(--line)}
.todo li::before{content:"";position:absolute;left:0;top:10px;width:18px;height:18px;border:2px solid var(--ink);border-radius:3px;background:#fff}
.todo li::after{content:"";position:absolute;left:5px;top:11px;width:7px;height:12px;border:solid var(--accent2);border-width:0 3px 3px 0;transform:rotate(40deg)}
.todo .note{margin-top:28px}
.engage{display:flex;flex-wrap:wrap;gap:14px;margin-top:40px}
.engage div{flex:1 1 220px;border-left:6px solid var(--accent);padding:6px 0 6px 16px}
.engage b{display:block;font-family:var(--display);font-size:1.2rem}
/* zone entourée */
.zone .w{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(26px,5vw,60px);align-items:center}
.ring{position:relative;padding:clamp(56px,9vw,96px) clamp(40px,7vw,80px);text-align:center}
.ring svg{position:absolute;inset:0;width:100%%;height:100%%;overflow:visible}
.ring svg path{fill:none;stroke:var(--accent2);stroke-width:3;stroke-linecap:round}
.ring .c{font:800 clamp(1.8rem,4vw,2.6rem)/1 var(--display);display:block;margin-bottom:12px}
.ring .t{font-size:.95rem;line-height:1.75}
.ring .t span{white-space:nowrap}
.ring .t span:not(:last-child)::after{content:",";margin-right:.35em}
.zone .map{width:100%%;height:360px;border:2px solid var(--ink);background:var(--soft)}
@media(max-width:860px){.zone .w{grid-template-columns:minmax(0,1fr)}}
/* photos scotchées */
.board{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%%,250px),1fr));gap:34px 26px;margin-top:10px}
.board figure{background:#fff;padding:10px 10px 12px;box-shadow:0 14px 30px -20px rgba(0,0,0,.5);position:relative}
.board figure:nth-child(3n+1){transform:rotate(-1.2deg)}.board figure:nth-child(3n+2){transform:rotate(.9deg)}
.board figure::before{content:"";position:absolute;top:-11px;left:50%%;width:84px;height:22px;margin-left:-42px;background:var(--accent);opacity:.75;transform:rotate(-3deg)}
.board button{display:block;width:100%%;border:0;padding:0;background:var(--soft);cursor:zoom-in}
.board img{width:100%%;aspect-ratio:4/3;object-fit:cover}
@media(max-width:560px){.board{grid-template-columns:repeat(2,minmax(0,1fr));gap:24px 14px}.board figure{padding:6px 6px 8px}.board figure::before{width:54px;margin-left:-27px}}
.board figcaption{font-family:var(--hand);font-size:1.2rem;line-height:1.2;margin-top:8px;color:var(--ink)}
/* qui */
.who .w{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:clamp(26px,5vw,70px);align-items:center}
.who img{width:100%%;max-width:380px;aspect-ratio:4/5;object-fit:cover;border:8px solid #fff;box-shadow:0 18px 40px -22px rgba(0,0,0,.45);transform:rotate(-1.5deg);background:var(--soft)}
.who p{margin-bottom:14px;max-width:60ch}
@media(max-width:860px){.who .w{grid-template-columns:minmax(0,1fr)}}
.labels{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}.labels span{background:var(--ink);color:var(--paper);padding:6px 12px;border-radius:4px;font-weight:600;font-size:.92rem}
/* contact */
.contact .w{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(26px,5vw,60px);align-items:start}
.contact dl{display:grid;grid-template-columns:120px minmax(0,1fr);gap:10px 16px;margin-top:10px}.contact dt{font-weight:700}.contact dd{overflow-wrap:anywhere}
@media(max-width:860px){.contact .w{grid-template-columns:minmax(0,1fr)}.contact dl{grid-template-columns:minmax(0,1fr);gap:2px}.contact dd{margin-bottom:10px}}
footer{background:var(--ink);color:var(--paper);padding:40px 0 110px;font-size:.92rem}
footer .w{display:flex;flex-wrap:wrap;gap:22px 40px;justify-content:space-between}
footer p{max-width:46ch}footer a{color:var(--paper)}footer .logo-txt{color:var(--paper)}
"""

RING = ('<svg viewBox="0 0 400 300" preserveAspectRatio="none" aria-hidden="true">'
        '<path d="M206 14C110 10 22 52 16 140c-6 92 92 146 196 144 112-2 176-62 172-140C380 62 300 18 190 22c-30 1-58 6-80 14"/></svg>')


def _coupon(d, tag="h3"):
    c = d["coupon"]
    mail = c.get("mail")
    mail_btn = (f'<a class="btn line" href="mailto:{a(mail)}?subject={a(c.get("subject", "Demande de devis"))}">Demander un devis par e-mail</a>'
                if mail else "")
    return f'''<div class="coupon"><{tag}>{e(c["title"])}</{tag}><p>{e(c["text"])}</p>
<a class="tel" href="tel:{a(c["tel_href"])}">{e(c["tel"])}</a>
<div class="row"><a class="btn" href="tel:{a(c["tel_href"])}">Appeler pour un devis</a>{mail_btn}</div>
{f'<small>{e(c["small"])}</small>' if c.get("small") else ""}</div>'''


def render(d):
    t = d["theme"]
    css = CSS % {**t, "logo_bg": t.get("logo_bg", "transparent")}
    nav = "".join(f'<a href="#{i}">{e(l)}</a>' for i, l in d["nav"]) + '<a class="btn" href="#devis">Demander un devis</a>'
    h = d["hero"]
    title = e(h["title"])
    if h.get("mark"):
        title = title.replace(e(h["mark"]), f'<mark>{e(h["mark"])}</mark>', 1)
    badges = "".join(f"<span>{e(b)}</span>" for b in h.get("badges", []))
    photo = ""
    if h.get("img") and t.get("opening") != "photo":
        photo = (f'<div class="hero-photo"><span class="tape"></span><img src="{a(h["img"])}" alt="{a(h.get("alt", ""))}" referrerpolicy="no-referrer">'
                 f'{f"""<span class="hand">{e(h["note"])}</span>""" if h.get("note") else ""}</div>')
    side = photo if photo else ""
    if t.get("opening") == "photo":
        hero = f'''<div class="cover" style="background-image:url('{a(h["img"])}')" role="img" aria-label="{a(h.get("alt", ""))}"></div>
<section class="open-hero" id="accueil"><div class="w"><div class="sheet"><h1>{title}</h1><p class="lead">{e(h["lead"])}</p>
<div class="ctas"><a class="btn" href="#devis">Demander un devis</a><a class="btn line" href="#prestations">Voir les prestations</a></div><div class="badges">{badges}</div></div>
<div>{_coupon(d)}</div></div></section>'''
    else:
        hero = f'''<section class="open-hero" id="accueil"><div class="w"><div><h1>{title}</h1><p class="lead">{e(h["lead"])}</p>
<div class="ctas"><a class="btn" href="#devis">Demander un devis</a><a class="btn line" href="#prestations">Voir les prestations</a></div><div class="badges">{badges}</div></div>
<div>{side}</div></div></section>'''
    p = d["prestations"]
    groups = "".join(f'<div><h3>{e(g["title"])}</h3><ul>' + "".join(f"<li>{e(x)}</li>" for x in g["items"]) + "</ul></div>" for g in p["groups"])
    engage = "".join(f'<div><b>{e(x[0])}</b>{e(x[1])}</div>' for x in p.get("engage", []))
    pnote = f'<p class="hand note">{e(p["note"])}</p>' if p.get("note") else ""
    z = d.get("zone")
    zone = ""
    if z:
        towns = " ".join(f"<span>{e(x)}</span>" for x in z["towns"])
        zone = f'''<section class="zone" id="zone"><div class="w"><div><h2>{e(z["title"])}</h2><p class="intro">{e(z["text"])}</p>
<div class="ring">{RING}<span class="c">{e(z["center"])}</span><p class="t">{towns}</p></div></div>
{map_iframe(z["map_q"])}</div></section>'''
    ph = d.get("photos")
    photos = ""
    if ph and ph.get("items"):
        figs = "".join(
            f'<figure><button data-full="{a(x["src"])}" data-cap="{a(x.get("cap", ""))}" data-alt="{a(x.get("cap", ""))}" aria-label="Agrandir la photo{(" : " + a(x["cap"])) if x.get("cap") else ""}">'
            f'<img src="{a(x["src"])}" alt="{a(x.get("cap", ""))}" loading="lazy" referrerpolicy="no-referrer"></button>'
            f'{f"""<figcaption>{e(x["cap"])}</figcaption>""" if x.get("cap") else ""}</figure>' for x in ph["items"])
        photos = f'''<section id="chantiers" class="sheetbg"><div class="w"><h2>{e(ph["title"])}</h2><p class="intro">{e(ph.get("lead", ""))}</p><div class="board">{figs}</div></div></section>'''
    wh = d.get("who")
    who = ""
    if wh:
        img = f'<img src="{a(wh["img"])}" alt="{a(wh.get("alt", ""))}" loading="lazy" referrerpolicy="no-referrer">' if wh.get("img") else _coupon(d)
        labels = "".join(f"<span>{e(x)}</span>" for x in d.get("labels", []))
        who = f'''<section class="who" id="artisan"><div class="w"><div>{img}</div><div><h2>{e(wh["title"])}</h2>{"".join(f"<p>{e(x)}</p>" for x in wh["paras"])}
<div class="labels">{labels}</div></div></div></section>'''
    c = d["contact"]
    rows = "".join(f"<dt>{e(k)}</dt><dd>{v}</dd>" for k, v in c["rows"])
    f = d["footer"]
    body = f'''<header id="top"><div class="w nav"><a href="#accueil" class="logo-box" aria-label="{a(d["brand"])}, retour en haut">{logo(d)}</a>
<nav class="links" aria-label="Navigation principale">{nav}</nav><button class="burger" aria-expanded="false" aria-controls="top">Menu</button></div></header>
<main>
{hero}
<section id="prestations" class="sheetbg"><div class="w"><h2>{e(p["title"])}</h2><p class="intro">{e(p["lead"])}</p><div class="todo">{groups}</div>{pnote}<div class="engage">{engage}</div></div></section>
{zone}
{photos}
{who}
<section class="contact" id="devis"><div class="w"><div><h2>{e(c["title"])}</h2><p class="intro">{e(c["text"])}</p><dl>{rows}</dl></div>{_coupon(d, "h3")}</div></section>
</main>
<footer><div class="w"><div>{logo(d, 34)}<p style="margin-top:12px">{e(f["about"])}</p></div><p>{"<br>".join(f["lines"])}</p></div></footer>'''
    js = """
const H=document.getElementById('top'),B=H.querySelector('.burger');B.onclick=()=>{const o=H.classList.toggle('open');B.setAttribute('aria-expanded',o)};
H.querySelectorAll('nav a').forEach(l=>l.addEventListener('click',()=>{H.classList.remove('open');B.setAttribute('aria-expanded',false)}));
"""
    html = page(d, css, body, t["fonts"], js)
    cls = t.get("grid", "quadrille") + (" opening-photo" if t.get("opening") == "photo" else "")
    return html.replace("<body", f'<body class="{cls}"', 1)
