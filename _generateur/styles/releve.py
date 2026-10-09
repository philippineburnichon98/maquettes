"""Style « relevé » — la planche du diagnostiqueur immobilier.
Fond papier calque quadrillé, encre de plan et traits de cote rouges. En ouverture, un plan
d'appartement coté avec son cartouche d'architecte (coordonnées, repères chiffrés). Le parcours
de vente / location / avant travaux se déroule le long d'un mètre ruban jaune gradué (onglets,
étapes réellement séquentielles). Les diagnostics forment une nomenclature dépliable (details),
le DPE affiche l'échelle énergie A à G aux couleurs officielles. Puis champs d'intervention,
avis, références, zone + carte, demande de devis (mailto / tel) et pied de page des mentions
(certification, organisme, assurance).
Thème : d["theme"] = {ink, paper, cote, ribbon, graphite, head, body, fonts}.
"""
import urllib.parse
from core import e, a, tgt, logo, map_iframe, page

DEF_FONTS = "https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap"
DPE = [("A", "#009c6d", "#fff"), ("B", "#52b153", "#fff"), ("C", "#78bd76", "#14321a"), ("D", "#f4e70f", "#332f00"),
       ("E", "#f0b40f", "#332300"), ("F", "#eb8235", "#2b1400"), ("G", "#d7221f", "#fff")]

