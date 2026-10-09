"""Briques communes à tous les styles de maquettes Fyce.

Chaque style (_generateur/styles/<nom>.py) expose render(d) -> HTML complet
et s'appuie sur ces helpers : enveloppe de page (noindex, polices), bandeau Fyce,
popup d'annonce, visionneuse photo, carte d'accès, logo avec repli texte.
"""
import html
import urllib.parse

FYCE = {"name": "Philippine Burnichon", "brand": "Fyce", "phone": "06 65 57 16 72",
        "tel": "+33665571672", "site": "https://fyce.space"}


def e(s):
    return html.escape(str(s or ""), quote=False)


def a(s):
    return html.escape(str(s or ""), quote=True)


def tgt(url):
    return ' target="_blank" rel="noopener"' if str(url).startswith("http") else ""


def logo(d, h=None, cls="logo-img"):
    """Logo du prospect ; si l'image ne charge pas, le nom s'affiche en texte."""
    lg = d.get("logo")
    if not lg:
        return f'<span class="logo-txt">{e(d["brand"])}</span>'
    h = h or lg.get("height", 44)
    return (f'<img class="{cls}" src="{a(lg["src"])}" alt="{a(d["brand"])}" style="height:{h}px;width:auto" '
            f'referrerpolicy="no-referrer" onerror="this.outerHTML=\'<span class=&quot;logo-txt&quot;>\'+this.alt+\'</span>\'">')


def map_iframe(q, cls="map"):
    return (f'<iframe class="{cls}" title="Plan d\'accès" loading="lazy" '
            f'src="https://maps.google.com/maps?q={urllib.parse.quote(q)}&amp;z=15&amp;output=embed"></iframe>')


