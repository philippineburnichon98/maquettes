"""Style « diorite » — la page comme une coupe de terrain sous les vignes.
Pour un domaine dont l'identité tient à son sol. L'ouverture trace le relief de la colline
(ou montre une grande photo, theme["open"] = "photo"), puis on descend de couche en couche :
domaine, terroir, savoir-faire, et la « coupe » des cuvées : chaque bouteille est posée
dans la strate de sol où elle pousse ; un clic ouvre sa fiche technique (PDF, médailles, prix).
Ensuite visites/hébergement avec offres en clair, presse et actualités en relevé daté, contact.
Tout est paramétré par d["theme"] (couleurs, polices, ouverture) pour un autre domaine.
"""
import json as _j
from core import e, a, tgt, logo, map_iframe, page

CSS = """
:root{--rock:%(rock)s;--rock2:%(rock2)s;--wine:%(wine)s;--chalk:%(chalk)s;--moss:%(moss)s;--ink:%(ink)s;--muted:%(muted)s;--rule:color-mix(in srgb,var(--ink) 16%%,transparent)}
body{background:var(--chalk);color:var(--ink);font:400 1.06rem/1.62 %(body)s}
.hd{font-family:%(head)s;font-stretch:%(stretch)s;font-variation-settings:'wdth' %(wdth)s;font-weight:%(hw)s;line-height:1.02;letter-spacing:-.01em}
.w{max-width:1220px;margin:0 auto;padding:0 22px}
a.btn,.btn{display:inline-block;padding:13px 20px;background:var(--wine);color:#fff;text-decoration:none;font:600 .95rem/1.2 %(head)s;border:2px solid var(--wine)}
.btn:hover{background:var(--ink);border-color:var(--ink)}.btn.ghost{background:none;color:inherit;border-color:currentColor}.btn.ghost:hover{background:var(--chalk);color:var(--ink);border-color:var(--chalk)}
header{position:sticky;top:0;z-index:50;background:%(logobg)s;border-bottom:1px solid var(--rule)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:76px}
.logo-txt{font:700 1.25rem %(head)s;color:var(--rock)}
nav.links{display:flex;gap:22px;font:500 .93rem %(head)s}nav.links a{text-decoration:none;padding:6px 0;border-bottom:2px solid transparent}nav.links a:hover{border-color:var(--wine)}
.burger{display:none;background:none;border:2px solid var(--ink);padding:7px 12px;font:600 .9rem %(head)s;cursor:pointer}
@media(max-width:1020px){nav.links{display:none;position:absolute;top:76px;left:0;right:0;flex-direction:column;gap:0;background:var(--chalk);padding:4px 22px 14px;border-bottom:1px solid var(--rule)}
nav.links a{padding:12px 0;border-bottom:1px solid var(--rule)}header.open nav.links{display:flex}.burger{display:block}}
/* ouverture relief */
.open{background:var(--rock);color:var(--chalk);position:relative;overflow:hidden}
.open .w{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:clamp(24px,5vw,64px);align-items:end;padding-top:clamp(40px,7vw,90px);padding-bottom:clamp(30px,4vw,50px)}
.open h1{font-size:clamp(2.6rem,7vw,6.2rem);color:#fff}
.open .lead{font-size:1.14rem;max-width:46ch;margin:22px 0 28px;color:color-mix(in srgb,var(--chalk) 86%%,transparent)}
.open .ctas{display:flex;flex-wrap:wrap;gap:12px}
.open figure img{width:100%%;aspect-ratio:4/5;object-fit:cover;background:var(--rock2)}
.open figcaption{font-size:.85rem;margin-top:8px;opacity:.8}
.relief{display:block;width:100%%;height:auto;margin-top:-1px}
.relief path.line{fill:none;stroke:var(--chalk);stroke-width:2;stroke-dasharray:2600;stroke-dashoffset:2600;animation:draw 2.6s ease-out .3s forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.relief text{font:500 13px %(head)s;fill:var(--chalk)}
@media(prefers-reduced-motion:reduce){.relief path.line{stroke-dashoffset:0}}
.open.photo{min-height:78vh;display:grid;align-items:end;background:var(--rock) center/cover}
.open.photo::before{content:"";position:absolute;inset:0;background:linear-gradient(transparent 30%%,color-mix(in srgb,var(--rock) 92%%,transparent))}
.open.photo .w{position:relative;grid-template-columns:minmax(0,1fr)}
@media(max-width:860px){.open .w{grid-template-columns:minmax(0,1fr)}.open figure img{aspect-ratio:4/3}}
.strata{display:grid;grid-auto-flow:column;grid-auto-columns:1fr}.strata span{display:block;padding:12px 22px;font:600 .9rem %(head)s;color:#fff}
@media(max-width:700px){.strata{grid-auto-flow:row}}
section{padding:clamp(60px,9vw,112px) 0}
h2.hd{font-size:clamp(2rem,4.6vw,3.6rem)}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(28px,5vw,72px);align-items:start}
.two p{margin-top:14px;max-width:60ch}.two img{width:100%%;aspect-ratio:4/3;object-fit:cover;background:var(--rock2)}
.two .pics{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px}.two .pics img:first-child{grid-column:1/-1}
@media(max-width:840px){.two{grid-template-columns:minmax(0,1fr)}}
.people{margin-top:24px;border-top:2px solid var(--ink)}.people div{display:grid;grid-template-columns:7.5rem minmax(0,1fr);gap:14px;padding:12px 0;border-bottom:1px solid var(--rule)}
.people b{font-family:%(head)s}
.terroir{background:var(--rock2);color:var(--chalk)}.terroir h2{color:#fff}
.terroir blockquote{font:%(hw)s clamp(1.5rem,3.2vw,2.5rem)/1.2 %(head)s;font-stretch:%(stretch)s;border-left:6px solid var(--moss);padding-left:22px;margin:30px 0 10px;max-width:30ch;color:#fff}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:0;margin-top:44px;border-top:1px solid color-mix(in srgb,var(--chalk) 30%%,transparent)}
.facts div{padding:18px 20px 18px 0;border-bottom:1px solid color-mix(in srgb,var(--chalk) 30%%,transparent)}
.facts b{display:block;font:700 1.6rem/1.1 %(head)s;color:var(--moss);margin-bottom:4px}
.steps{list-style:none;margin-top:36px;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:30px}
.steps li{border-top:6px solid var(--rock);padding-top:14px}.steps h3{font:700 1.2rem %(head)s;margin-bottom:6px}.steps p{color:var(--muted)}
/* coupe des cuvées */
.coupe .intro{max-width:64ch}.coupe .intro p{margin-top:12px;color:var(--muted)}
.layer{margin-top:34px;background:var(--lc);color:var(--lt);position:relative}
.layer .lh{display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px 20px;padding:16px 22px 0}
.layer .lh h3{font:700 1.35rem %(head)s}.layer .lh p{max-width:56ch;opacity:.9}
.row{display:flex;gap:6px;overflow-x:auto;padding:12px 16px 0;scroll-snap-type:x mandatory}
.btl{flex:0 0 132px;scroll-snap-align:start;background:none;border:0;cursor:pointer;display:flex;flex-direction:column;align-items:center;padding:8px 4px 14px;text-align:center;color:inherit;border-bottom:4px solid transparent}
.btl img{height:220px;width:auto;max-width:100%%;object-fit:contain;filter:drop-shadow(0 8px 8px rgba(0,0,0,.25))}
.btl .nm{font:600 .9rem/1.2 %(head)s;margin-top:10px}.btl .ap{font-size:.8rem;opacity:.85}
.btl .md{font:700 .7rem %(head)s;background:var(--chalk);color:var(--ink);padding:2px 7px;margin-top:6px}
.btl[aria-pressed="true"]{border-color:currentColor}
.sheet{background:var(--chalk);color:var(--ink);border:2px solid var(--lc);border-top:0;display:grid;grid-template-columns:minmax(0,220px) minmax(0,1fr) minmax(0,13rem);gap:22px 30px;padding:24px}
.sheet img.hdimg{width:100%%;aspect-ratio:1;object-fit:cover;background:var(--rock2)}
.sheet h4{font:700 1.6rem/1.1 %(head)s}.sheet .ap{color:var(--wine);font-weight:600;margin-top:4px}
.sheet dl{display:grid;grid-template-columns:9.5rem minmax(0,1fr);gap:6px 14px;margin-top:14px;font-size:.96rem}.sheet dt{color:var(--muted)}
.sheet .medal{margin-top:12px;font-weight:600;color:var(--wine)}.sheet .desc{margin-top:12px;max-width:66ch}
.sheet .side{text-align:right;display:flex;flex-direction:column;align-items:flex-end;gap:4px}.sheet .side small{font-size:.9rem}.sheet .price{font:700 1.8rem %(head)s}.sheet .price small{display:block;font:400 .82rem %(body)s;color:var(--muted)}
.sheet .side a{display:inline-block;margin-top:12px;font-weight:600;color:var(--wine)}
@media(max-width:900px){.sheet{grid-template-columns:minmax(0,1fr)}.sheet img.hdimg{aspect-ratio:16/9}.sheet .side{text-align:left;align-items:flex-start}}
@media(max-width:520px){.sheet dl{grid-template-columns:minmax(0,1fr);gap:0}.sheet dd{margin-bottom:8px}}
.coupe .note{margin-top:26px;color:var(--muted);max-width:70ch}
/* visiter */
.visit{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(24px,4vw,48px);margin-top:36px}
.visit article{border:2px solid var(--ink);display:flex;flex-direction:column}
.visit article img{width:100%%;aspect-ratio:16/10;object-fit:cover;background:var(--rock2)}
.visit .in{padding:22px 24px 26px;display:flex;flex-direction:column;gap:12px;flex:1}
.visit h3{font:700 1.45rem/1.15 %(head)s}.visit ul{padding-left:1.1em}.visit .offer{background:var(--moss);color:var(--ink);padding:12px 14px;font-weight:600}
.visit .btn{align-self:flex-start;margin-top:auto}
.visit .thumbs{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:0 24px}.visit .thumbs button{border:0;padding:0;background:none;cursor:zoom-in}.visit .thumbs img{aspect-ratio:4/3}
@media(max-width:840px){.visit{grid-template-columns:minmax(0,1fr)}}
/* relevé presse */
.log{margin-top:30px;border-top:2px solid var(--ink)}
.log a,.log div.it{display:grid;grid-template-columns:9rem 12rem minmax(0,1fr);gap:16px;padding:14px 0;border-bottom:1px solid var(--rule);text-decoration:none}
.log a:hover .t{text-decoration:underline}.log time,.log .m{color:var(--muted)}.log .m{font-weight:600;color:var(--ink)}
@media(max-width:700px){.log a,.log div.it{grid-template-columns:minmax(0,1fr);gap:2px}}
.news{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:26px;margin-top:30px}
.news div{border-left:6px solid var(--rock);padding-left:16px}.news h3{font:700 1.15rem %(head)s}.news time{color:var(--muted);font-size:.9rem}
/* contact */
.contact{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);border:2px solid var(--ink)}
.contact .in{padding:clamp(24px,5vw,50px)}.contact dl{display:grid;grid-template-columns:8rem minmax(0,1fr);gap:10px 16px;margin:22px 0 26px}
.contact dt{color:var(--muted)}.contact dd{overflow-wrap:anywhere}.contact dd a{color:var(--wine);font-weight:600}
.map{width:100%%;height:100%%;min-height:380px;border:0}
@media(max-width:840px){.contact{grid-template-columns:minmax(0,1fr)}.contact dl{grid-template-columns:minmax(0,1fr);gap:0}.contact dd{margin-bottom:10px}}
.ann-box{background:var(--chalk);max-width:440px;width:100%%;padding:32px 28px 28px;position:relative;border-top:10px solid var(--wine)}
.ann-box .x{position:absolute;top:8px;right:12px;background:none;border:0;font-size:1.6rem;cursor:pointer}
.ann-box h2{font:700 1.5rem %(head)s;margin:6px 0 10px}.ann-box p{margin-bottom:18px}.ann-box .ann-k{color:var(--wine);font-weight:600}
footer{background:var(--rock);color:var(--chalk);padding:44px 0 110px;font-size:.92rem}
footer .w{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr) minmax(0,1fr);gap:28px}
footer .flogo{display:inline-block;background:%(logobg)s;padding:8px 12px}
footer .alc{grid-column:1/-1;border-top:1px solid color-mix(in srgb,var(--chalk) 30%%,transparent);padding-top:18px;font-weight:600}
@media(max-width:760px){footer .w{grid-template-columns:minmax(0,1fr)}}
"""