CSS = """
.ph{display:block;width:100%%;object-fit:cover;border:2px solid var(--ink);box-shadow:6px 6px 0 var(--ribbon);background:#fff}
.band{height:clamp(200px,32vw,360px);margin:8px 0 30px}
.soc{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(22px,4vw,48px);align-items:center}.soc .ph{aspect-ratio:4/3}
.tabimg{aspect-ratio:21/8;margin:6px 0 22px}.opimg{aspect-ratio:4/3;margin:0 0 16px}.zimg{max-height:260px;margin:18px 0 0;object-fit:contain;box-shadow:none;border:0;background:none}
@media(max-width:760px){.soc{grid-template-columns:minmax(0,1fr)}.tabimg{aspect-ratio:16/9}}
:root{--ink:%(ink)s;--paper:%(paper)s;--cote:%(cote)s;--ribbon:%(ribbon)s;--graphite:%(graphite)s;--grid:rgba(28,42,72,.07);--rule:rgba(28,42,72,.18)}
body{background:var(--paper);color:var(--ink);font:400 1.03rem/1.62 %(body)s;
background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:24px 24px}
h1,h2,h3,.hd{font-family:%(head)s;font-weight:600;line-height:1.05;letter-spacing:.005em}
.w{max-width:1180px;margin:0 auto;padding:0 22px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:12px 20px;border:2px solid var(--ink);background:var(--ink);color:#fff;text-decoration:none;font-weight:600;border-radius:2px}
.btn:hover{background:var(--cote);border-color:var(--cote)}.btn.line{background:transparent;color:var(--ink)}.btn.line:hover{background:var(--ink);color:#fff}
header{position:sticky;top:0;z-index:50;background:#fff;border-bottom:2px solid var(--ink)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:76px}
.logo-txt{font-family:%(head)s;font-weight:700;font-size:1.55rem;text-transform:uppercase;letter-spacing:.02em;padding:2px 10px;border:2px solid var(--ink);box-shadow:4px 4px 0 var(--ribbon)}
footer .logo-txt{display:inline-block}
@media(max-width:600px){header .logo-txt{font-size:1.15rem;white-space:nowrap}}
nav.links{display:flex;gap:22px;font-weight:500;font-size:.95rem}nav.links a{text-decoration:none;padding:4px 0;border-bottom:2px solid transparent}nav.links a:hover{border-color:var(--cote)}
.nav .tel{white-space:nowrap}
.burger{display:none;background:#fff;border:2px solid var(--ink);padding:7px 12px;font-weight:600;cursor:pointer}
@media(max-width:980px){nav.links{display:none;position:absolute;top:100%%;left:0;right:0;flex-direction:column;gap:0;background:#fff;padding:4px 22px 14px;border-bottom:2px solid var(--ink)}
nav.links a{padding:12px 0;border-bottom:1px solid var(--rule)}header.open nav.links{display:flex}.burger{display:block}.nav .tel{display:none}}
/* héros : plan coté + cartouche */
.hero{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:clamp(28px,5vw,64px);align-items:center;padding-top:clamp(40px,6vw,84px);padding-bottom:clamp(40px,6vw,84px)}
.hero h1{font-size:clamp(2.6rem,6.2vw,5rem);text-transform:uppercase}
.hero .sub{font-family:%(head)s;font-size:clamp(1.2rem,2.2vw,1.6rem);font-weight:500;margin-top:14px;color:var(--cote)}
.hero p.lead{margin:18px 0 26px;max-width:46ch;color:var(--graphite)}
.hero .ctas{display:flex;flex-wrap:wrap;gap:12px}
.sheet{background:#fff;border:2px solid var(--ink);position:relative}
.sheet svg{display:block;width:100%%;height:auto}
.cart{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border-top:2px solid var(--ink)}
.cart div{padding:10px 14px;border-right:1px solid var(--ink);border-bottom:1px solid var(--ink)}.cart div:nth-child(2n){border-right:0}
.cart div:nth-last-child(-n+2){border-bottom:0}
.cart small{display:block;font-size:.72rem;color:var(--graphite)}.cart b{font-family:%(head)s;font-size:1.25rem;font-weight:600}
@media(max-width:860px){.hero{grid-template-columns:minmax(0,1fr)}}
section{padding:clamp(60px,8vw,104px) 0}
h2.h{font-size:clamp(2.1rem,4.4vw,3.3rem);max-width:22ch}
p.intro{color:var(--graphite);max-width:62ch;margin-top:12px}
/* parcours + mètre ruban */
.tabs{display:flex;flex-wrap:wrap;gap:0;margin-top:30px;border:2px solid var(--ink);width:max-content;max-width:100%%;background:#fff}
.tabs button{background:#fff;border:0;border-right:2px solid var(--ink);padding:11px 18px;font-weight:600;cursor:pointer}.tabs button:last-child{border-right:0}
.tabs button[aria-selected=true]{background:var(--ink);color:#fff}
.track{position:relative;margin-top:34px;padding-left:96px}
.tape{position:absolute;left:0;top:0;bottom:0;width:62px;background:var(--ribbon);border:2px solid var(--ink);transform-origin:top;
background-image:repeating-linear-gradient(180deg,var(--ink) 0 2px,transparent 2px 60px),repeating-linear-gradient(180deg,var(--ink) 0 1px,transparent 1px 12px);
background-size:26px 100%%,12px 100%%;background-repeat:no-repeat;background-position:right top,right top}
.track.run .tape{animation:unroll 1.1s ease-out both}@keyframes unroll{from{transform:scaleY(.04)}to{transform:scaleY(1)}}
.step{position:relative;padding:0 0 38px}.step:last-child{padding-bottom:6px}
.step .n{position:absolute;left:-96px;top:-4px;width:62px;text-align:left;padding-left:8px;font-family:%(head)s;font-weight:700;font-size:2rem;line-height:1}
.step .n::after{content:"";position:absolute;left:62px;top:16px;width:34px;border-top:2px solid var(--cote)}
.step h3{font-size:1.6rem}.step p{margin-top:6px;max-width:64ch}
.step ul{margin-top:12px;list-style:none;border-top:1px solid var(--rule);max-width:780px;background:#fff}
.step li{padding:10px 14px;border-bottom:1px solid var(--rule);border-left:1px solid var(--rule);border-right:1px solid var(--rule)}
.step li b{font-weight:600}.step li .v{display:inline-block;margin-left:6px;color:var(--cote);font-weight:600;white-space:nowrap}
.panel[hidden]{display:none}
@media(max-width:600px){.track{padding-left:58px}.tape{width:36px;background-size:16px 100%%,8px 100%%}.step .n{left:-58px;width:36px;font-size:1.4rem;padding-left:5px}.step .n::after{left:36px;width:22px;top:11px}}
/* nomenclature des diagnostics */
.nom{margin-top:34px;border-top:2px solid var(--ink);background:#fff}
.nom details{border-bottom:1px solid var(--ink)}
.nom summary{list-style:none;display:grid;grid-template-columns:96px minmax(0,1fr) auto;gap:18px;align-items:center;padding:12px 16px;cursor:pointer}
.nom summary::-webkit-details-marker{display:none}
.nom summary img{width:96px;height:64px;object-fit:cover;background:var(--grid)}
.nom summary h3{font-size:1.5rem}.nom summary span.t{display:block;color:var(--graphite);font-size:.95rem}
.nom summary .pl{font-family:%(head)s;font-size:1.9rem;font-weight:600;line-height:1;width:34px;text-align:center;color:var(--cote)}
.nom details[open] summary .pl{transform:rotate(45deg)}
.nom details.noimg summary{grid-template-columns:minmax(0,1fr) auto;padding:16px 16px 16px 20px;border-left:6px solid var(--ribbon)}
.nom details.noimg .body{padding-left:26px}
.nom summary:hover h3{color:var(--cote)}
.nom .body{padding:4px 16px 24px 130px;display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:28px}
.nom .body p+p{margin-top:10px}.nom dl{border-top:1px solid var(--rule)}.nom dl div{display:flex;justify-content:space-between;gap:14px;padding:8px 0;border-bottom:1px solid var(--rule)}
.nom dt{color:var(--graphite)}.nom dd{font-weight:600;text-align:right}
.dpe{margin-top:16px;display:grid;gap:4px}.dpe span{display:block;font-family:%(head)s;font-weight:700;font-size:1.05rem;padding:3px 10px;clip-path:polygon(0 0,calc(100%% - 14px) 0,100%% 50%%,calc(100%% - 14px) 100%%,0 100%%)}
.dpe small{font-size:.8rem;color:var(--graphite)}
@media(max-width:760px){.nom summary{grid-template-columns:64px minmax(0,1fr) auto;gap:12px}.nom summary img{width:64px;height:48px}.nom .body{padding:4px 16px 22px;grid-template-columns:minmax(0,1fr)}}
/* champs d'intervention */
.fields{margin-top:34px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:2px solid var(--ink);border-left:1px solid var(--ink)}
.fields div{padding:20px 20px 24px;border-right:1px solid var(--ink);border-bottom:1px solid var(--ink);background:#fff}
.fields h3{font-size:1.45rem;margin-bottom:6px}.fields ul{margin:8px 0 0 18px}
@media(max-width:900px){.fields{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:600px){.fields{grid-template-columns:minmax(0,1fr)}}
/* confiance */
.trust{background:var(--ink);color:#fff;background-image:none}
.trust .cols{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:48px;margin-top:30px}
.trust blockquote{border-left:4px solid var(--ribbon);padding:4px 0 4px 18px;margin-bottom:24px;font-size:1.08rem}
.trust blockquote cite{display:block;font-style:normal;font-size:.85rem;opacity:.75;margin-top:6px}
.trust h3{font-size:1.5rem;margin-bottom:10px}.trust ul{list-style:none}.trust li{padding:8px 0;border-bottom:1px solid rgba(255,255,255,.2)}
.trust p.intro{color:rgba(255,255,255,.8)}
@media(max-width:820px){.trust .cols{grid-template-columns:minmax(0,1fr)}}
/* zone */
.zone{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:40px;align-items:start}
.towns{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px;list-style:none}.towns li{border:1px solid var(--ink);background:#fff;padding:4px 10px;font-size:.93rem}
.map{width:100%%;height:400px;border:2px solid var(--ink)}
@media(max-width:820px){.zone{grid-template-columns:minmax(0,1fr)}.map{height:300px}}
/* devis */
.devis{border:2px solid var(--ink);background:#fff;display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr)}
.devis>div{padding:clamp(24px,4vw,44px)}.devis>div+div{border-left:2px solid var(--ink);background:var(--ribbon)}
.devis ol{margin:16px 0 0 20px}.devis li{margin-bottom:4px}
.devis dl div{padding:9px 0;border-bottom:1px solid var(--ink)}.devis dt{font-size:.82rem}.devis dd{font-weight:600;font-size:1.08rem}
.devis .ctas{display:flex;flex-wrap:wrap;gap:12px;margin-top:22px}
@media(max-width:820px){.devis{grid-template-columns:minmax(0,1fr)}.devis>div+div{border-left:0;border-top:2px solid var(--ink)}}
footer{background:#fff;border-top:2px solid var(--ink);padding:44px 0 110px;font-size:.93rem}
footer .w{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr) minmax(0,1.2fr);gap:30px}
footer h3{font-size:1.15rem;margin-bottom:6px}footer p+p{margin-top:6px}
@media(max-width:820px){footer .w{grid-template-columns:minmax(0,1fr)}}
"""

