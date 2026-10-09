#!/usr/bin/env python3
"""Générateur de maquettes Fyce.

Usage : python3 build.py sites/<prospect>.json [...]
Chaque fichier JSON décrit le contenu d'un prospect ; la page est écrite dans
../<slug>/index.html (dossier publié par Hostinger). Les maquettes sont toujours
non indexées et portent le bandeau « Proposition de maquette — Fyce ».
"""
import json, sys, html, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent / "site"
FYCE = {"name": "Philippine Burnichon", "brand": "Fyce", "phone": "06 65 57 16 72",
        "tel": "+33665571672", "site": "https://fyce.space"}

e = html.escape


def attr(s):
    return html.escape(s, quote=True)


CSS = """
:root{--paper:%(paper)s;--paper-2:%(paper2)s;--ink:%(ink)s;--muted:%(muted)s;--accent:%(accent)s;--accent-2:%(accent2)s;
--gold:%(gold)s;--line:rgba(0,0,0,.12);--serif:%(serif)s;--sans:%(sans)s;--max:1200px}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--paper);color:var(--ink);font-family:var(--sans);font-weight:300;line-height:1.7;-webkit-font-smoothing:antialiased}
img{max-width:100%%;display:block}a{color:inherit;text-decoration:none}
.wrap{max-width:var(--max);margin:0 auto;padding:0 24px}
.eyebrow{font-size:.72rem;letter-spacing:.26em;text-transform:uppercase;color:var(--gold);font-weight:600}
h1,h2,h3{font-family:var(--serif);font-weight:500;line-height:1.08;letter-spacing:-.01em}
h2{font-size:clamp(2.1rem,4.5vw,3.5rem)}h3{font-size:1.5rem}
em.it,h1 em,h2 em{font-style:italic}
.btn{display:inline-flex;align-items:center;gap:.6em;padding:14px 28px;border:1px solid currentColor;font-size:.78rem;letter-spacing:.16em;text-transform:uppercase;font-weight:500;transition:.3s;background:none;cursor:pointer;font-family:var(--sans)}
.btn.solid{background:var(--accent);border-color:var(--accent);color:#fff}.btn.solid:hover{background:var(--accent-2);border-color:var(--accent-2)}
.btn.ghost{color:#fff}.btn.ghost:hover{background:#fff;color:var(--ink)}
header{position:fixed;inset:0 0 auto;z-index:50;transition:background .35s,box-shadow .35s,color .35s;color:#fff}
header.scrolled{background:color-mix(in srgb,var(--paper) 94%%,transparent);backdrop-filter:blur(10px);color:var(--ink);box-shadow:0 1px 0 var(--line)}
.nav{display:flex;align-items:center;justify-content:space-between;height:80px}
.logo{font-family:var(--serif);font-size:1.45rem;line-height:1}
header.haslogo{background:color-mix(in srgb,var(--paper) 95%%,transparent);backdrop-filter:blur(10px);color:var(--ink);box-shadow:0 1px 0 var(--line)}
.logo img{display:block;width:auto;max-width:60vw;object-fit:contain}
.flogo{display:inline-block;background:var(--paper);padding:10px 14px;border-radius:6px}.flogo img{display:block;width:auto;max-width:240px}
.logo small{display:block;font-family:var(--sans);font-size:.58rem;letter-spacing:.3em;text-transform:uppercase;opacity:.75;margin-top:6px}
.links{display:flex;gap:32px;font-size:.76rem;letter-spacing:.14em;text-transform:uppercase}
.links a{position:relative;padding:6px 0;white-space:nowrap}.logo{flex-shrink:0;margin-right:24px}@media(max-width:1280px){.links{gap:20px;font-size:.7rem;letter-spacing:.1em}}.links a::after{content:"";position:absolute;left:0;bottom:0;width:0;height:1px;background:currentColor;transition:width .3s}.links a:hover::after{width:100%%}
.burger{display:none;background:none;border:0;color:inherit;cursor:pointer;width:32px;height:32px}.burger span{display:block;height:1px;background:currentColor;margin:7px 0}
@media(max-width:860px){.links{position:fixed;inset:80px 0 auto;flex-direction:column;gap:0;background:var(--paper);color:var(--ink);padding:8px 24px 24px;transform:translateY(-130%%);transition:transform .4s;box-shadow:0 10px 30px rgba(0,0,0,.08)}
.links a{padding:16px 0;border-bottom:1px solid var(--line)}header.open .links{transform:none}header.open{background:var(--paper);color:var(--ink)}.burger{display:block}}
@media(min-width:861px) and (max-width:1180px){header.many .links{position:fixed;inset:80px 0 auto;flex-direction:column;gap:0;background:var(--paper);color:var(--ink);padding:8px 24px 24px;transform:translateY(-130%%);transition:transform .4s;box-shadow:0 10px 30px rgba(0,0,0,.08)}
header.many .links a{padding:16px 0;border-bottom:1px solid var(--line)}header.many.open .links{transform:none}header.many.open{background:var(--paper);color:var(--ink)}header.many .burger{display:block}}
.hero{position:relative;min-height:100svh;display:grid;place-items:end start;color:#fff;overflow:hidden;background:#222 center/cover}
.hero::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.45) 0%%,rgba(0,0,0,.2) 30%%,rgba(0,0,0,.55) 60%%,rgba(0,0,0,.82) 100%%)}
.hero .wrap{position:relative;padding-bottom:12vh;width:100%%}
.hero .eyebrow{display:inline-flex;align-items:center;gap:14px;color:#fff3df;font-size:.8rem;letter-spacing:.22em;text-shadow:0 1px 2px rgba(0,0,0,.7),0 0 18px rgba(0,0,0,.55)}
.hero .eyebrow::before{content:"";width:42px;height:1px;background:currentColor}
.hero h1{font-size:clamp(2.8rem,8.5vw,7rem);font-weight:400;margin:18px 0 22px;text-shadow:0 2px 20px rgba(0,0,0,.35)}
.hero h1 em{color:%(heroem)s}
.hero p{max-width:560px;font-size:1.08rem;opacity:.95;margin-bottom:34px;text-shadow:0 2px 14px rgba(0,0,0,.4)}
.hero .ctas{display:flex;gap:14px;flex-wrap:wrap}
@media(max-width:560px){.hero .eyebrow{font-size:.68rem;letter-spacing:.14em}.hero .eyebrow::before{width:22px}}
.figures{border-bottom:1px solid var(--line)}.figures .wrap{display:grid;grid-template-columns:repeat(4,1fr)}
.fig{padding:44px 16px;text-align:center;border-right:1px solid var(--line)}.fig:last-child{border-right:0}
.fig b{display:block;font-family:var(--serif);font-weight:400;font-size:3rem;color:var(--accent);line-height:1.05}
.fig span{font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
@media(max-width:760px){.figures .wrap{grid-template-columns:repeat(2,1fr)}.fig:nth-child(2){border-right:0}.fig:nth-child(-n+2){border-bottom:1px solid var(--line)}}
section{padding:clamp(80px,11vw,140px) 0}
.split{display:grid;grid-template-columns:1fr 1fr;gap:clamp(40px,7vw,110px);align-items:center}
.split .img{aspect-ratio:4/5;background:var(--paper-2) center/cover;position:relative}
.split .img::after{content:"";position:absolute;inset:18px -18px -18px 18px;border:1px solid var(--gold);z-index:-1}
.split h2{margin:16px 0 26px}.split p{margin-bottom:18px;max-width:520px;color:color-mix(in srgb,var(--ink) 85%%,transparent)}
.sign{font-family:var(--serif);font-style:italic;font-size:1.3rem;color:var(--accent);margin-top:24px}
@media(max-width:860px){.split{grid-template-columns:1fr}.split .img{aspect-ratio:4/3}}
.quote{text-align:center;background:var(--paper-2)}
.quote blockquote{font-family:var(--serif);font-size:clamp(1.7rem,3.6vw,2.8rem);font-style:italic;line-height:1.3;max-width:900px;margin:22px auto 22px;color:var(--accent)}
.quote p{max-width:600px;margin:0 auto;color:var(--muted)}
.feat{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--line);border:1px solid var(--line);margin-top:56px}
.feat div{background:var(--paper);padding:36px 28px}.feat i{font-style:normal;font-family:var(--serif);color:var(--gold)}
.feat h3{font-size:1.3rem;margin:10px 0}.feat p{font-size:.9rem;color:var(--muted)}
@media(max-width:960px){.feat{grid-template-columns:1fr 1fr}}@media(max-width:560px){.feat{grid-template-columns:1fr}}
.dark{background:var(--ink);color:color-mix(in srgb,var(--paper) 90%%,transparent)}
.dark .feat{background:rgba(255,255,255,.14);border-color:rgba(255,255,255,.14)}.dark .feat div{background:var(--ink)}.dark .feat p{color:rgba(255,255,255,.65)}
.head{text-align:center;max-width:660px;margin:0 auto 46px}.head h2{margin:14px 0 16px}.head p{color:var(--muted)}
.tabs{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin-bottom:46px}
.tabs button{font:inherit;font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;padding:11px 20px;border:1px solid var(--line);background:transparent;color:var(--ink);cursor:pointer;transition:.25s}
.tabs button[aria-pressed="true"],.tabs button:hover{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:22px}
.card{background:#fff;border:1px solid var(--line);padding:30px 26px 26px;display:flex;flex-direction:column;transition:transform .35s,box-shadow .35s;position:relative}
.card:hover{transform:translateY(-5px);box-shadow:0 22px 40px -22px rgba(0,0,0,.35)}
.card .tag{font-size:.64rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);display:flex;align-items:center;gap:8px}
.card .tag::before{content:"";width:9px;height:9px;border-radius:50%%;background:var(--c)}
.card h3{margin:12px 0 4px;font-size:1.4rem}.card .app{font-family:var(--serif);font-style:italic;color:var(--accent);margin-bottom:10px}
.card p{font-size:.88rem;color:var(--muted);flex:1}
.card .price{margin-top:18px;padding-top:14px;border-top:1px solid var(--line);display:flex;justify-content:space-between;align-items:baseline;font-size:.82rem;color:var(--muted)}
.card .price b{font-family:var(--serif);font-size:1.5rem;font-weight:500;color:var(--ink)}
.card .bimg{display:block;height:230px;width:100%%;object-fit:contain;margin:0 auto 18px}
.card svg.bimg{height:170px;margin:30px auto 48px}
.card .medal{font-size:.74rem;color:var(--gold);font-weight:600;margin-top:10px;line-height:1.4}
.gallery figcaption{padding:10px 4px 2px;font-size:.85rem;color:var(--muted);text-align:left;font-style:italic;font-family:var(--serif)}
.ann{position:fixed;inset:0;z-index:120;background:rgba(0,0,0,.55);display:grid;place-items:center;padding:20px}.ann[hidden]{display:none}
.ann>div{background:var(--paper);color:var(--ink);max-width:460px;width:100%%;padding:38px 34px 32px;position:relative;text-align:center;box-shadow:0 30px 60px -20px rgba(0,0,0,.5)}
.ann h3{font-size:1.7rem;margin:12px 0 14px;color:var(--accent)}.ann p{color:var(--muted);margin-bottom:24px}
.ann .x{position:absolute;top:10px;right:14px;background:none;border:0;font-size:1.6rem;cursor:pointer;color:var(--muted)}
.teamhero{width:100%%;aspect-ratio:16/7;object-fit:cover;margin-bottom:clamp(40px,6vw,70px);background:var(--paper-2)}
.picto{width:56px;height:56px;object-fit:contain;margin-bottom:6px}
.labels{display:flex;flex-wrap:wrap;gap:22px;align-items:center;margin-top:26px}.labels img{height:64px;width:auto;background:#fff;padding:6px;border-radius:4px}
.team{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:30px;text-align:center}
.team img{width:140px;height:140px;border-radius:50%%;object-fit:cover;margin:0 auto 14px;background:var(--paper-2)}
.team b{display:block;font-family:var(--serif);font-size:1.3rem;font-weight:500}.team span{color:var(--muted);font-size:.9rem}
.resa{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:clamp(26px,5vw,60px);background:#fff;border:1px solid var(--line);padding:clamp(24px,4vw,52px)}
.rform{display:grid;grid-template-columns:1fr 1fr;gap:14px}.rform .full{grid-column:1/-1}
.rform label{display:flex;flex-direction:column;gap:6px;font-size:.85rem;color:var(--muted)}
.rform input,.rform select,.rform textarea{font:inherit;color:var(--ink);padding:11px 12px;border:1px solid var(--line);background:var(--paper)}
@media(max-width:760px){.resa{grid-template-columns:minmax(0,1fr)}.rform{grid-template-columns:minmax(0,1fr)}}
.card dl.sheet{display:grid;grid-template-columns:auto 1fr;gap:3px 12px;font-size:.8rem;margin-top:14px;padding-top:12px;border-top:1px solid var(--line)}
.card dl.sheet dt{color:var(--muted)}.card dl.sheet dd{margin:0}
.menu.solo{grid-template-columns:minmax(0,760px);justify-content:center}
.tl{list-style:none;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));border-top:1px solid rgba(255,255,255,.25);margin-top:50px}
@media(min-width:961px){.tl[style]{grid-template-columns:repeat(min(var(--n),6),minmax(0,1fr))}}.tl li{padding:22px 20px 0 0;position:relative}.tl li::before{content:"";position:absolute;top:-5px;left:0;width:9px;height:9px;border-radius:50%%;background:var(--gold)}
.tl time{font-family:var(--serif);color:var(--gold);font-size:1.1rem}.tl h3{font-size:1.3rem;margin:6px 0 10px;color:#fff}.tl p{font-size:.88rem;opacity:.72}
@media(max-width:960px){.tl{grid-template-columns:1fr;border-top:0;border-left:1px solid rgba(255,255,255,.25)}.tl li{padding:0 0 30px 26px}.tl li::before{top:8px;left:-5px}}
.tlimgs{display:flex;gap:16px;flex-wrap:wrap;margin-top:34px}.tlimgs img{height:130px;width:auto;object-fit:contain}
.hero .hv{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover}.hero::before{z-index:1}.hero .wrap{z-index:2}
@media(prefers-reduced-motion:reduce){.hero .hv{display:none}}
.card.hide{display:none}.badge{position:absolute;top:14px;right:14px;font-size:.6rem;letter-spacing:.14em;text-transform:uppercase;background:var(--gold);color:#fff;padding:5px 9px}
.note{text-align:center;color:var(--muted);font-size:.82rem;margin-top:26px}
.menu{display:grid;grid-template-columns:1.5fr 1fr;gap:clamp(30px,5vw,70px);align-items:start}
.menu .col h3{font-size:1.15rem;letter-spacing:.14em;text-transform:uppercase;font-family:var(--sans);font-weight:600;color:var(--accent);margin:34px 0 10px}
.menu .col h3:first-child{margin-top:0}
.menu ul{list-style:none}.menu li{display:flex;justify-content:space-between;gap:16px;padding:11px 0;border-bottom:1px dashed var(--line)}
.menu li span{font-family:var(--serif);font-size:1.18rem}.menu li small{color:var(--muted);font-size:.8rem;white-space:nowrap}.menu li small:not(:empty){max-width:60%%}.menu li small{white-space:normal;text-align:right}@media(min-width:861px){.menu li small{white-space:nowrap;max-width:none}}.menu li span{min-width:0}
.menu aside{background:var(--ink);color:var(--paper);padding:38px 34px;position:sticky;top:100px}
.menu aside h3{font-size:1.9rem;margin-bottom:6px}.menu aside .big{font-family:var(--serif);font-size:3.4rem;color:var(--gold);line-height:1.1}
.menu aside p{opacity:.8;font-size:.9rem;margin:10px 0 18px}.menu aside ul li{border-color:rgba(255,255,255,.18)}.menu aside li small{color:rgba(255,255,255,.75)}
@media(max-width:860px){.menu{grid-template-columns:1fr}.menu aside{position:static}}
.booking{max-width:760px;margin:0 auto;background:#fff;border:1px solid var(--line);padding:12px}
.booking iframe{display:block;width:100%%;border:0;background:#fff}
.gallery{columns:3 260px;column-gap:14px}
.gallery button{display:block;width:100%%;margin:0 0 14px;padding:0;border:0;background:var(--paper-2);cursor:zoom-in;overflow:hidden;break-inside:avoid}
.gallery img{width:100%%;height:auto;transition:transform .6s,filter .4s}.gallery button:hover img{transform:scale(1.04);filter:brightness(.92)}
.lb{position:fixed;inset:0;z-index:100;background:rgba(10,8,7,.94);display:grid;grid-template-columns:60px 1fr 60px;align-items:center}.lb[hidden]{display:none}
.lb figure{text-align:center;padding:20px}.lb img{max-width:100%%;max-height:84vh;margin:0 auto}
.lb button{background:none;border:0;color:#fff;cursor:pointer;font-size:2.6rem;line-height:1;opacity:.8}.lb .x{position:absolute;top:14px;right:22px}
.banner{min-height:56vh;display:grid;place-items:center;text-align:center;color:#fff;position:relative;padding:0;background:#333 center/cover fixed}
.banner::before{content:"";position:absolute;inset:0;background:rgba(0,0,0,.55)}.banner>div{position:relative;padding:80px 24px}
.banner .eyebrow{color:#fff3df}.banner h2{font-weight:400;margin:16px 0 30px}
@media(max-width:860px){.banner{background-attachment:scroll}}
.visit{display:grid;grid-template-columns:1.05fr 1fr;background:#fff;border:1px solid var(--line)}
.visit .info{padding:clamp(34px,6vw,66px)}.visit h2{margin:14px 0 20px}
.visit dl{display:grid;grid-template-columns:120px 1fr;gap:16px 20px;margin:30px 0 36px;font-size:.95rem}
.visit dt{font-size:.68rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);padding-top:4px}
.visit dd a{border-bottom:1px solid var(--gold)}
.visit iframe{width:100%%;height:100%%;min-height:420px;border:0;filter:grayscale(.3)}
@media(max-width:860px){.visit{grid-template-columns:1fr}.visit dl{grid-template-columns:1fr;gap:2px}.visit dd{margin-bottom:12px}}
footer{background:var(--ink);color:color-mix(in srgb,var(--paper) 80%%,transparent);padding:64px 0 96px;font-size:.85rem}
footer .top{display:grid;grid-template-columns:2fr 1fr 1fr;gap:40px;padding-bottom:44px;border-bottom:1px solid rgba(255,255,255,.12)}
footer .logo{color:#fff}footer h4{font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);font-weight:600;margin-bottom:14px}
footer li{list-style:none;margin-bottom:8px}footer a:hover{color:#fff}
footer .bottom{display:flex;justify-content:space-between;flex-wrap:wrap;gap:14px;padding-top:24px;font-size:.74rem;opacity:.7}
@media(max-width:760px){footer .top{grid-template-columns:1fr}}
.rv{opacity:0;transform:translateY(26px);transition:opacity .9s,transform .9s}.rv.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.rv{opacity:1;transform:none}html{scroll-behavior:auto}}
.solo-text{max-width:820px}.solo-text h2{margin:16px 0 26px}.solo-text p{margin-bottom:18px;color:color-mix(in srgb,var(--ink) 85%%,transparent)}
.blocks{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%%,290px),1fr));gap:22px}
.blk{background:#fff;border:1px solid var(--line);padding:30px 26px;min-width:0;display:flex;flex-direction:column}
.blk .bi{width:calc(100%% + 52px);margin:-30px -26px 22px;aspect-ratio:4/3;object-fit:cover;background:var(--paper-2)}
.blk .bi.contain{object-fit:contain;background:#fff;padding:14px}
.blk .k{font-size:.68rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);font-weight:600}
.blk h3{font-size:1.35rem;margin:6px 0 12px}.blk p{font-size:.92rem;color:var(--muted);margin-bottom:10px}
.blk ul{list-style:none;margin-top:4px}.blk li{font-size:.92rem;padding:8px 0 8px 18px;border-bottom:1px dashed var(--line);position:relative}
.blk li::before{content:"";position:absolute;left:0;top:1.05em;width:6px;height:6px;border-radius:50%%;background:var(--accent)}
.blk a{border-bottom:1px solid var(--gold)}.blk .more{margin-top:auto;padding-top:14px;font-size:.85rem}
.chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}.chips span{border:1px solid var(--line);background:#fff;padding:7px 14px;border-radius:999px;font-size:.85rem}
.dark .blk{background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.14)}.dark .blk p{color:rgba(255,255,255,.7)}.dark .blk li{border-color:rgba(255,255,255,.14)}
.dark .head p{color:rgba(255,255,255,.7)}.dark .chips span{background:transparent;border-color:rgba(255,255,255,.25)}
.visit.nomap{grid-template-columns:1fr}
.fyce{position:fixed;left:16px;bottom:16px;z-index:90;display:flex;align-items:center;gap:12px;max-width:calc(100%% - 32px);background:rgba(20,18,16,.92);color:#f6f1e9;backdrop-filter:blur(8px);padding:10px 12px 10px 16px;border-radius:999px;font:400 .78rem/1.3 system-ui,sans-serif;box-shadow:0 10px 30px -10px rgba(0,0,0,.5)}
.fyce b{font-weight:600}.fyce a{color:#f0d9b5;text-decoration:underline;text-underline-offset:2px}
.fyce button{background:none;border:0;color:#f6f1e9;opacity:.7;cursor:pointer;font-size:1.1rem;line-height:1;padding:0 4px}
@media(max-width:560px){.fyce{font-size:.7rem;border-radius:14px}}
"""