FYCE_BAR = f'''<div class="fyce" role="note"><span><b>Proposition de maquette</b> réalisée par <a href="{FYCE["site"]}" target="_blank" rel="noopener">{FYCE["brand"]}</a>, {FYCE["name"]}, <a href="tel:{FYCE["tel"]}">{FYCE["phone"]}</a></span>
<button aria-label="Masquer ce bandeau" onclick="this.parentElement.remove()">×</button></div>'''

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
img,video,iframe{max-width:100%;display:block}a{color:inherit}button{font:inherit;color:inherit}
:focus-visible{outline:2px solid currentColor;outline-offset:3px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.fyce{position:fixed;left:14px;bottom:14px;z-index:90;display:flex;align-items:center;gap:10px;max-width:calc(100% - 28px);background:rgba(24,22,22,.93);color:#f5f2ec;padding:9px 10px 9px 15px;border-radius:999px;font:400 .76rem/1.35 system-ui,-apple-system,sans-serif;box-shadow:0 10px 30px -12px rgba(0,0,0,.6)}
.fyce b{font-weight:600}.fyce a{color:#f1d9b0}.fyce button{background:none;border:0;color:#f5f2ec;opacity:.7;cursor:pointer;font-size:1.1rem;padding:0 4px}
@media(max-width:560px){.fyce{font-size:.68rem;border-radius:12px}}
.lb{position:fixed;inset:0;z-index:110;background:rgba(10,9,9,.94);display:grid;grid-template-columns:56px 1fr 56px;align-items:center}.lb[hidden]{display:none}
.lb figure{text-align:center;padding:16px;color:#eee}.lb img{max-width:100%;max-height:82vh;margin:0 auto}.lb figcaption{margin-top:12px;font-size:.95rem;opacity:.85}
.lb button{background:none;border:0;color:#fff;cursor:pointer;font-size:2.4rem;line-height:1;opacity:.8}.lb .x{position:absolute;top:12px;right:18px}
.ann{position:fixed;inset:0;z-index:120;background:rgba(0,0,0,.5);display:grid;place-items:center;padding:20px}.ann[hidden]{display:none}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}html{scroll-behavior:auto}}
"""

LB_HTML = '''<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Photo agrandie" hidden><button class="x" aria-label="Fermer">×</button>
<button class="p" aria-label="Photo précédente">‹</button><figure><img alt="" referrerpolicy="no-referrer"><figcaption></figcaption></figure><button class="n" aria-label="Photo suivante">›</button></div>'''

LB_JS = """(()=>{const L=document.getElementById('lb');if(!L)return;const im=L.querySelector('img'),cap=L.querySelector('figcaption');let G=[],cur=0;
const show=i=>{cur=(i+G.length)%G.length;const g=G[cur];im.src=g.dataset.full;im.alt=g.dataset.alt||'';cap.textContent=g.dataset.cap||'';L.hidden=false;document.body.style.overflow='hidden'};
const close=()=>{L.hidden=true;document.body.style.overflow=''};
document.addEventListener('click',ev=>{const b=ev.target.closest('[data-full]');if(!b)return;G=[...document.querySelectorAll('[data-full]')].filter(x=>x.offsetParent!==null);show(G.indexOf(b))});
document.querySelectorAll('[data-full] img').forEach(i=>i.addEventListener('error',()=>i.closest('[data-full]').remove()));
L.querySelector('.x').onclick=close;L.querySelector('.p').onclick=()=>show(cur-1);L.querySelector('.n').onclick=()=>show(cur+1);
L.onclick=ev=>{if(ev.target===L||ev.target.tagName==='FIGURE')close()};
addEventListener('keydown',ev=>{if(L.hidden)return;if(ev.key==='Escape')close();if(ev.key==='ArrowLeft')show(cur-1);if(ev.key==='ArrowRight')show(cur+1)});})();"""


def announce(d, box_cls="ann-box"):
    an = d.get("announce")
    if not an:
        return ""
    cta = f'<a class="btn" href="{a(an["cta"][1])}"{tgt(an["cta"][1])}>{e(an["cta"][0])}</a>' if an.get("cta") else ""
    return f'''<div class="ann" id="ann" role="dialog" aria-modal="true" aria-labelledby="ann-t" hidden><div class="{box_cls}">
<button class="x" aria-label="Fermer">×</button><p class="ann-k">{e(an.get("kicker", ""))}</p>
<h2 id="ann-t">{e(an["title"])}</h2><p>{e(an["text"])}</p>{cta}</div></div>
<script>(()=>{{const A=document.getElementById('ann');let seen=false;try{{seen=sessionStorage.getItem('ann')==='1'}}catch(x){{}}
const close=()=>{{A.hidden=true;try{{sessionStorage.setItem('ann','1')}}catch(x){{}}}};
if(!seen)setTimeout(()=>{{A.hidden=false;A.querySelector('.x').focus()}},1400);A.querySelector('.x').onclick=close;A.onclick=ev=>{{if(ev.target===A)close()}};
A.querySelectorAll('a').forEach(l=>l.addEventListener('click',close));addEventListener('keydown',ev=>{{if(ev.key==='Escape'&&!A.hidden)close()}});}})();</script>'''


LOGO_JS = r"""<script>(function(){const src=document.body.dataset.logo;if(!src)return;const i=new Image();i.crossOrigin='anonymous';i.referrerPolicy='no-referrer';
i.onload=()=>{try{const W=Math.min(240,i.naturalWidth),H=Math.max(1,Math.round(i.naturalHeight*W/i.naturalWidth)),c=document.createElement('canvas');c.width=W;c.height=H;
const x=c.getContext('2d');x.drawImage(i,0,0,W,H);const d=x.getImageData(0,0,W,H).data;const B={};let op=0;
for(let k=0;k<d.length;k+=4){if(d[k+3]<200)continue;op++;const r=d[k]/255,g=d[k+1]/255,b=d[k+2]/255,mx=Math.max(r,g,b),mn=Math.min(r,g,b),l=(mx+mn)/2,df=mx-mn;
if(!df)continue;const s=df/(1-Math.abs(2*l-1));if(s<.35||l<.12||l>.78)continue;let h=mx===r?((g-b)/df)%6:mx===g?(b-r)/df+2:(r-g)/df+4;h=(h*60+360)%360;
const q=Math.round(h/20)%18;const o=B[q]||(B[q]={n:0,r:0,g:0,b:0});o.n++;o.r+=d[k];o.g+=d[k+1];o.b+=d[k+2]}
const best=Object.values(B).sort((a,b)=>b.n-a.n)[0];if(!best||best.n<op*.03)return;
let rgb=[best.r/best.n,best.g/best.n,best.b/best.n];const lum=a=>{const f=v=>(v/=255)<=.03928?v/12.92:((v+.055)/1.055)**2.4;return .2126*f(a[0])+.7152*f(a[1])+.0722*f(a[2])};
let n=0;while(1.05/(lum(rgb)+.05)<4.2&&n++<20)rgb=rgb.map(v=>v*.92);const hex=a=>'#'+a.map(v=>Math.round(v).toString(16).padStart(2,'0')).join('');
const R=document.documentElement.style,V=(document.body.dataset.logoVars||'--accent,--accent-2').split(',');R.setProperty(V[0],hex(rgb));if(V[1])R.setProperty(V[1],hex(rgb.map(v=>v*.85)));document.documentElement.dataset.logoAccent=hex(rgb)}catch(e){}};i.src=src})()</script>"""


def page(d, css, body, fonts, extra_js=""):
    """Enveloppe HTML commune. css = CSS propre au style ; body = contenu."""
    gallery = 'data-full=' in body
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>{e(d["title"])}</title>
<meta name="description" content="{a(d["description"])}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{a(fonts)}" rel="stylesheet">
<style>{BASE_CSS}{css}</style>
</head>
<body{(' data-logo="' + a(d['logo']['src']) + '" data-logo-vars="' + a(d['theme'].get('logo_vars', '--accent,--accent-2')) + '"') if d.get('logo') and d.get('theme', {}).get('logo_accent', True) else ''}>
{body}
{LB_HTML if gallery else ""}
{announce(d)}
{FYCE_BAR}
<script>{LB_JS if gallery else ""}{extra_js}</script>
{LOGO_JS if d.get('logo') and d.get('theme', {}).get('logo_accent', True) else ''}
</body>
</html>'''