PLAN_SVG = """<svg viewBox="0 0 520 330" role="img" aria-label="Plan d'appartement coté, dessin d'illustration">
<g fill="none" stroke="var(--ink)" stroke-width="7" stroke-linejoin="miter">
<path d="M60 60 H300 M330 60 H470 V280 H260 M220 280 H60 V60"/><path d="M250 60 V150 M250 190 V280" stroke-width="4"/><path d="M250 170 H340 M380 170 H470" stroke-width="4"/></g>
<g fill="none" stroke="var(--ink)" stroke-width="1.5"><path d="M300 60 A30 30 0 0 0 330 90"/><path d="M220 280 A40 40 0 0 1 260 240"/><path d="M250 150 A40 40 0 0 1 290 190" stroke-dasharray="3 3"/></g>
<g stroke="var(--cote)" stroke-width="1.5" fill="var(--cote)">
<path d="M60 30 H470 M60 22 V38 M470 22 V38"/><path d="M30 60 V280 M22 60 H38 M22 280 H38"/><path d="M490 60 V170 M482 60 H498 M482 170 H498"/>
<path d="M60 30 l8 -4 v8z M470 30 l-8 -4 v8z M30 60 l-4 8 h8z M30 280 l-4 -8 h8z M490 60 l-4 8 h8z M490 170 l-4 -8 h8z" stroke="none"/></g>
<g font-family="Barlow Condensed, sans-serif" font-weight="600" font-size="15" fill="var(--ink)">
<text x="125" y="170">Séjour</text><text x="335" y="120">Chambre</text><text x="340" y="232">Cuisine</text></g>
<g fill="var(--ribbon)" stroke="var(--ink)" stroke-width="1.5"><rect x="88" y="214" width="122" height="22"/></g>
<g stroke="var(--ink)" stroke-width="1.2"><path d="M98 214 v8 M108 214 v5 M118 214 v8 M128 214 v5 M138 214 v8 M148 214 v5 M158 214 v8 M168 214 v5 M178 214 v8 M188 214 v5 M198 214 v8"/></g>
</svg>"""