LB = """<div class="lb" id="lb" role="dialog" aria-modal="true" hidden><button class="x" aria-label="Fermer">×</button>
<button class="p" aria-label="Précédente">‹</button><figure><img alt="" referrerpolicy="no-referrer"></figure><button class="n" aria-label="Suivante">›</button></div>"""

JS = """
const H=document.querySelector('header'),B=document.querySelector('.burger');
const sc=()=>H.classList.toggle('scrolled',scrollY>40);addEventListener('scroll',sc,{passive:true});sc();
B.onclick=()=>{const o=H.classList.toggle('open');B.setAttribute('aria-expanded',o)};
document.querySelectorAll('.links a').forEach(a=>a.onclick=()=>{H.classList.remove('open');B.setAttribute('aria-expanded',false)});
document.querySelectorAll('.tabs').forEach(t=>{const scope=t.parentElement;t.querySelectorAll('button').forEach(b=>b.onclick=()=>{
  t.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',x===b));const f=b.dataset.f;
  scope.querySelectorAll('.card').forEach(c=>c.classList.toggle('hide',f!=='all'&&c.dataset.cat!==f));});});
const G=[...document.querySelectorAll('.gallery button')],L=document.getElementById('lb');let cur=0;
if(L){const im=L.querySelector('img'),show=i=>{cur=(i+G.length)%G.length;im.src=G[cur].dataset.full;im.alt=G[cur].querySelector('img').alt;L.hidden=false;document.body.style.overflow='hidden'},
close=()=>{L.hidden=true;document.body.style.overflow=''};
G.forEach((g,i)=>{g.onclick=()=>show(i);g.querySelector('img').addEventListener('error',()=>g.remove())});
L.querySelector('.x').onclick=close;L.querySelector('.p').onclick=()=>show(cur-1);L.querySelector('.n').onclick=()=>show(cur+1);
L.onclick=e=>{if(e.target===L||e.target.tagName==='FIGURE')close()};
addEventListener('keydown',e=>{if(L.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(cur-1);if(e.key==='ArrowRight')show(cur+1)});}
const io=new IntersectionObserver(es=>es.forEach(x=>{if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}}),{threshold:.1});
document.querySelectorAll('.rv').forEach(el=>io.observe(el));
"""