RELIEF = """<svg class="relief" viewBox="0 0 1440 170" preserveAspectRatio="none" aria-hidden="true">
<path d="M0 170V150C180 148 330 140 470 118C600 96 660 40 760 26C830 16 880 30 950 58C1080 110 1250 140 1440 146V170Z" fill="var(--lc1)"/>
<path d="M0 170V162C220 160 420 156 600 140C720 128 800 96 900 98C1040 104 1200 150 1440 156V170Z" fill="var(--lc2)"/>
<path class="line" d="M0 150C180 148 330 140 470 118C600 96 660 40 760 26C830 16 880 30 950 58C1080 110 1250 140 1440 146"/></svg>"""


def sheet_html(w):
    tech = "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in w.get("tech", []))
    medal = "".join(f'<p class="medal">{e(m)}</p>' for m in w.get("medals", []))
    desc = f'<p class="desc">{e(w["desc"])}</p>' if w.get("desc") else ""
    img = (f'<div><img class="hdimg" src="{a(w["photo"])}" alt="{a(w.get("photo_alt", ""))}" loading="lazy" referrerpolicy="no-referrer" onerror="this.remove()"></div>'
           if w.get("photo") else "<div></div>")
    price = (f'<div class="price">{e(w["price"])}<small>{e(w.get("fmt", "la bouteille"))}</small></div>' if w.get("price")
             else f'<small style="color:var(--muted)">{e(w.get("noprice", ""))}</small>')
    pdf = f'<a href="{a(w["pdf"])}" target="_blank" rel="noopener">Télécharger la fiche (PDF)</a>' if w.get("pdf") else ""
    return (f'{img}<div><h4>{e(w["name"])}</h4><p class="ap">{e(w["app"])}</p>{desc}<dl>{tech}</dl>{medal}</div>'
            f'<div class="side">{price}{pdf}</div>')


