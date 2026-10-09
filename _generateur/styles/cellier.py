"""Style « cellier » — la parole du vigneron en ouverture, les vins rangés sur des étagères.
Pour un domaine familial avec beaucoup de cuvées. Étagères de bouteilles par couleur avec
étiquette de prix ; un clic sur une bouteille ouvre sa fiche (description, médaille, prix).
Popup d'annonce, achat et livraison, points de vente, chambre d'hôtes, souvenirs légendés.
"""
from core import e, a, tgt, logo, map_iframe, page

FONTS = "https://fonts.googleapis.com/css2?family=Young+Serif&family=Instrument+Sans:wght@400;500;600&display=swap"

CSS = """
:root{--white:#fff;--gamay:%(gamay)s;--stone:%(stone)s;--blush:%(blush)s;--ink:%(ink)s;--gold:%(gold)s;--muted:%(muted)s;--rule:rgba(38,25,31,.13);--wood:#b89b7a}
body{background:var(--white);color:var(--ink);font:400 1.02rem/1.62 "Instrument Sans",system-ui,sans-serif}
.ys{font-family:"Young Serif",Georgia,serif;font-weight:400;line-height:1.08}
.w{max-width:1200px;margin:0 auto;padding:0 22px}
.btn{display:inline-block;padding:13px 22px;border-radius:6px;background:var(--gamay);color:#fff;text-decoration:none;font-weight:600;border:2px solid var(--gamay)}
.btn:hover{background:var(--ink);border-color:var(--ink)}.btn.line{background:none;color:var(--gamay)}.btn.line:hover{background:var(--gamay);color:#fff}
header{position:sticky;top:0;z-index:50;background:#fff;border-bottom:1px solid var(--rule)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;height:80px}
.logo-txt{font-family:"Young Serif",serif;font-size:1.3rem;color:var(--gamay)}
nav.links{display:flex;gap:20px;font-weight:500;font-size:.94rem}nav.links a{text-decoration:none}nav.links a:hover{color:var(--gamay)}
.burger{display:none;background:none;border:1px solid var(--rule);border-radius:6px;padding:8px 13px;font-weight:600;cursor:pointer}
@media(max-width:1000px){nav.links{display:none;position:absolute;top:80px;left:0;right:0;flex-direction:column;gap:0;background:#fff;padding:6px 22px 16px;border-bottom:1px solid var(--rule)}
nav.links a{padding:12px 0;border-bottom:1px solid var(--rule)}header.open nav.links{display:flex}.burger{display:block}}
.hero{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:clamp(26px,5vw,70px);align-items:center;padding:clamp(40px,6vw,80px) 0}
.hero blockquote{font-family:"Young Serif",serif;font-size:clamp(2.3rem,5.4vw,4.6rem);line-height:1.08;color:var(--gamay)}
.hero cite{display:block;font-style:normal;margin-top:18px;font-weight:600}
.hero p.lead{margin:22px 0 28px;font-size:1.1rem;max-width:48ch;color:var(--muted)}
.hero .ctas{display:flex;gap:12px;flex-wrap:wrap}
.hero figure img{width:100%%;aspect-ratio:4/5;object-fit:cover;border-radius:4px;background:var(--blush)}
.hero figcaption{font-size:.85rem;color:var(--muted);margin-top:8px}
@media(max-width:860px){.hero{grid-template-columns:minmax(0,1fr)}.hero figure img{aspect-ratio:4/3}}
.band{background:var(--blush)}.band ul{list-style:none;display:grid;grid-template-columns:repeat(3,1fr);gap:0}
.band li{padding:20px 22px;border-left:1px solid var(--rule);font-weight:500}.band li:first-child{border-left:0}.band li b{display:block;font-family:"Young Serif",serif;font-weight:400;font-size:1.15rem;color:var(--gamay)}
@media(max-width:760px){.band ul{grid-template-columns:1fr}.band li{border-left:0;border-top:1px solid var(--rule)}}
section{padding:clamp(64px,9vw,110px) 0}
h2.h{font-size:clamp(2.1rem,4.4vw,3.4rem);color:var(--ink)}
.split{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(28px,5vw,70px);align-items:center}
.split img{width:100%%;aspect-ratio:4/3;object-fit:cover;border-radius:4px;background:var(--blush)}
.split p{margin-top:15px;max-width:58ch}.split .sig{font-family:"Young Serif",serif;color:var(--gamay);font-size:1.2rem}
.split.rev>:first-child{order:2}
@media(max-width:820px){.split{grid-template-columns:minmax(0,1fr)}.split.rev>:first-child{order:0}}
.vignes{background:var(--stone);color:#f2f0ee}.vignes h2.h{color:#fff}
.sf{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:26px;margin-top:40px}
.sf div{border-top:2px solid var(--gamay);padding-top:14px}.sf h3{font:600 1.02rem "Instrument Sans",sans-serif;margin-bottom:6px}.sf p{color:var(--muted);font-size:.93rem}
@media(max-width:860px){.sf{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:520px){.sf{grid-template-columns:minmax(0,1fr)}}
/* cellier */
.cave{background:linear-gradient(#fff,var(--blush))}
.cave .intro{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:18px;margin-bottom:30px}.cave .intro p{color:var(--muted);max-width:52ch}
.shelf{margin-top:38px}.shelf h3{font-family:"Young Serif",serif;font-weight:400;font-size:1.6rem;margin-bottom:8px}
.row{display:flex;gap:8px;overflow-x:auto;padding:10px 4px 0;border-bottom:12px solid var(--wood);box-shadow:0 8px 12px -8px rgba(0,0,0,.35);scroll-snap-type:x mandatory}
.btl{flex:0 0 132px;scroll-snap-align:start;background:none;border:0;cursor:pointer;display:flex;flex-direction:column;align-items:center;position:relative;padding:0 4px;text-align:center}
.btl img,.btl svg{height:210px;width:auto;max-width:100%%;object-fit:contain;transition:transform .25s}
.btl:hover img,.btl:hover svg,.btl[aria-pressed="true"] img,.btl[aria-pressed="true"] svg{transform:translateY(-8px)}
.btl .pt{position:relative;margin:8px 0 -4px;background:#fff;border:1px solid var(--rule);padding:4px 10px 4px 14px;font-weight:600;font-size:.88rem;clip-path:polygon(10px 0,100%% 0,100%% 100%%,10px 100%%,0 50%%)}
.btl .nm{font-size:.82rem;line-height:1.2;margin:10px 0 12px;min-height:2.4em}
.btl[aria-pressed="true"] .nm{color:var(--gamay);font-weight:600}
.btl .md{position:absolute;top:6px;right:18px;width:30px;height:30px;border-radius:50%%;background:var(--gold);color:#fff;font:600 .58rem/30px "Instrument Sans",sans-serif;box-shadow:0 0 0 3px #fff}
.sheet{background:#fff;border:1px solid var(--rule);border-top:0;padding:22px 24px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px 30px}
.sheet h4{font-family:"Young Serif",serif;font-weight:400;font-size:1.5rem}.sheet .ap{color:var(--gamay);font-weight:500}
.sheet p{color:var(--muted);margin-top:8px;max-width:70ch}.sheet .medal{color:var(--gold);font-weight:600;font-size:.92rem;margin-top:8px}
.sheet .price{text-align:right;font-family:"Young Serif",serif;font-size:2rem;color:var(--ink)}.sheet .price small{display:block;font:500 .82rem "Instrument Sans",sans-serif;color:var(--muted)}
@media(max-width:620px){.sheet{grid-template-columns:minmax(0,1fr)}.sheet .price{text-align:left}}
.cave .note{margin-top:30px;color:var(--muted);font-size:.92rem}
/* acheter */
.buy{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin-top:34px}
.buy div{border:1px solid var(--rule);border-radius:6px;padding:24px}.buy h3{font-family:"Young Serif",serif;font-weight:400;font-size:1.3rem;color:var(--gamay);margin-bottom:8px}
.buy .hl{background:var(--gamay);color:#fff;border-color:var(--gamay)}.buy .hl h3{color:#fff}.buy .hl small{display:block;opacity:.8;margin-top:10px;font-size:.85rem}
@media(max-width:700px){.buy{grid-template-columns:minmax(0,1fr)}}
.pdv{margin-top:56px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:22px}
.pdv h3{font:600 1rem "Instrument Sans",sans-serif;margin-bottom:6px}.pdv p{color:var(--muted);font-size:.93rem}
@media(max-width:860px){.pdv{grid-template-columns:repeat(2,minmax(0,1fr))}}
/* souvenirs */
.souv{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:22px;margin-top:34px}
.souv button{background:#fff;border:0;padding:10px 10px 14px;box-shadow:0 10px 24px -14px rgba(0,0,0,.45);cursor:zoom-in;text-align:left}
.souv img{width:100%%;aspect-ratio:1;object-fit:cover;background:var(--blush)}.souv span{display:block;margin-top:10px;font-size:.9rem}
.contact{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);border:1px solid var(--rule);border-radius:6px;overflow:hidden}
.contact .in{padding:clamp(26px,5vw,52px)}.contact dl{display:grid;grid-template-columns:110px minmax(0,1fr);gap:12px 16px;margin:24px 0}
.contact dt{color:var(--muted)}.contact dd{overflow-wrap:anywhere}
.map{width:100%%;height:100%%;min-height:380px;border:0}
@media(max-width:820px){.contact{grid-template-columns:minmax(0,1fr)}.contact dl{grid-template-columns:1fr;gap:2px}.contact dd{margin-bottom:10px}}
.ann-box{background:#fff;max-width:440px;width:100%%;padding:34px 30px 30px;border-radius:8px;position:relative;border-top:8px solid var(--gamay)}
.ann-box .x{position:absolute;top:8px;right:12px;background:none;border:0;font-size:1.6rem;cursor:pointer;color:var(--muted)}
.ann-box .ann-k{color:var(--gold);font-weight:600}.ann-box h2{font-family:"Young Serif",serif;font-weight:400;font-size:1.6rem;color:var(--gamay);margin:8px 0 12px}
.ann-box p{color:var(--muted);margin-bottom:20px}.ann-box .btn{width:100%%;text-align:center}
footer{background:var(--ink);color:#e7dfe3;padding:40px 0 100px;font-size:.9rem}footer .w{display:flex;flex-wrap:wrap;justify-content:space-between;gap:20px}
footer .flogo{background:#fff;padding:8px 12px;border-radius:6px;display:inline-block}
"""