def section_story(s):
    if not s.get("img"):
        paras = "".join(f"<p>{p}</p>" for p in s["paras"])
        sign = f'<p class="sign">{e(s["sign"])}</p>' if s.get("sign") else ""
        if s.get("logos"):
            sign += '<div class="labels">' + "".join(f'<img src="{attr(u)}" alt="{attr(al)}" loading="lazy" referrerpolicy="no-referrer">' for u, al in s["logos"]) + '</div>'
        cls = ' class="dark"' if s.get("dark") else ""
        return f'''<section id="{s["id"]}"{cls}><div class="wrap"><div class="solo-text rv"><span class="eyebrow">{e(s["eyebrow"])}</span><h2>{s["title"]}</h2>{paras}{sign}</div></div></section>'''
    paras = "".join(f"<p>{p}</p>" for p in s["paras"])
    sign = f'<p class="sign">{e(s["sign"])}</p>' if s.get("sign") else ""
    if s.get("logos"):
        sign += '<div class="labels">' + "".join(f'<img src="{attr(u)}" alt="{attr(al)}" loading="lazy" referrerpolicy="no-referrer">' for u, al in s["logos"]) + '</div>'
    return f'''<section id="{s["id"]}"><div class="wrap split">
<div class="img rv" style="background-image:url('{attr(s["img"])}')" role="img" aria-label="{attr(s.get("alt", ""))}"></div>
<div class="rv"><span class="eyebrow">{e(s["eyebrow"])}</span><h2>{s["title"]}</h2>{paras}{sign}</div></div></section>'''