def render(d):
    t = d["theme"]
    css = CSS % t
    nav = "".join(f'<a href="#{i}">{e(l)}</a>' for i, l in d["nav"])
    h = d["hero"]
    layers = d["coupe"]["layers"]
    lc1 = layers[0]["color"]
    lc2 = layers[-1]["color"]
    ctas = "".join(f'<a class="btn{" ghost" if n else ""}" href="{a(u)}"{tgt(u)}>{e(l)}</a>' for n, (l, u) in enumerate(h["ctas"]))
    if t.get("open", "relief") == "photo":
        opening = f'''<div class="open photo" id="accueil" style="background-image:url('{a(h["img"])}')"><div class="w"><div><h1 class="hd">{e(h["title"])}</h1><p class="lead">{e(h["lead"])}</p><div class="ctas">{ctas}</div></div></div></div>'''
    else:
        opening = f'''<div class="open" id="accueil" style="--lc1:{a(lc1)};--lc2:{a(lc2)}"><div class="w"><div><h1 class="hd">{e(h["title"])}</h1><p class="lead">{e(h["lead"])}</p><div class="ctas">{ctas}</div></div>
<figure><img src="{a(h["img"])}" alt="{a(h.get("alt", ""))}" referrerpolicy="no-referrer"><figcaption>{e(h.get("caption", ""))}</figcaption></figure></div>{RELIEF}</div>'''
    strata = "".join(f'<span style="background:{a(L["color"])};color:{a(L.get("text", "#fff"))}">{e(L["label"])}</span>' for L in layers)
    dom = d["domaine"]
    pics = "".join(f'<img src="{a(p[0])}" alt="{a(p[1])}" loading="lazy" referrerpolicy="no-referrer" onerror="this.remove()">' for p in dom["imgs"])
    people = "".join(f"<div><b>{e(p[0])}</b><span>{e(p[1])}</span></div>" for p in dom.get("people", []))
    ter = d["terroir"]
    facts = "".join(f"<div><b>{e(f[0])}</b>{e(f[1])}</div>" for f in ter["facts"])
    sf = d["savoirfaire"]
    steps = "".join(f"<li><h3>{e(s[0])}</h3><p>{e(s[1])}</p></li>" for s in sf["steps"])
    data = {}
    lay_html = ""
    for L in layers:
        items = [w for w in d["coupe"]["wines"] if w["layer"] == L["key"]]
        btns = ""
        for n, w in enumerate(items):
            wid = f'{L["key"]}{n}'
            data[wid] = sheet_html(w)
            md = '<span class="md">Médaillé</span>' if w.get("medals") else ""
            btns += (f'<button class="btl" aria-pressed="{"true" if n == 0 else "false"}" data-w="{wid}" aria-controls="sh-{L["key"]}">'
                     f'<img src="{a(w["bottle"])}" alt="" loading="lazy" referrerpolicy="no-referrer"><span class="nm">{e(w["name"])}</span><span class="ap">{e(w["short"])}</span>{md}</button>')
        lay_html += f'''<div class="layer" style="--lc:{a(L["color"])};--lt:{a(L.get("text", "#fff"))}"><div class="lh"><h3>{e(L["label"])}</h3><p>{e(L["sub"])}</p></div>
<div class="row" role="group" aria-label="Cuvées : {a(L["label"])}">{btns}</div></div>
<div class="sheet" id="sh-{L["key"]}" aria-live="polite" style="--lc:{a(L["color"])}">{sheet_html(items[0])}</div>'''
    vis = ""
    for v in d["visiter"]["items"]:
        lis = "".join(f"<li>{e(x)}</li>" for x in v.get("list", []))
        thumbs = "".join(f'<button data-full="{a(p[0])}" data-cap="{a(p[1])}" data-alt="{a(p[1])}"><img src="{a(p[0])}" alt="{a(p[1])}" loading="lazy" referrerpolicy="no-referrer"></button>' for p in v.get("thumbs", []))
        offer = f'<p class="offer">{e(v["offer"])}</p>' if v.get("offer") else ""
        cta = f'<a class="btn" href="{a(v["cta"][1])}"{tgt(v["cta"][1])}>{e(v["cta"][0])}</a>' if v.get("cta") else ""
        vis += f'''<article><img src="{a(v["img"])}" alt="{a(v.get("alt", ""))}" loading="lazy" referrerpolicy="no-referrer"><div class="in"><h3>{e(v["title"])}</h3>{"".join(f"<p>{e(p)}</p>" for p in v["paras"])}{f"<ul>{lis}</ul>" if lis else ""}{offer}{cta}</div>{f'<div class="thumbs">{thumbs}</div><div style="height:24px"></div>' if thumbs else ""}</article>'''
    pr = d["presse"]
    log = ""
    for it in pr["items"]:
        inner = f'<time>{e(it["date"])}</time><span class="m">{e(it["media"])}</span><span class="t">{e(it["title"])}</span>'
        log += f'<a href="{a(it["url"])}" target="_blank" rel="noopener">{inner}</a>' if it.get("url") else f'<div class="it">{inner}</div>'
    news = "".join(f'<div><time>{e(n[0])}</time><h3>{e(n[1])}</h3><p>{e(n[2])}</p></div>' for n in pr.get("news", []))
    c = d["contact"]
    rows = "".join(f"<dt>{e(k)}</dt><dd>{v}</dd>" for k, v in c["rows"])
    f = d["footer"]
    body = f'''<header id="top"><div class="w nav"><a href="#accueil" aria-label="{a(d["brand"])}, retour en haut">{logo(d)}</a>
<nav class="links" aria-label="Navigation principale">{nav}</nav><button class="burger" aria-expanded="false">Menu</button></div></header>
<main>{opening}<div class="strata" aria-hidden="true">{strata}</div>
<section id="domaine"><div class="w two"><div><h2 class="hd">{e(dom["title"])}</h2>{"".join(f"<p>{p}</p>" for p in dom["paras"])}<div class="people">{people}</div></div><div class="pics">{pics}</div></div></section>
<section class="terroir" id="terroir"><div class="w"><h2 class="hd">{e(ter["title"])}</h2><blockquote>{e(ter["quote"])}</blockquote>
<div class="two"><div>{"".join(f"<p>{p}</p>" for p in ter["paras"])}</div><img src="{a(ter["img"])}" alt="{a(ter.get("alt", ""))}" loading="lazy" referrerpolicy="no-referrer" onerror="this.remove()"></div>
<div class="facts">{facts}</div></div></section>
<section id="savoir-faire"><div class="w"><h2 class="hd">{e(sf["title"])}</h2><p style="max-width:62ch;margin-top:12px">{e(sf["lead"])}</p><ul class="steps">{steps}</ul></div></section>
<section class="coupe" id="vins" style="padding-top:0"><div class="w"><div class="intro"><h2 class="hd">{e(d["coupe"]["title"])}</h2><p>{e(d["coupe"]["lead"])}</p></div>{lay_html}
<p class="note">{d["coupe"]["note"]}</p></div></section>
<section id="visiter" style="padding-top:0"><div class="w"><h2 class="hd">{e(d["visiter"]["title"])}</h2><div class="visit">{vis}</div></div></section>
<section id="presse" style="padding-top:0"><div class="w"><h2 class="hd">{e(pr["title"])}</h2><div class="log">{log}</div>
<h3 class="hd" style="font-size:1.6rem;margin-top:54px">{e(pr.get("news_title", "Actualités"))}</h3><div class="news">{news}</div></div></section>
<section id="contact" style="padding-top:0"><div class="w"><div class="contact"><div class="in"><h2 class="hd">{e(c["title"])}</h2><p style="margin-top:10px">{e(c["text"])}</p><dl>{rows}</dl>
<a class="btn" href="{a(c["cta"][1])}"{tgt(c["cta"][1])}>{e(c["cta"][0])}</a></div>{map_iframe(c["map_q"])}</div></div></section>
</main>
<footer><div class="w"><div><span class="flogo">{logo(d, 46)}</span><p style="margin-top:12px">{e(f["about"])}</p></div>
<p>{"<br>".join(f["contact"])}</p><p>{"<br>".join(e(x) for x in f["legal"])}</p>
<p class="alc">L'abus d'alcool est dangereux pour la santé, à consommer avec modération.</p></div></footer>
<script type="application/json" id="wines">{_j.dumps(data, ensure_ascii=False).replace("</", "<\\/")}</script>'''
    js = """
const H=document.getElementById('top'),B=H.querySelector('.burger');B.onclick=()=>{const o=H.classList.toggle('open');B.setAttribute('aria-expanded',o)};
H.querySelectorAll('nav a').forEach(l=>l.onclick=()=>{H.classList.remove('open');B.setAttribute('aria-expanded',false)});
const W=JSON.parse(document.getElementById('wines').textContent);
document.querySelectorAll('.btl').forEach(b=>b.onclick=()=>{b.parentElement.querySelectorAll('.btl').forEach(x=>x.setAttribute('aria-pressed',x===b));
 document.getElementById(b.getAttribute('aria-controls')).innerHTML=W[b.dataset.w]});
"""
    return page(d, css, body, t["fonts"], js)