_img = lambda u, c: (f'<img class="ph {c}" src="{a(u)}" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.remove()">' if u else "")


def _tab_panels(tabs):
    btns, panels = [], []
    for i, t in enumerate(tabs):
        sel = "true" if i == 0 else "false"
        btns.append(f'<button role="tab" id="tb-{a(t["id"])}" aria-controls="pn-{a(t["id"])}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}">{e(t["label"])}</button>')
        steps = []
        for n, s in enumerate(t["steps"], 1):
            lst = ""
            if s.get("list"):
                lis = []
                for it in s["list"]:
                    if isinstance(it, list):
                        v = f'<span class="v">{e(it[2])}</span>' if len(it) > 2 and it[2] else ""
                        lis.append(f'<li><b>{e(it[0])}</b> : {e(it[1])}{v}</li>')
                    else:
                        lis.append(f"<li>{e(it)}</li>")
                lst = "<ul>" + "".join(lis) + "</ul>"
            steps.append(f'<div class="step"><span class="n" aria-hidden="true">{n}</span><h3><span class="sr">Étape {n} : </span>{e(s["t"])}</h3>'
                         f'{"".join(f"<p>{e(p)}</p>" for p in s.get("text", []))}{lst}</div>')
        hid = "" if i == 0 else " hidden"
        panels.append(f'<div class="panel" role="tabpanel" id="pn-{a(t["id"])}" aria-labelledby="tb-{a(t["id"])}"{hid}>{_img(t.get("img"), "tabimg")}<div class="track"><div class="tape" aria-hidden="true"></div>{"".join(steps)}</div></div>')
    return f'<div class="tabs" role="tablist" aria-label="Choisir votre projet">{"".join(btns)}</div>{"".join(panels)}'