def section_quote(q):
    return f'''<section class="quote"><div class="wrap rv"><span class="eyebrow">{e(q["eyebrow"])}</span>
<blockquote>{e(q["text"])}</blockquote><p>{e(q.get("sub", ""))}</p></div></section>'''


def section_features(f):
    def _it(n, it):
        ic = f'<img class="picto" src="{attr(it[2])}" alt="" loading="lazy" referrerpolicy="no-referrer">' if len(it) > 2 else f'<i>{n}.</i>'
        return f'<div>{ic}<h3>{e(it[0])}</h3><p>{e(it[1])}</p></div>'
    items = "".join(_it(n, it) for n, it in zip(["I", "II", "III", "IV", "V", "VI"], f["items"]))
    cls = ' class="dark"' if f.get("dark") else ""
    return f'''<section id="{f.get("id", "savoir-faire")}"{cls}><div class="wrap">
<div class="rv" style="max-width:660px"><span class="eyebrow">{e(f["eyebrow"])}</span>
<h2 style="margin:14px 0 18px">{f["title"]}</h2><p style="opacity:.8">{e(f.get("lead", ""))}</p></div>
<div class="feat rv">{items}</div></div></section>'''


def section_cards(o):
    tabs = ('<div class="tabs" role="group"><button aria-pressed="true" data-f="all">Tout</button>' + "".join(
        f'<button aria-pressed="false" data-f="{k}">{e(v)}</button>' for k, v in o["tabs"]) + '</div>') if o.get("tabs") else ""
    cards = []
    for c in o["items"]:
        badge = f'<span class="badge">{e(c["badge"])}</span>' if c.get("badge") else ""
        price = ""
        if c.get("price"):
            price = f'<div class="price"><span>{e(c.get("fmt", "Bouteille 75 cl"))}</span><b>{e(c["price"])}</b></div>'
        sil = f'<svg class="bimg" viewBox="0 0 40 120" aria-hidden="true"><path d="M16 2h8v30c0 6 10 10 10 22v58a6 6 0 0 1-6 6H12a6 6 0 0 1-6-6V54c0-12 10-16 10-22z" fill="{c.get("color", "#777")}" opacity=".85"/><rect x="10" y="66" width="20" height="28" fill="#fff" opacity=".9"/></svg>'
        if c.get("img"):
            img = f'<img class="bimg" src="{attr(c["img"])}" alt="{attr(c["name"])}" loading="lazy" referrerpolicy="no-referrer" onerror="this.outerHTML=this.dataset.sil" data-sil="{attr(sil)}">'
        elif any(x.get("img") for x in o["items"]):
            img = sil
        else:
            img = ""
        medal = f'<div class="medal">{e(c["medal"])}</div>' if c.get("medal") else ""
        cards.append(f'''<article class="card" data-cat="{c.get("cat", "")}" style="--c:{c.get("color", "var(--accent)")}">{badge}{img}
{f'<span class="tag">{e(c["tag"])}</span>' if c.get("tag") else ""}<h3>{e(c["name"])}</h3>{f'<div class="app">{e(c["app"])}</div>' if c.get("app") else ""}
<p>{e(c.get("desc", ""))}</p>{('<dl class="sheet">' + "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in c["sheet"]) + "</dl>") if c.get("sheet") else ""}{medal}{price}{f'<p class="note" style="text-align:left;margin-top:12px"><a href="{attr(c["link"][1])}" target="_blank" rel="noopener" style="border-bottom:1px solid var(--gold)">{e(c["link"][0])}</a></p>' if c.get("link") else ""}</article>''')
    note = f'<p class="note">{e(o["note"])}</p>' if o.get("note") else ""
    return f'''<section id="{o["id"]}"><div class="wrap"><div class="head rv"><span class="eyebrow">{e(o["eyebrow"])}</span>
<h2>{o["title"]}</h2><p>{e(o.get("lead", ""))}</p></div>{tabs}
<div class="grid">{"".join(cards)}</div>{note}</div></section>'''