def bottle(color):
    return (f'<svg viewBox="0 0 40 120" aria-hidden="true"><path d="M16 2h8v30c0 6 10 10 10 22v58a6 6 0 0 1-6 6H12a6 6 0 0 1-6-6V54c0-12 10-16 10-22z" fill="{color}"/>'
            f'<rect x="10" y="66" width="20" height="26" fill="#fff" opacity=".9"/></svg>')


def render(d):
    css = CSS % d["theme"]
    nav = "".join(f'<a href="#{i}">{e(l)}</a>' for i, l in d["nav"])
    h = d["hero"]
    band = "".join(f"<li><b>{e(x[0])}</b>{e(x[1])}</li>" for x in d["band"])
    dom, vg, sf = d["domaine"], d["vignes"], d["savoirfaire"]
    sfh = "".join(f'<div><h3>{e(x[0])}</h3><p>{e(x[1])}</p></div>' for x in sf["items"])
    shelves = ""
    data = {}
    for key, label in d["cave"]["shelves"]:
        items = [w for w in d["cave"]["items"] if w["cat"] == key]
        btns = ""
        for n, w in enumerate(items):
            wid = f"{key}{n}"
            data[wid] = w
            img = (f'<img src="{a(w["img"])}" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.outerHTML=this.dataset.s" data-s="{a(bottle(w["color"]))}">'
                   if w.get("img") else bottle(w["color"]))
            ml = w.get("medal", "").lower()
            md = ('<span class="md" aria-hidden="true">Or</span>' if "d'or" in ml else
                  '<span class="md" aria-hidden="true" style="background:#8f999e">Arg.</span>' if "argent" in ml else "")
            btns += (f'<button class="btl" aria-pressed="{"true" if n == 0 else "false"}" data-w="{wid}" aria-controls="sheet-{key}">{md}{img}'
                     f'<span class="pt">{e(w.get("price", ""))}</span><span class="nm">{e(w["name"])}</span></button>')
        first = items[0]
        shelves += f'''<div class="shelf"><h3>{e(label)}</h3><div class="row" role="group" aria-label="{a(label)}">{btns}</div>
<div class="sheet" id="sheet-{key}" aria-live="polite">{sheet_html(first)}</div></div>'''
    import json as _j
    wjson = _j.dumps({k: {"h": sheet_html(v)} for k, v in data.items()}, ensure_ascii=False).replace("</", "<\\/")
    buy = "".join(f'<div class="{"hl" if x.get("hl") else ""}"><h3>{e(x["title"])}</h3><p>{e(x["text"])}</p>{f"<small>{e(x["small"])}</small>" if x.get("small") else ""}</div>' for x in d["acheter"]["items"])
    pdv = "".join(f'<div><h3>{e(x[0])}</h3><p>{e(x[1])}</p></div>' for x in d["acheter"]["pdv"])
    ch = d["chambre"]
    souv = "".join(f'<button data-full="{a(p["full"])}" data-cap="{a(p["caption"])}" data-alt="{a(p["caption"])}"><img src="{a(p["thumb"])}" alt="{a(p["caption"])}" loading="lazy" referrerpolicy="no-referrer"><span>{e(p["caption"])}</span></button>' for p in d["partage"]["photos"])
    c = d["contact"]
    rows = "".join(f"<dt>{e(k)}</dt><dd>{v}</dd>" for k, v in c["rows"])
    body = f'''<header id="top" style="background:{a(d.get("logo", {}).get("bg", "#fff"))}"><div class="w nav"><a href="#accueil" aria-label="{a(d["brand"])}, accueil">{logo(d)}</a>
<nav class="links" aria-label="Navigation principale">{nav}</nav><button class="burger" aria-expanded="false">Menu</button></div></header>
<main>
<div class="w hero" id="accueil"><div><blockquote>{e(h["quote"])}</blockquote><cite>{e(h["cite"])}</cite><p class="lead">{e(h["lead"])}</p>
<div class="ctas"><a class="btn" href="#cave">Voir la cave</a><a class="btn line" href="{a(h["shop"])}" target="_blank" rel="noopener">Commander en ligne</a></div></div>
<figure><img src="{a(h["img"])}" alt="{a(h.get("alt", ""))}" referrerpolicy="no-referrer"><figcaption>{e(h.get("caption", ""))}</figcaption></figure></div>
<div class="band"><ul class="w">{band}</ul></div>
<section id="domaine"><div class="w split"><img src="{a(dom["img"])}" alt="{a(dom.get("alt", ""))}" loading="lazy" referrerpolicy="no-referrer">
<div><h2 class="h ys">{e(dom["title"])}</h2>{"".join(f"<p>{p}</p>" for p in dom["paras"])}<p class="sig">{e(dom.get("sign", ""))}</p></div></div></section>
<section class="vignes" id="vignes"><div class="w split rev"><img src="{a(vg["img"])}" alt="{a(vg.get("alt", ""))}" loading="lazy" referrerpolicy="no-referrer">
<div><h2 class="h ys">{e(vg["title"])}</h2>{"".join(f"<p>{p}</p>" for p in vg["paras"])}</div></div></section>
<section id="savoir-faire"><div class="w"><h2 class="h ys">{e(sf["title"])}</h2><div class="sf">{sfh}</div></div></section>
<section class="cave" id="cave"><div class="w"><div class="intro"><h2 class="h ys">{e(d["cave"]["title"])}</h2><p>{e(d["cave"]["lead"])}</p></div>{shelves}
<p class="note">{e(d["cave"]["note"])}</p></div></section>
<section id="acheter"><div class="w"><h2 class="h ys">{e(d["acheter"]["title"])}</h2><div class="buy">{buy}</div>
<h3 class="ys" style="font-size:1.6rem;margin-top:60px">{e(d["acheter"]["pdv_title"])}</h3><div class="pdv" style="margin-top:20px">{pdv}</div></div></section>
<section id="chambre" style="padding-top:0"><div class="w split rev"><img src="{a(ch["img"])}" alt="{a(ch.get("alt", ""))}" loading="lazy" referrerpolicy="no-referrer">
<div><h2 class="h ys">{e(ch["title"])}</h2>{"".join(f"<p>{p}</p>" for p in ch["paras"])}</div></div></section>
<section id="partage" style="padding-top:0"><div class="w"><h2 class="h ys">{e(d["partage"]["title"])}</h2><p style="color:var(--muted);margin-top:10px">{e(d["partage"]["lead"])}</p><div class="souv">{souv}</div></div></section>
<section id="contact" style="padding-top:0"><div class="w"><div class="contact"><div class="in"><h2 class="h ys">{e(c["title"])}</h2><p style="color:var(--muted);margin-top:10px">{e(c["text"])}</p><dl>{rows}</dl>
<a class="btn" href="{a(c["cta"][1])}">{e(c["cta"][0])}</a></div>{map_iframe(c["map_q"])}</div></div></section>
</main>
<footer><div class="w"><div><span class="flogo">{logo(d, 44)}</span><p style="margin-top:12px">{e(d["footer"]["about"])}</p></div><p>{"<br>".join(d["footer"]["contact"])}</p><p style="max-width:34ch">{e(d["footer"]["legal"])}</p></div></footer>
<script type="application/json" id="wines">{wjson}</script>'''
    js = """
const H=document.getElementById('top'),B=H.querySelector('.burger');B.onclick=()=>{const o=H.classList.toggle('open');B.setAttribute('aria-expanded',o)};
H.querySelectorAll('nav a').forEach(l=>l.onclick=()=>{H.classList.remove('open');B.setAttribute('aria-expanded',false)});
const W=JSON.parse(document.getElementById('wines').textContent);
document.querySelectorAll('.btl').forEach(b=>b.onclick=()=>{const row=b.parentElement;row.querySelectorAll('.btl').forEach(x=>x.setAttribute('aria-pressed',x===b));
 document.getElementById(b.getAttribute('aria-controls')).innerHTML=W[b.dataset.w].h});
"""
    return page(d, css, body, FONTS, js)


def sheet_html(w):
    medal = f'<p class="medal">{e(w["medal"])}</p>' if w.get("medal") else ""
    desc = f'<p>{e(w["desc"])}</p>' if w.get("desc") else ""
    return (f'<div><h4>{e(w["name"])}</h4><p class="ap">{e(w["app"])}{", " + e(w["tag"]) if w.get("tag") else ""}</p>{desc}{medal}</div>'
            f'<div class="price">{e(w.get("price", ""))}<small>{e(w.get("fmt", "la bouteille, départ cave"))}</small></div>')