def _dpe():
    rows = "".join(f'<span style="width:{34 + i * 10}%;background:{c};color:{f}">{l}</span>' for i, (l, c, f) in enumerate(DPE))
    return f'<div class="dpe" role="img" aria-label="Échelle de l\'étiquette énergie, de A à G">{rows}</div>'


def _nom(items):
    out = []
    for it in items:
        img = f'<img src="{a(it["img"])}" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.style.visibility=\'hidden\'">' if it.get("img") else ""
        facts = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in it.get("facts", []))
        dpe = (_dpe() + f'<small>{e(it["dpe_note"])}</small>') if it.get("dpe") else ""
        cls = "" if img else ' class="noimg"'
        out.append(f'''<details id="{a(it["id"])}"{cls}><summary>{img}<span><h3>{e(it["name"])}</h3><span class="t">{e(it["tag"])}</span></span><span class="pl" aria-hidden="true">+</span></summary>
<div class="body"><div>{"".join(f"<p>{e(p)}</p>" for p in it["text"])}</div><div><dl>{facts}</dl>{dpe}</div></div></details>''')
    return '<div class="nom">' + "".join(out) + "</div>"


def render(d):
    t = d["theme"]
    css = CSS % {"ink": t["ink"], "paper": t["paper"], "cote": t["cote"], "ribbon": t["ribbon"], "graphite": t["graphite"],
                 "head": t.get("head", '"Barlow Condensed",system-ui,sans-serif'), "body": t.get("body", '"Barlow",system-ui,sans-serif')}
    h, c = d["hero"], d["devis"]
    mail = "mailto:" + c["email"] + "?subject=" + urllib.parse.quote(c["mail_subject"]) + "&body=" + urllib.parse.quote(c["mail_body"])
    nav = "".join(f'<a href="#{a(k)}">{e(v)}</a>' for k, v in d["nav"])
    cart = "".join(f"<div><small>{e(k)}</small><b>{e(v)}</b></div>" for k, v in h["cartouche"])
    fields = "".join(f'<div><h3>{e(f["t"])}</h3>{"".join(f"<p>{e(p)}</p>" for p in f.get("text", []))}'
                     f'{("<ul>" + "".join(f"<li>{e(x)}</li>" for x in f["list"]) + "</ul>") if f.get("list") else ""}</div>' for f in d["patrimoine"]["items"])
    tr = d["confiance"]
    avis = "".join(f'<blockquote><p>« {e(q)} »</p><cite>{e(tr["avis_cite"])}</cite></blockquote>' for q in tr["avis"])
    refs = "".join(f"<li>{e(r)}</li>" for r in tr["refs"])
    z = d["zone"]
    towns = "".join(f"<li>{e(x)}</li>" for x in z["towns"])
    info = "".join(f"<li>{e(x)}</li>" for x in c["infos"])
    rows = "".join(f"<div><dt>{e(k)}</dt><dd>{v}</dd></div>" for k, v in [
        ("Téléphone", f'<a href="tel:{a(c["tel"])}">{e(c["phone"])}</a>'), ("E-mail", f'<a href="mailto:{a(c["email"])}">{e(c["email"])}</a>'),
        ("Adresse", e(c["address"])), ("Rendez-vous", e(c["hours"]))])
    so = d.get("societe")
    soc = (f'<section id="societe" style="padding-top:10px"><div class="w soc">{_img(so.get("img"), "")}<div><h2 class="h">{e(so["title"])}</h2>'
           + "".join(f"<p>{e(p)}</p>" for p in so["paras"]) + '</div></div></section>') if so else ""
    f = d["footer"]
    body = f'''<header id="top"><div class="w nav"><a href="#accueil" aria-label="{a(d["brand"])}, retour en haut">{logo(d)}</a>
<nav class="links" aria-label="Menu principal">{nav}</nav><a class="btn tel" href="tel:{a(c["tel"])}">Appeler le {e(c["phone"])}</a>
<button class="burger" aria-expanded="false" aria-controls="menu">Menu</button></div></header>
<main id="accueil">
<div class="w hero"><div><h1>{e(h["title"])}</h1><p class="sub">{e(h["sub"])}</p><p class="lead">{e(h["lead"])}</p>
<div class="ctas"><a class="btn" href="{a(mail)}">Demander un devis par e-mail</a><a class="btn line" href="tel:{a(c["tel"])}">Appeler le {e(c["phone"])}</a></div></div>
<figure class="sheet">{PLAN_SVG}<figcaption class="cart">{cart}</figcaption></figure></div>
{('<div class="w">' + _img(h.get("img"), "band") + '</div>') if h.get("img") else ""}
{soc}
<section id="parcours" style="padding-top:20px"><div class="w"><h2 class="h">{e(d["parcours"]["title"])}</h2><p class="intro">{e(d["parcours"]["lead"])}</p>
{_tab_panels(d["parcours"]["tabs"])}</div></section>
<section id="diagnostics" style="padding-top:0"><div class="w"><h2 class="h">{e(d["diagnostics"]["title"])}</h2><p class="intro">{e(d["diagnostics"]["lead"])}</p>{_nom(d["diagnostics"]["items"])}</div></section>
<section id="patrimoine" style="padding-top:0"><div class="w"><h2 class="h">{e(d["patrimoine"]["title"])}</h2><p class="intro">{e(d["patrimoine"]["lead"])}</p><div class="fields">{fields}</div></div></section>
<section class="trust" id="confiance"><div class="w"><h2 class="h">{e(tr["title"])}</h2><p class="intro">{e(tr["lead"])}</p>
<div class="cols"><div>{avis}</div><div><h3>{e(tr["refs_title"])}</h3><ul>{refs}</ul><h3 style="margin-top:28px">{e(tr["op_title"])}</h3>{_img(tr.get("op_img"), "opimg")}<p>{e(tr["op_text"])}</p></div></div></div></section>
<section id="zone"><div class="w zone"><div><h2 class="h">{e(z["title"])}</h2><p class="intro">{e(z["text"])}</p><ul class="towns">{towns}</ul>{_img(z.get("img"), "zimg")}</div>{map_iframe(z["map_q"])}</div></section>
<section id="devis" style="padding-top:0"><div class="w"><div class="devis"><div><h2 class="h">{e(c["title"])}</h2><p class="intro">{e(c["text"])}</p><ol>{info}</ol>
<div class="ctas"><a class="btn" href="{a(mail)}">Demander un devis par e-mail</a><a class="btn line" href="tel:{a(c["tel"])}">Appeler le {e(c["phone"])}</a></div></div>
<div><h3 class="hd" style="font-size:1.6rem;margin-bottom:8px">{e(d["brand"])}</h3><dl>{rows}</dl></div></div></div></section>
</main>
<footer><div class="w"><div>{logo(d, 40)}<p style="margin-top:12px">{e(f["about"])}</p></div>
<div><h3>Contact</h3>{"".join(f"<p>{e(x)}</p>" for x in f["contact"])}</div>
<div><h3>Mentions</h3>{"".join(f"<p>{e(x)}</p>" for x in f["legal"])}</div></div></footer>'''
    js = """
const H=document.getElementById('top'),B=H.querySelector('.burger');B.onclick=()=>{const o=H.classList.toggle('open');B.setAttribute('aria-expanded',o)};
H.querySelectorAll('nav a').forEach(l=>l.onclick=()=>{H.classList.remove('open');B.setAttribute('aria-expanded',false)});
const T=[...document.querySelectorAll('[role=tab]')];
const sel=b=>{T.forEach(x=>{const on=x===b;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1;document.getElementById(x.getAttribute('aria-controls')).hidden=!on})};
T.forEach((b,i)=>{b.onclick=()=>sel(b);b.onkeydown=ev=>{if(ev.key==='ArrowRight'||ev.key==='ArrowLeft'){const n=T[(i+(ev.key==='ArrowRight'?1:T.length-1))%T.length];sel(n);n.focus()}}});
const tr=document.querySelector('#parcours .track');if(tr&&'IntersectionObserver' in window){const io=new IntersectionObserver(es=>{if(es[0].isIntersecting){tr.classList.add('run');io.disconnect()}},{threshold:.2});io.observe(tr)}
"""
    return page(d, css, body, t.get("fonts", DEF_FONTS), js)