def section_menu(o):
    cols = ""
    for sec in o["sections"]:
        lis = "".join(f'<li><span>{e(i[0])}</span><small>{e(i[1]) if len(i) > 1 else ""}</small></li>' for i in sec["items"])
        cols += f'<h3>{e(sec["title"])}</h3><ul>{lis}</ul>'
    a = o.get("aside")
    if not a:
        note = f'<p class="note" style="text-align:left">{e(o["note"])}</p>' if o.get("note") else ""
        return f'''<section id="{o["id"]}"><div class="wrap"><div class="head rv"><span class="eyebrow">{e(o["eyebrow"])}</span>
<h2>{o["title"]}</h2><p>{e(o.get("lead", ""))}</p></div><div class="menu solo"><div class="col rv">{cols}{note}</div></div></div></section>'''
    alis = "".join(f'<li><span>{e(i[0])}</span><small>{e(i[1])}</small></li>' for i in a.get("items", []))
    cta = ""
    if a.get("cta"):
        tgt = ' target="_blank" rel="noopener"' if a["cta"][1].startswith("http") else ""
        cta = f'<a class="btn solid" style="margin-top:24px" href="{attr(a["cta"][1])}"{tgt}>{e(a["cta"][0])}</a>'
    note = f'<p class="note" style="text-align:left">{e(o["note"])}</p>' if o.get("note") else ""
    return f'''<section id="{o["id"]}"><div class="wrap"><div class="head rv"><span class="eyebrow">{e(o["eyebrow"])}</span>
<h2>{o["title"]}</h2><p>{e(o.get("lead", ""))}</p></div>
<div class="menu"><div class="col rv">{cols}{note}</div>
<aside class="rv"><span class="eyebrow">{e(a["eyebrow"])}</span><h3>{e(a["title"])}</h3>
<div class="big">{e(a.get("big", ""))}</div><p>{e(a.get("text", ""))}</p><ul>{alis}</ul>{cta}</aside></div></div></section>'''


def section_booking(b):
    """Module de réservation existant du client (TheFork, Zenchef…), intégré tel quel dans la page."""
    h = b.get("height", 640)
    return f'''<section id="{b.get("id", "reserver")}" style="padding-top:0"><div class="wrap"><div class="head rv"><span class="eyebrow">{e(b["eyebrow"])}</span>
<h2>{b["title"]}</h2><p>{e(b.get("lead", ""))}</p></div>
<div class="booking rv"><iframe src="{attr(b["url"])}" title="{attr(b.get("label", "Module de réservation"))}" loading="lazy" style="height:{h}px"></iframe>
<p class="note">Le module ne s'affiche pas ? <a href="{attr(b["url"])}" target="_blank" rel="noopener" style="border-bottom:1px solid var(--gold)">Réserver dans un nouvel onglet</a></p></div></div></section>'''


def section_team(t):
    ppl = "".join(f'<figure><img src="{attr(p["img"])}" alt="{attr(p["name"])}" loading="lazy" referrerpolicy="no-referrer"><figcaption><b>{e(p["name"])}</b><span>{e(p["role"])}</span></figcaption></figure>' for p in t["people"])
    note = f'<p class="note">{e(t["note"])}</p>' if t.get("note") else ""
    big = f'<img class="teamhero" src="{attr(t["img"])}" alt="{attr(t.get("alt", ""))}" loading="lazy" referrerpolicy="no-referrer">' if t.get("img") else ""
    return f'''<section id="{t.get("id", "equipe")}"><div class="wrap">{big}<div class="head rv"><span class="eyebrow">{e(t["eyebrow"])}</span>
<h2>{t["title"]}</h2><p>{e(t.get("lead", ""))}</p></div><div class="team rv">{ppl}</div>{note}</div></section>'''


RESA_CSS = """<style>
.rm{background:var(--paper);color:var(--ink);border:1px solid var(--line);border-radius:4px;padding:28px;box-shadow:0 20px 50px rgba(0,0,0,.06);min-width:0}
.rm-steps{display:flex;gap:6px;margin-bottom:22px}.rm-steps i{flex:1;height:3px;background:var(--line);border-radius:2px}.rm-steps i.on{background:var(--accent)}
.rm h3{font-family:var(--serif);font-weight:400;font-size:1.35rem;margin:0 0 14px}
.rm-cov{display:flex;align-items:center;gap:14px;margin-bottom:22px}.rm-cov button{width:40px;height:40px;border-radius:50%;border:1px solid var(--line);background:none;font-size:1.2rem;cursor:pointer;color:inherit}
.rm-cov b{font-family:var(--serif);font-size:1.6rem;min-width:2ch;text-align:center;font-weight:400}
.rm-cal header{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;font-weight:600;text-transform:capitalize}
.rm-cal header button{background:none;border:1px solid var(--line);width:34px;height:34px;border-radius:50%;cursor:pointer;color:inherit}.rm-cal header button:disabled{opacity:.3;cursor:default}
.rm-grid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:4px;text-align:center}
.rm-grid span{font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding:4px 0}
.rm-grid button{height:40px;width:40px;max-width:100%;justify-self:center;border:0;background:none;border-radius:50%;cursor:pointer;font:inherit;color:inherit;padding:0}
.rm-grid button:hover:not(:disabled){background:color-mix(in srgb,var(--accent) 12%,transparent)}
.rm-grid button:disabled{color:var(--muted);opacity:.35;cursor:default;text-decoration:line-through}
.rm-grid button.sel,.rm-grid button.sel:hover{background:var(--accent);color:#fff}
.rm-slots h4{font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:16px 0 8px;font-weight:600}
.rm-slots div{display:flex;flex-wrap:wrap;gap:8px}.rm-slots button{border:1px solid var(--line);background:none;padding:9px 14px;border-radius:999px;cursor:pointer;font:inherit;color:inherit}
.rm-slots button.sel{background:var(--accent);border-color:var(--accent);color:#fff}
.rm-sum{background:var(--paper-2);padding:12px 16px;border-radius:4px;margin-bottom:18px;font-size:.92rem}
.rm form{display:grid;gap:12px}.rm label{display:grid;gap:6px;font-size:.82rem}
.rm input,.rm textarea{font:inherit;padding:12px;border:1px solid var(--line);border-radius:3px;background:#fff;color:#222;width:100%;box-sizing:border-box}
.rm-nav{display:flex;justify-content:space-between;gap:10px;margin-top:20px;align-items:center}
.rm-back{background:none;border:0;cursor:pointer;color:var(--muted);font:inherit;text-decoration:underline}
.rm .btn[disabled]{opacity:.4;pointer-events:none}
.rm-ok{text-align:center;padding:20px 0}.rm-ok .ck{width:56px;height:56px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;margin:0 auto 16px;font-size:1.6rem}
.rm [hidden]{display:none!important}
@media(max-width:480px){.rm{padding:20px 16px}}
.resa .rm{border:0;box-shadow:none;padding:0;background:none}
</style>"""

RESA_JS = r"""<script>document.querySelectorAll('.rm').forEach(R=>{const C=JSON.parse(R.dataset.cfg);
const st={n:2,d:null,h:null,step:0};const $=q=>R.querySelector(q);const today=new Date();today.setHours(0,0,0,0);
const maxD=new Date(today);maxD.setDate(maxD.getDate()+(C.ahead||60));let view=new Date(today.getFullYear(),today.getMonth(),1);
const fmt=d=>d.toLocaleDateString('fr-FR',{weekday:'long',day:'numeric',month:'long'});
const iso=d=>d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
const open=d=>C.days.includes(d.getDay())&&d>=today&&d<=maxD&&!(C.closed||[]).includes(iso(d));
function show(i){st.step=i;R.querySelectorAll('[data-step]').forEach(p=>p.hidden=+p.dataset.step!==i);
R.querySelectorAll('.rm-steps i').forEach((b,k)=>b.classList.toggle('on',k<=i));sum()}
function sum(){const t=(st.n+' couvert'+(st.n>1?'s':''))+(st.d?', '+fmt(st.d):'')+(st.h?' à '+st.h.replace(':','h'):'');R.querySelectorAll('.rm-sum').forEach(x=>x.textContent=t)}
function cal(){const g=$('.rm-grid');g.innerHTML='';['lun','mar','mer','jeu','ven','sam','dim'].forEach(x=>g.insertAdjacentHTML('beforeend','<span>'+x+'</span>'));
$('.rm-cal header b').textContent=view.toLocaleDateString('fr-FR',{month:'long',year:'numeric'});
const off=(view.getDay()+6)%7;for(let i=0;i<off;i++)g.insertAdjacentHTML('beforeend','<i></i>');
const last=new Date(view.getFullYear(),view.getMonth()+1,0).getDate();
for(let k=1;k<=last;k++){const d=new Date(view.getFullYear(),view.getMonth(),k);const b=document.createElement('button');b.type='button';b.textContent=k;
b.disabled=!open(d);b.setAttribute('aria-label',fmt(d));if(st.d&&+st.d===+d)b.classList.add('sel');b.onclick=()=>{st.d=d;st.h=null;cal();slots();sum()};g.appendChild(b)}
$('.rm-prev').disabled=view<=new Date(today.getFullYear(),today.getMonth(),1);$('.rm-nextm').disabled=new Date(view.getFullYear(),view.getMonth()+1,1)>maxD;
$('[data-next="1"]').disabled=!st.d}
function slots(){const w=$('.rm-slots');w.innerHTML='';$('[data-next="2"]').disabled=!st.h;if(!st.d)return;
const now=new Date();C.services.forEach(([lab,hs])=>{const ok=hs.filter(h=>{const[a,b]=h.split(':');const t=new Date(st.d);t.setHours(+a,+b);return t-now>3600e3});if(!ok.length)return;
w.insertAdjacentHTML('beforeend','<h4>'+lab+'</h4>');const box=document.createElement('div');ok.forEach(h=>{const b=document.createElement('button');b.type='button';b.textContent=h.replace(':','h');
if(st.h===h)b.classList.add('sel');b.onclick=()=>{st.h=h;slots();sum()};box.appendChild(b)});w.appendChild(box)});
if(!w.children.length)w.innerHTML='<p style="color:var(--muted);font-size:.9rem">Plus de créneau disponible ce jour-là.</p>'}
$('.rm-minus').onclick=()=>{st.n=Math.max(1,st.n-1);$('.rm-cov b').textContent=st.n;sum()};
$('.rm-plus').onclick=()=>{st.n=Math.min(C.max,st.n+1);$('.rm-cov b').textContent=st.n;sum()};
$('.rm-prev').onclick=()=>{view.setMonth(view.getMonth()-1);cal()};$('.rm-nextm').onclick=()=>{view.setMonth(view.getMonth()+1);cal()};
R.querySelectorAll('[data-next]').forEach(b=>b.onclick=()=>show(+b.dataset.next));R.querySelectorAll('.rm-back').forEach(b=>b.onclick=()=>show(st.step-1));
R.querySelector('form').onsubmit=ev=>{ev.preventDefault();const f=ev.target,v=n=>f.elements[n].value.trim();const hh=st.h.replace(':','h'),cv=st.n+' couvert'+(st.n>1?'s':'');
const s='Réservation '+st.d.toLocaleDateString('fr-FR')+' à '+hh+', '+cv;
const b='Bonjour,\n\nNouvelle demande de réservation :\n- '+cv+'\n- '+fmt(st.d)+' à '+hh+'\n\n'+(v('msg')?'Message : '+v('msg')+'\n\n':'')+v('nom')+'\n'+v('tel')+(v('mail')?'\n'+v('mail'):'');
location.href='mailto:'+C.to+'?subject='+encodeURIComponent(s)+'&body='+encodeURIComponent(b);$('.rm-ok p b').textContent=fmt(st.d)+' à '+hh;show(3)};
cal();slots();show(0)})</script>"""


def section_resaform(r):
    hours = r["hours"]
    services = r.get("services") or [[lab, hs] for lab, hs in (("Midi", [h for h in hours if int(h[:2]) < 17]), ("Soir", [h for h in hours if int(h[:2]) >= 17])) if hs]
    cfg = {"to": r["email"], "max": r.get("max", 40), "days": r.get("days", [1, 2, 3, 4, 5, 6]), "services": services,
           "ahead": r.get("ahead", 60), "closed": r.get("closed", [])}
    nxt = '<button type="button" class="btn solid" data-next="{n}">Continuer</button>'
    return f'''<section id="{r.get("id", "reserver")}"><div class="wrap"><div class="resa rv"><div>
<span class="eyebrow">{e(r["eyebrow"])}</span><h2 style="margin:14px 0 16px">{r["title"]}</h2><p style="color:var(--muted)">{e(r["lead"])}</p>
<p style="margin-top:22px">Par téléphone : <a href="tel:{attr(r["tel"])}" style="border-bottom:1px solid var(--gold)">{e(r["phone"])}</a></p>
<p style="margin-top:6px;color:var(--muted);font-size:.9rem">{e(r.get("note", ""))}</p></div>
<div class="rm" data-cfg="{attr(json.dumps(cfg, ensure_ascii=False))}" aria-live="polite"><div class="rm-steps"><i></i><i></i><i></i><i></i></div>
<div data-step="0"><h3>Combien serez-vous ?</h3><div class="rm-cov"><button type="button" class="rm-minus" aria-label="Un couvert de moins">&minus;</button><b>2</b><button type="button" class="rm-plus" aria-label="Un couvert de plus">+</button><span style="color:var(--muted)">couverts</span></div>
<h3>Quel jour ?</h3><div class="rm-cal"><header><button type="button" class="rm-prev" aria-label="Mois précédent">&lsaquo;</button><b></b><button type="button" class="rm-nextm" aria-label="Mois suivant">&rsaquo;</button></header><div class="rm-grid"></div></div>
<div class="rm-nav"><span></span>{nxt.format(n=1)}</div></div>
<div data-step="1" hidden><div class="rm-sum"></div><h3>À quelle heure ?</h3><div class="rm-slots"></div>
<div class="rm-nav"><button type="button" class="rm-back">Retour</button>{nxt.format(n=2)}</div></div>
<div data-step="2" hidden><div class="rm-sum"></div><h3>Vos coordonnées</h3><form>
<label>Nom<input name="nom" autocomplete="name" required></label><label>Téléphone<input name="tel" type="tel" autocomplete="tel" required></label>
<label>E-mail (facultatif)<input name="mail" type="email" autocomplete="email"></label><label>Un message, une allergie, une occasion ? (facultatif)<textarea name="msg" rows="2"></textarea></label>
<div class="rm-nav"><button type="button" class="rm-back">Retour</button><button class="btn solid" type="submit">Confirmer la réservation</button></div></form></div>
<div data-step="3" hidden><div class="rm-ok"><div class="ck">&#10003;</div><h3>Demande envoyée</h3><p>Votre table pour le <b></b> est demandée. {e(r["brand"])} vous confirme très vite.</p></div></div>
</div></div></div></section>''' + RESA_CSS + RESA_JS


def section_timeline(t):
    lis = "".join(f'<li><time>{e(x["when"])}</time><h3>{e(x["who"])}</h3><p>{e(x["text"])}</p></li>' for x in t["items"])
    imgs = "".join(f'<img src="{attr(u)}" alt="" loading="lazy" referrerpolicy="no-referrer">' for u in t.get("imgs", []))
    n = len(t["items"])
    tlst = f' style="--n:{n}"' if n != 5 else ""
    return f'''<section id="{t.get("id", "histoire")}" class="dark"><div class="wrap"><div class="rv" style="max-width:680px"><span class="eyebrow">{e(t["eyebrow"])}</span>
<h2 style="margin:14px 0 16px">{t["title"]}</h2><p style="opacity:.8">{e(t.get("lead", ""))}</p></div>{f'<div class="tlimgs">{imgs}</div>' if imgs else ""}<ol class="tl rv"{tlst}>{lis}</ol></div></section>'''


def section_gallery(g):
    btns = "".join(f'<button data-full="{attr(p["full"])}" aria-label="Agrandir"><img src="{attr(p["thumb"])}" alt="{attr(p.get("alt", ""))}" loading="lazy" referrerpolicy="no-referrer">'
                   + (f'<figcaption>{e(p["caption"])}</figcaption>' if p.get("caption") else "") + '</button>'
                   for p in g["photos"])
    lead = f'<p>{e(g["lead"])}</p>' if g.get("lead") else ""
    return f'''<section id="{g.get("id", "photos")}" style="padding-top:0"><div class="wrap"><div class="head rv"><span class="eyebrow">{e(g["eyebrow"])}</span>
<h2>{g["title"]}</h2>{lead}</div><div class="gallery">{btns}</div></div></section>'''


def section_banner(b):
    return f'''<div class="banner" style="background-image:url('{attr(b["img"])}')"><div class="rv"><span class="eyebrow">{e(b["eyebrow"])}</span>
<h2>{b["title"]}</h2><a href="{attr(b["cta"][1])}" class="btn ghost">{e(b["cta"][0])}</a></div></div>'''


def section_visit(v):
    rows = "".join(f"<dt>{e(k)}</dt><dd>{val}</dd>" for k, val in v["rows"])
    q = urllib.parse.quote(v.get("map_q", ""))
    cta = v["cta"]
    tgt = ' target="_blank" rel="noopener"' if cta[1].startswith("http") else ""
    return f'''<section id="{v.get("id", "contact")}" style="padding-top:0"><div class="wrap"><div class="visit{"" if v.get("map_q") else " nomap"} rv"><div class="info">
<span class="eyebrow">{e(v["eyebrow"])}</span><h2>{v["title"]}</h2><p style="color:var(--muted)">{e(v.get("text", ""))}</p>
<dl>{rows}</dl><a class="btn solid" href="{attr(cta[1])}"{tgt}>{e(cta[0])}</a></div>
{f'<iframe title="Plan d’accès" loading="lazy" src="https://maps.google.com/maps?q={q}&amp;z=15&amp;output=embed"></iframe>' if v.get("map_q") else ""}</div></div></section>'''


def section_blocks(b):
    """Rubriques génériques (prestations, compétences, actualités, presse, liens utiles, communes…) : cartes avec photo, texte, liste."""
    out = []
    for x in b.get("items", []):
        img = f'<img class="bi{" contain" if x.get("contain") else ""}" src="{attr(x["img"])}" alt="{attr(x.get("alt", ""))}" loading="lazy" referrerpolicy="no-referrer">' if x.get("img") else ""
        k = f'<span class="k">{e(x["kicker"])}</span>' if x.get("kicker") else ""
        h = f'<h3>{x["title"]}</h3>' if x.get("title") else ""
        ps = "".join(f"<p>{p}</p>" for p in x.get("paras", []))
        ul = ("<ul>" + "".join(f"<li>{i}</li>" for i in x["list"]) + "</ul>") if x.get("list") else ""
        more = f'<p class="more"><a href="{attr(x["link"][1])}"{" target=\"_blank\" rel=\"noopener\"" if x["link"][1].startswith("http") else ""}>{e(x["link"][0])}</a></p>' if x.get("link") else ""
        out.append(f'<article class="blk">{img}{k}{h}{ps}{ul}{more}</article>')
    chips = ('<div class="chips">' + "".join(f"<span>{e(c)}</span>" for c in b["chips"]) + "</div>") if b.get("chips") else ""
    note = f'<p class="note">{b["note"]}</p>' if b.get("note") else ""
    cls = ' class="dark"' if b.get("dark") else ""
    pad = ' style="padding-top:0"' if b.get("tight") else ""
    lead = f'<p>{b["lead"]}</p>' if b.get("lead") else ""
    grid = f'<div class="blocks rv">{"".join(out)}</div>' if out else ""
    return f'''<section id="{b.get("id", "rubriques")}"{cls}{pad}><div class="wrap"><div class="head rv"><span class="eyebrow">{e(b["eyebrow"])}</span>
<h2>{b["title"]}</h2>{lead}</div>{grid}{chips}{note}</div></section>'''


ANALYTICS_JS = r"""<script>(function(){try{var q=location.search;if(/[?&]moi\b/.test(q))localStorage.setItem('fyce_moi','1');if(/[?&]pasmoi\b/.test(q))localStorage.removeItem('fyce_moi');if(localStorage.getItem('fyce_moi')==='1')return}catch(e){}
var s=document.createElement('script');s.defer=true;s.src='https://static.cloudflareinsights.com/beacon.min.js';s.setAttribute('data-cf-beacon','{"token": "d97afe693f1b460f8a964b23ec19fe6d"}');document.head.appendChild(s)})()</script>"""

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


def build(d):
    t = d["theme"]
    css = CSS % {**t, "heroem": t.get("heroem", "#f0d9b5")}
    h = d["hero"]
    nav = "".join(f'<a href="#{i}">{e(l)}</a>' for i, l in d["nav"])
    figs = "".join(f'<div class="fig rv"><b>{b}</b><span>{e(l)}</span></div>' for b, l in d.get("figures", []))
    blocks = []
    for blk in d["sections"]:
        kind = blk["kind"]
        blocks.append({"story": section_story, "quote": section_quote, "features": section_features,
                       "cards": section_cards, "menu": section_menu, "gallery": section_gallery,
                       "banner": section_banner, "visit": section_visit, "booking": section_booking, "team": section_team, "resaform": section_resaform, "timeline": section_timeline, "blocks": section_blocks}[kind](blk))
    f = d["footer"]
    fcontact = "".join(f"<li>{c}</li>" for c in f["contact"])
    fnav = "".join(f'<li><a href="#{i}">{e(l)}</a></li>' for i, l in d["nav"])
    legal = f'<span>{e(f["legal"])}</span>' if f.get("legal") else ""
    lbhtml = LB if any(b["kind"] == "gallery" for b in d["sections"]) else ""
    an = d.get("announce")
    annhtml = ""
    if an:
        acta = ""
        if an.get("cta"):
            tgt = ' target="_blank" rel="noopener"' if an["cta"][1].startswith("http") else ""
            acta = f'<a class="btn solid" href="{attr(an["cta"][1])}"{tgt}>{e(an["cta"][0])}</a>'
        annhtml = f'''<div class="ann" id="ann" role="dialog" aria-modal="true" aria-labelledby="ann-t" hidden><div>
<button class="x" aria-label="Fermer">×</button><span class="eyebrow">{e(an.get("eyebrow", "Actualité"))}</span>
<h3 id="ann-t">{e(an["title"])}</h3><p>{e(an["text"])}</p>{acta}</div></div>
<script>(()=>{{const A=document.getElementById('ann');let seen=false;try{{seen=sessionStorage.getItem('ann')==='1'}}catch(e){{}}
const close=()=>{{A.hidden=true;try{{sessionStorage.setItem('ann','1')}}catch(e){{}}}};
if(!seen)setTimeout(()=>A.hidden=false,1200);A.querySelector('.x').onclick=close;A.onclick=e=>{{if(e.target===A)close()}};
A.querySelectorAll('a').forEach(a=>a.addEventListener('click',close));addEventListener('keydown',e=>{{if(e.key==='Escape'&&!A.hidden)close()}});}})();</script>'''
    lg = d.get("logo")
    _c = (["haslogo"] if lg else []) + (["many"] if len(d.get("nav", [])) > 6 else [])
    hcls = f' class="{" ".join(_c)}"' if _c else ""
    if lg and lg.get("bg"):
        hcls += f' style="background:{attr(lg["bg"])}"' 
    if lg:
        fb = 'onerror="this.parentElement.textContent=this.alt"'
        hlogo = f'<a href="#accueil" class="logo"><img src="{attr(lg["src"])}" alt="{attr(d["brand"])}" style="height:{lg.get("height", 44)}px" referrerpolicy="no-referrer" {fb}></a>'
        flogo = f'<div class="flogo"{" style=\"background:" + attr(lg["bg"]) + "\"" if lg.get("bg") else ""}><img src="{attr(lg["src"])}" alt="{attr(d["brand"])}" style="height:{lg.get("height", 44)}px" referrerpolicy="no-referrer" {fb}></div>'
    else:
        hlogo = f'<a href="#accueil" class="logo">{e(d["brand"])}<small>{e(d["tagline"])}</small></a>'
        flogo = f'<div class="logo">{e(d["brand"])}<small>{e(d["tagline"])}</small></div>' 
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>{e(d["title"])}</title>
<meta name="description" content="{attr(d["description"])}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{attr(t["fonts"])}" rel="stylesheet">
<style>{css}</style>
</head>
<body{(' data-logo="'+attr(d["logo"]["src"])+'"') if d.get("logo") else ""}>
<header{hcls}><div class="wrap nav">{hlogo}
<nav class="links">{nav}</nav>
<button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span></button></div></header>
<section class="hero" id="accueil" style="{("background-image:url('" + attr(h["img"]) + "')") if h.get("img") else "background:var(--ink)"}">{f'<video class="hv" autoplay muted loop playsinline poster="{attr(h["img"])}"><source src="{attr(h["video"])}" type="video/mp4"></video>' if h.get("video") else ""}<div class="wrap">
<span class="eyebrow">{e(h["eyebrow"])}</span><h1>{h["title"]}</h1><p>{e(h["lead"])}</p>
<div class="ctas"><a href="{attr(h["cta1"][1])}" class="btn solid">{e(h["cta1"][0])}</a><a href="{attr(h["cta2"][1])}" class="btn ghost">{e(h["cta2"][0])}</a></div></div></section>
{f'<div class="figures"><div class="wrap">{figs}</div></div>' if figs else ""}
{"".join(blocks)}
<footer><div class="wrap"><div class="top"><div>{flogo}
<p style="margin-top:18px;max-width:340px;opacity:.75">{e(f["about"])}</p></div>
<div><h4>Explorer</h4><ul>{fnav}</ul></div><div><h4>Contact</h4><ul>{fcontact}</ul></div></div>
<div class="bottom"><span>© {e(d["brand"])} · Mentions légales · Confidentialité</span>{legal}</div></div></footer>
{lbhtml}{annhtml}<div class="fyce" role="note"><span><b>Proposition de maquette</b> réalisée par <a href="{FYCE["site"]}" target="_blank" rel="noopener">{FYCE["brand"]}</a> · {FYCE["name"]} · <a href="tel:{FYCE["tel"]}">{FYCE["phone"]}</a></span>
<button aria-label="Masquer" onclick="this.parentElement.remove()">×</button></div>
<script>{JS}</script>
{LOGO_JS if (d.get("logo") and d["theme"].get("logo_accent", True)) else ""}
{ANALYTICS_JS}
</body>
</html>'''


if __name__ == "__main__":
    for p in sys.argv[1:]:
        d = json.load(open(p, encoding="utf-8"))
        out = ROOT / d["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        if d.get("style"):
            import importlib
            sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
            mod = importlib.import_module("styles." + d["style"])
            out.write_text(mod.render(d), encoding="utf-8")
        else:
            out.write_text(build(d), encoding="utf-8")
        print("écrit", out.relative_to(ROOT))
