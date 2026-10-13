#!/usr/bin/env python3
"""Générateur de maquettes Fyce.

Usage : python3 build.py sites/<prospect>.json [...]
Chaque fichier JSON décrit le contenu d'un prospect ; la page est écrite dans
../<slug>/index.html (dossier publié par Hostinger). Les maquettes sont toujours
non indexées et portent le bandeau « Proposition de maquette — Fyce ».
"""
import json, sys, html, pathlib, urllib.parse, re

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
section{padding:clamp(56px,7vw,92px) 0}
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
.vimg{display:block;width:100%%;aspect-ratio:16/9;object-fit:cover;margin:0 0 22px}header.many .links{gap:18px;font-size:.7rem;letter-spacing:.1em}.hero.phead{min-height:36vh}.hero.phead h1{font-size:clamp(2.2rem,5vw,3.6rem)}.links a[aria-current]{border-bottom:1px solid currentColor}.teamhero{width:100%%;aspect-ratio:16/7;object-fit:cover;margin-bottom:clamp(40px,6vw,70px);background:var(--paper-2)}
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
.menu li span{font-family:var(--serif);font-size:1.18rem}.menu li .ds{display:block;font-family:var(--sans);font-style:normal;font-size:.86rem;color:var(--muted);margin-top:3px;line-height:1.5}.menu li small{color:var(--muted);font-size:.8rem;white-space:nowrap}.menu li small:not(:empty){max-width:60%%}.menu li small{white-space:normal;text-align:right}@media(min-width:861px){.menu li small{white-space:nowrap;max-width:none}}.menu li span{min-width:0}
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


def _headimg(x, cls="teamhero"):
    """Grande photo d'en-tête facultative (bandeau de la page d'origine) : champ "img" de la section."""
    return f'<img class="{cls}" src="{attr(x["img"])}" alt="{attr(x.get("alt", ""))}" loading="lazy" referrerpolicy="no-referrer">' if x.get("img") else ""


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
    return f'''<section id="{s["id"]}"><div class="wrap split{" flip" if s.get("_flip") else ""}">
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
    return f'''<section id="{o["id"]}"><div class="wrap">{_headimg(o)}<div class="head rv"><span class="eyebrow">{e(o["eyebrow"])}</span>
<h2>{o["title"]}</h2><p>{e(o.get("lead", ""))}</p></div>{tabs}
<div class="grid">{"".join(cards)}</div>{note}</div></section>'''


def section_menu(o):
    cols = ""
    for sec in o["sections"]:
        lis = "".join(f'<li><span>{e(i[0])}{("<em class=" + chr(34) + "ds" + chr(34) + ">" + e(i[2]) + "</em>") if len(i) > 2 and i[2] else ""}</span><small>{e(i[1]) if len(i) > 1 else ""}</small></li>' for i in sec["items"])
        cols += f'<h3>{e(sec["title"])}</h3><ul>{lis}</ul>'
    pdfv = f'<div class="pdfview rv"><object data="{attr(o["pdf"])}" type="application/pdf" aria-label="Carte en PDF"><p class="note"><a href="{attr(o["pdf"])}" target="_blank" rel="noopener">Ouvrir la carte en PDF</a></p></object></div>' if o.get("pdf") and o.get("pdf_embed") else ""
    pdfl = f'<p class="note" style="text-align:left"><a href="{attr(o["pdf"])}" target="_blank" rel="noopener" style="border-bottom:1px solid var(--gold)">Télécharger la carte (PDF)</a></p>' if o.get("pdf") else ""
    a = o.get("aside")
    if not a:
        note = f'<p class="note" style="text-align:left">{e(o["note"])}</p>' if o.get("note") else ""
        return f'''<section id="{o["id"]}"><div class="wrap">{_headimg(o)}<div class="head rv"><span class="eyebrow">{e(o["eyebrow"])}</span>
<h2>{o["title"]}</h2><p>{e(o.get("lead", ""))}</p></div><div class="menu solo"><div class="col rv">{cols}{note}{pdfl}</div></div>{pdfv}</div></section>'''
    alis = "".join(f'<li><span>{e(i[0])}</span><small>{e(i[1])}</small></li>' for i in a.get("items", []))
    cta = ""
    if a.get("cta"):
        tgt = ' target="_blank" rel="noopener"' if a["cta"][1].startswith("http") else ""
        cta = f'<a class="btn solid" style="margin-top:24px" href="{attr(a["cta"][1])}"{tgt}>{e(a["cta"][0])}</a>'
    note = f'<p class="note" style="text-align:left">{e(o["note"])}</p>' if o.get("note") else ""
    return f'''<section id="{o["id"]}"><div class="wrap">{_headimg(o)}<div class="head rv"><span class="eyebrow">{e(o["eyebrow"])}</span>
<h2>{o["title"]}</h2><p>{e(o.get("lead", ""))}</p></div>
<div class="menu"><div class="col rv">{cols}{note}{pdfl}</div>
<aside class="rv"><span class="eyebrow">{e(a["eyebrow"])}</span><h3>{e(a["title"])}</h3>
<div class="big">{e(a.get("big", ""))}</div><p>{e(a.get("text", ""))}</p>{('<dl class="courses">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in a["courses"]) + "</dl>") if a.get("courses") else ""}<ul>{alis}</ul>{cta}</aside></div>{pdfv}</div></section>'''


def section_booking(b):
    """Module de réservation existant du client (TheFork, Zenchef…), intégré tel quel dans la page."""
    h = b.get("height", 640)
    return f'''<section id="{b.get("id", "reserver")}"><div class="wrap"><div class="head rv"><span class="eyebrow">{e(b["eyebrow"])}</span>
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


CAR_CSS = """<style>
.carw{position:relative}
.gallery.car{columns:auto;display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;scrollbar-width:none;padding-bottom:4px}
.gallery.car::-webkit-scrollbar{display:none}
.gallery.car button{flex:0 0 calc((100% - 28px)/3);aspect-ratio:4/3;margin:0;scroll-snap-align:start}
.gallery.car img{height:100%;object-fit:cover}
.carb{position:absolute;top:50%;transform:translateY(-50%);width:46px;height:46px;border-radius:50%;border:0;background:var(--paper);color:var(--ink);font-size:1.7rem;line-height:1;cursor:pointer;box-shadow:0 8px 24px -10px rgba(0,0,0,.45);z-index:2;transition:background .25s,color .25s}
.carb:hover{background:var(--accent);color:#fff}.carb.prev{left:-12px}.carb.next{right:-12px}
@media(max-width:860px){.gallery.car button{flex-basis:calc((100% - 14px)/2)}}
@media(max-width:560px){.gallery.car button{flex-basis:84%}.carb.prev{left:4px}.carb.next{right:4px}}
</style>"""
CAR_JS = r"""<script>document.querySelectorAll('.carw').forEach(W=>{if(W.dataset.ok)return;W.dataset.ok=1;const T=W.querySelector('.car');
const step=()=>{const b=T.querySelector('button');return b?b.getBoundingClientRect().width+14:300};
const go=d=>{const end=T.scrollLeft+T.clientWidth>=T.scrollWidth-4;if(d>0&&end)T.scrollTo({left:0});else if(d<0&&T.scrollLeft<4)T.scrollTo({left:T.scrollWidth});else T.scrollBy({left:d*step()})};
W.querySelector('.prev').onclick=()=>go(-1);W.querySelector('.next').onclick=()=>go(1);
if(!matchMedia('(prefers-reduced-motion:reduce)').matches){let t=setInterval(()=>go(1),3800);const stop=()=>{clearInterval(t);t=null},start=()=>{if(!t)t=setInterval(()=>go(1),3800)};
W.addEventListener('mouseenter',stop);W.addEventListener('mouseleave',start);W.addEventListener('focusin',stop);T.addEventListener('touchstart',stop,{passive:true})}})</script>"""


def section_gallery(g):
    btns = "".join(f'<button data-full="{attr(p["full"])}" aria-label="Agrandir"><img src="{attr(p["thumb"])}" alt="{attr(p.get("alt", ""))}" loading="lazy" referrerpolicy="no-referrer">'
                   + (f'<figcaption>{e(p["caption"])}</figcaption>' if p.get("caption") else "") + '</button>'
                   for p in g["photos"])
    lead = f'<p>{e(g["lead"])}</p>' if g.get("lead") else ""
    return f'''<section id="{g.get("id", "photos")}"><div class="wrap">{_headimg(g)}<div class="head rv"><span class="eyebrow">{e(g["eyebrow"])}</span>
<h2>{g["title"]}</h2>{lead}</div>{('<div class="carw"><div class="gallery car">' + btns + '</div><button type="button" class="carb prev" aria-label="Photos précédentes">&lsaquo;</button><button type="button" class="carb next" aria-label="Photos suivantes">&rsaquo;</button></div>' + CAR_CSS + CAR_JS) if g.get("carousel") else ('<div class="gallery">' + btns + '</div>')}{('<div class="ctas" style="display:flex;justify-content:center;margin-top:34px"><a class="btn" href="' + attr(g["cta"][1]) + '">' + e(g["cta"][0]) + '</a></div>') if g.get("cta") else ""}</div></section>'''


def section_banner(b):
    return f'''<div class="banner" style="background-image:url('{attr(b["img"])}')"><div class="rv"><span class="eyebrow">{e(b["eyebrow"])}</span>
<h2>{b["title"]}</h2><a href="{attr(b["cta"][1])}" class="btn ghost">{e(b["cta"][0])}</a></div></div>'''


BLOG_CSS = """<style>
.blog .bt{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 26px}
.blog .bt button{font:inherit;font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;padding:9px 16px;border:1px solid var(--line);background:none;cursor:pointer;color:inherit}
.blog .bt button[aria-pressed=true]{background:var(--accent);border-color:var(--accent);color:#fff}
.blog .bg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:26px}
.blog article{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);min-width:0}
.blog article[hidden]{display:none}
.blog .th{aspect-ratio:16/10;background:var(--paper-2) center/cover no-repeat}
.blog .bd{padding:18px 20px 22px;display:flex;flex-direction:column;gap:8px;flex:1}
.blog .ct{font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);font-weight:600}
.blog h3{font-size:1.18rem;line-height:1.25}
.blog .bd p{color:var(--muted);font-size:.92rem;margin:0}
.blog .rd{margin-top:auto;padding-top:8px;font-size:.85rem;font-weight:500;border-bottom:1px solid var(--gold);align-self:flex-start}
.blog .more{display:flex;justify-content:center;margin-top:30px;gap:12px;flex-wrap:wrap}
.blog .art-more[hidden]{display:none}
@media(max-width:960px){.blog .bg{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:600px){.blog .bg{grid-template-columns:minmax(0,1fr)}}
</style>"""

BLOG_JS = r"""<script>document.querySelectorAll('.blog').forEach(B=>{const A=[...B.querySelectorAll('article')],N=+B.dataset.step||6;let f='all',n=N;
const M=B.querySelector('.art-more');const draw=()=>{let k=0;A.forEach(a=>{const ok=f==='all'||a.dataset.cat===f;a.hidden=!(ok&&k++<n)});
if(M)M.hidden=A.filter(a=>f==='all'||a.dataset.cat===f).length<=n};
B.querySelectorAll('.bt button').forEach(b=>b.onclick=()=>{f=b.dataset.f;n=N;B.querySelectorAll('.bt button').forEach(x=>x.setAttribute('aria-pressed',x===b));draw()});
if(M)M.onclick=()=>{n+=N;draw()};draw()})</script>"""


def section_blog(o):
    cats = []
    for p in o["posts"]:
        if p.get("cat") and p["cat"] not in cats:
            cats.append(p["cat"])
    slug = lambda c: "".join(ch for ch in c.lower() if ch.isalnum())
    tabs = '<button aria-pressed="true" data-f="all">Tous les articles</button>' + "".join(
        f'<button aria-pressed="false" data-f="{slug(c)}">{e(c)}</button>' for c in cats)
    arts = []
    for p in o["posts"]:
        th = f'<div class="th" style="background-image:url(\'{attr(p["img"])}\')" role="img" aria-label=""></div>' if p.get("img") else ""
        date = f' · {e(p["date"])}' if p.get("date") else ""
        if p.get("page"):
            link = f'<a class="rd" href="{attr(p["page"])}/">Lire l\'article</a>'
        else:
            link = f'<a class="rd" href="{attr(p["url"])}" target="_blank" rel="noopener">Lire l\'article</a>' if p.get("url") else ""
        arts.append(f'<article data-cat="{slug(p.get("cat", ""))}">{th}<div class="bd"><span class="ct">{e(p.get("cat", ""))}{date}</span>'
                    f'<h3>{e(p["title"])}</h3><p>{e(p.get("desc", ""))}</p>{link}</div></article>')
    allb = f'<a class="btn" href="{attr(o["all"][1])}" target="_blank" rel="noopener">{e(o["all"][0])}</a>' if o.get("all") else ""
    note = f'<p class="note" style="margin-top:18px;text-align:center">{o["note"]}</p>' if o.get("note") else ""
    return f'''<section id="{o.get("id", "blog")}"><div class="wrap blog" data-step="{o.get("step", 6)}"><div class="head rv"><span class="eyebrow">{e(o["eyebrow"])}</span>
<h2>{o["title"]}</h2><p>{e(o.get("lead", ""))}</p></div><div class="bt" role="group" aria-label="Filtrer par thème">{tabs}</div>
<div class="bg">{"".join(arts)}</div><div class="more"><button type="button" class="btn ghost art-more" style="color:var(--ink)">Voir plus d'articles</button>{allb}</div>{note}</div></section>''' + BLOG_CSS + BLOG_JS


ART_CSS = """<style>
.art{max-width:760px;margin:0 auto}.art .meta{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:600}
.art .chapo{font-size:1.2rem;line-height:1.6;margin:18px 0 26px;color:var(--ink)}
.art .cover{width:100%;aspect-ratio:16/9;object-fit:cover;margin:0 0 30px;background:var(--paper-2)}
.art .keys{background:var(--paper-2);border-left:3px solid var(--accent);padding:20px 24px;margin:0 0 34px}.art .keys h2{font-size:1.15rem;margin:0 0 8px}
.art h2{font-size:clamp(1.5rem,3vw,1.9rem);margin:40px 0 14px}.art p{margin:0 0 14px}.art ul{margin:0 0 18px 20px}.art li{margin-bottom:8px}
.art table{width:100%;border-collapse:collapse;margin:8px 0 22px;font-size:.94rem}.art th,.art td{border-bottom:1px solid var(--line);padding:10px 8px;text-align:left;vertical-align:top}.art th{font-weight:600;background:var(--paper-2)}
.art .tw{overflow-x:auto}.art details{border-bottom:1px solid var(--line);padding:12px 0}.art summary{cursor:pointer;font-weight:500}.art details p{margin:10px 0 0;color:var(--muted)}
.art .back{display:inline-block;margin-top:34px;border-bottom:1px solid var(--gold)}.art .src{font-size:.85rem;color:var(--muted);margin-top:24px}
</style>"""


def section_article(a):
    """Article de blog complet (page d'article) : meta, chapô, image, encadré « à retenir », corps (h2, p, ul, table), FAQ."""
    out = []
    for b in a.get("body", []):
        if "h2" in b:
            out.append(f"<h2>{e(b['h2'])}</h2>")
        if "p" in b:
            out.append(f"<p>{e(b['p'])}</p>")
        if "ul" in b:
            out.append("<ul>" + "".join(f"<li><b>{e(x[0])}</b> {e(x[1])}</li>" if isinstance(x, list) else f"<li>{e(x)}</li>" for x in b["ul"]) + "</ul>")
        if "table" in b:
            t = b["table"]
            out.append('<div class="tw"><table><thead><tr>' + "".join(f"<th>{e(h)}</th>" for h in t["head"]) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in t["rows"]) + "</tbody></table></div>")
    faq = ""
    if a.get("faq"):
        faq = "<h2>Questions fréquentes</h2>" + "".join(f"<details><summary>{e(q)}</summary><p>{e(r)}</p></details>" for q, r in a["faq"])
    keys = f'<div class="keys"><h2>Ce qu\'il faut retenir</h2><p>{e(a["keys"])}</p></div>' if a.get("keys") else ""
    cover = f'<img class="cover" src="{attr(a["img"])}" alt="" referrerpolicy="no-referrer">' if a.get("img") else ""
    meta = " · ".join(x for x in (a.get("cat"), a.get("date")) if x)
    src = f'<p class="src">{a["source"]}</p>' if a.get("source") else ""
    back = f'<a class="back" href="{attr(a["back"][1])}">{e(a["back"][0])}</a>' if a.get("back") else ""
    return f'''<section id="{a.get("id", "article")}"><div class="wrap"><article class="art"><span class="meta">{e(meta)}</span>
<p class="chapo">{e(a.get("chapo", ""))}</p>{cover}{keys}{"".join(out)}{faq}{src}{back}</article></div></section>''' + ART_CSS



def section_visit(v):
    rows = "".join(f"<dt>{e(k)}</dt><dd>{val}</dd>" for k, val in v["rows"])
    q = urllib.parse.quote(v.get("map_q", ""))
    cta = v["cta"]
    tgt = ' target="_blank" rel="noopener"' if cta[1].startswith("http") else ""
    return f'''<section id="{v.get("id", "contact")}"><div class="wrap"><div class="visit{"" if v.get("map_q") else " nomap"} rv"><div class="info">{_headimg(v, "vimg")}
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
    return f'''<section id="{b.get("id", "rubriques")}"{cls}{pad}><div class="wrap">{_headimg(b)}<div class="head rv"><span class="eyebrow">{e(b["eyebrow"])}</span>
<h2>{b["title"]}</h2>{lead}</div>{grid}{chips}{note}</div></section>'''


FORM_CSS = """<style>
.cform{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.3fr);gap:clamp(26px,5vw,60px);background:#fff;border:1px solid var(--line);padding:clamp(24px,4vw,52px)}
.cform form{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px}.cform .full{grid-column:1/-1}
.cform label{display:flex;flex-direction:column;gap:6px;font-size:.85rem;color:var(--muted)}
.cform input,.cform select,.cform textarea{font:inherit;color:var(--ink);padding:11px 12px;border:1px solid var(--line);background:var(--paper);width:100%;min-width:0}
.cform .ok{grid-column:1/-1;color:var(--accent);font-weight:500}
@media(max-width:760px){.cform,.cform form{grid-template-columns:minmax(0,1fr)}}
</style>"""

FORM_JS = r"""<script>document.querySelectorAll('.cform form').forEach(F=>F.onsubmit=ev=>{ev.preventDefault();
const L=[...F.querySelectorAll('[name]')].map(x=>{const l=x.closest('label');const t=l?l.firstChild.textContent.trim():x.name;return t+' : '+(x.value||'').trim()}).join('\n');
location.href='mailto:'+F.dataset.to+'?subject='+encodeURIComponent(F.dataset.subject)+'&body='+encodeURIComponent('Bonjour,\n\n'+L+'\n');
const o=F.querySelector('.ok');if(o)o.hidden=false})</script>"""


REV_CSS = """<style>
.rev-top{display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap;margin:-8px 0 30px;color:var(--muted);font-size:.92rem}
.rev-top b{font-family:var(--serif);font-size:2rem;color:var(--ink);font-weight:500}.rev-top .st{color:var(--gold);letter-spacing:2px;font-size:1.1rem}
.rev-top a{border-bottom:1px solid var(--gold)}
.revs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.rev{background:#fff;border:1px solid var(--line);border-radius:12px;padding:24px 24px 20px;display:flex;flex-direction:column;gap:12px;min-width:0;transition:transform .3s,box-shadow .3s}
.rev:hover{transform:translateY(-4px);box-shadow:0 18px 40px -28px rgba(0,0,0,.45)}
.rev .q{font-family:var(--serif);font-size:2.6rem;line-height:.6;color:var(--accent);height:18px}
.rev p{margin:0;font-size:.95rem;line-height:1.6}
.rev .k{font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:600}
.rev .rf{margin-top:auto;padding-top:12px;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:10px;font-size:.82rem;color:var(--muted);background:none}
.rev .rf strong{color:var(--ink);font-weight:600}
@media(max-width:960px){.revs{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:600px){.revs{grid-template-columns:minmax(0,1fr)}}
</style>"""


def section_reviews(r):
    """Avis clients réels, cités mot pour mot avec leur source (jamais inventés)."""
    cards = "".join(
        f'<article class="rev"><span class="q" aria-hidden="true">“</span>{f"<span class=\"k\">{e(x['work'])}</span>" if x.get("work") else ""}<p>{e(x["text"])}</p>'
        f'<div class="rf"><span><strong>{e(x["name"])}</strong>{(" · " + e(x["city"])) if x.get("city") else ""}</span><span>{e(x.get("date", ""))}</span></div></article>'
        for x in r["items"])
    src = r.get("source")
    top = (f'<div class="rev-top"><b>{e(r["score"])}</b><span class="st" aria-hidden="true">★★★★★</span><span>{e(r.get("count", ""))}</span>'
           + (f'<a href="{attr(src[1])}" target="_blank" rel="noopener">{e(src[0])}</a>' if src else "") + '</div>') if r.get("score") else ""
    return f'''<section id="{r.get("id", "avis")}"><div class="wrap"><div class="head rv"><span class="eyebrow">{e(r["eyebrow"])}</span><h2>{r["title"]}</h2></div>{top}
<div class="revs rv">{cards}</div></div></section>''' + REV_CSS


def section_form(f):
    """Formulaire de contact ou de devis reprenant les champs du site d'origine (envoi par e-mail au prospect)."""
    fields = []
    for x in f["fields"]:
        req = " required" if x.get("required") else ""
        lab = e(x["label"]) + (" *" if x.get("required") else "")
        cls = ' class="full"' if x.get("full") or x.get("type") == "textarea" else ""
        n = attr(x.get("name", x["label"]))
        if x.get("type") == "textarea":
            inp = f'<textarea name="{n}" rows="{x.get("rows", 4)}"{req}></textarea>'
        elif x.get("type") == "select":
            inp = f'<select name="{n}"{req}>' + "".join(f"<option>{e(o)}</option>" for o in x["options"]) + "</select>"
        else:
            inp = f'<input name="{n}" type="{attr(x.get("type", "text"))}"{req}>'
        fields.append(f"<label{cls}>{lab}{inp}</label>")
    side = "".join(f"<p style=\"margin-top:14px\">{p}</p>" for p in f.get("side", []))
    return f'''<section id="{f.get("id", "devis")}"><div class="wrap"><div class="cform rv"><div>
<span class="eyebrow">{e(f["eyebrow"])}</span><h2 style="margin:14px 0 16px">{f["title"]}</h2><p style="color:var(--muted)">{e(f.get("lead", ""))}</p>{side}</div>
<form data-to="{attr(f["email"])}" data-subject="{attr(f.get("subject", "Demande depuis le site"))}">{"".join(fields)}
<div class="full"><button class="btn solid" type="submit">{e(f.get("submit", "Envoyer"))}</button></div><p class="ok" hidden>Merci, votre messagerie va s'ouvrir pour envoyer la demande.</p></form>
</div></div></section>''' + FORM_CSS + FORM_JS


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


LOOKS = ["split", "center", "editorial", "framed"]

LOOK_CSS = """<style>
/* ---- Variantes de mise en page (theme.look) : chaque maquette a sa propre allure, toujours sobre ---- */
.flogo{color:var(--ink)}.blk .bi{max-width:none}
section:is(.quote,.dark,.alt,.trust,.contact)+section[style*="padding-top:0"]{padding-top:clamp(56px,7vw,92px)!important}
section:is(:not([class]),[class=""])+section:is(:not([class]),[class=""]):not([style]){padding-top:clamp(16px,2.5vw,32px)}
.nav .logo img{max-height:60px;transition:max-height .3s}header.scrolled .nav .logo img{max-height:52px}
.logo.gen{display:flex;align-items:center;gap:12px}.logo.gen .mono{flex:0 0 auto;width:44px;height:44px;border-radius:50%;display:grid;place-items:center;background:var(--accent);color:#fff;font-family:var(--serif);font-size:1.05rem;letter-spacing:.02em;font-weight:500}
.logo.gen .nm{display:flex;flex-direction:column;line-height:1.05}.logo.gen small{margin-top:4px}
footer .logo.gen .mono{background:var(--gold);color:var(--ink)}
.split.flip>.img{order:2}@media(max-width:860px){.split.flip>.img{order:0}}
.gallery button img,.card .bimg,.blocks .bi{transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.gallery button:hover img,.blocks article:hover .bi{transform:scale(1.04)}
@media(min-width:1024px) and (prefers-reduced-motion:no-preference){.banner{background-attachment:fixed}}
header{transition:background .35s,box-shadow .35s,color .35s,padding .3s}header.scrolled .nav{height:66px}
.nav{transition:height .3s}
.btn{transition:background .25s,color .25s,transform .25s,box-shadow .25s}.btn:hover{transform:translateY(-2px)}

/* split : texte sur fond clair à gauche, photo à droite */
.look-split .hero{background-color:var(--paper)!important;background-size:0 0!important;color:var(--ink);min-height:88svh;place-items:center start}
.look-split .hero::before{content:"";position:absolute;inset:96px 0 40px 52%;background:inherit;background-size:cover!important;background-position:center!important;border-radius:18px 0 0 18px;z-index:0}
.look-split .hero .wrap{padding:120px 24px 60px;max-width:var(--max)}.look-split .hero .wrap>*{max-width:46%}
.look-split .hero .eyebrow,.look-split .hero h1,.look-split .hero p{color:var(--ink);text-shadow:none}.look-split .hero .eyebrow{color:var(--accent)}
.look-split .hero h1{font-size:clamp(2.6rem,6vw,5rem)}.look-split .hero h1 em{color:var(--accent)}
.look-split .hero .btn.ghost{color:var(--ink);border-color:var(--ink)}
.look-split header:not(.open){background:color-mix(in srgb,var(--paper) 94%,transparent);color:var(--ink);backdrop-filter:blur(8px)}
.look-split .hero.phead::before{inset:0;border-radius:0;opacity:.18}
@media(max-width:860px){.look-split .hero::before{inset:auto 0 0 0;height:38%;border-radius:0}.look-split .hero .wrap>*{max-width:100%}.look-split .hero .wrap{padding:110px 20px 46vh}}
.look-split .split .img{border-radius:14px}.look-split .split .img::after{display:none}

/* center : titre centré, sections centrées, cartes arrondies */
.look-center .hero{place-items:center}.look-center .hero .wrap{text-align:center;padding-bottom:0;display:flex;flex-direction:column;align-items:center}
.look-center .hero::before{background:rgba(0,0,0,.5)}.look-center .hero p{margin-left:auto;margin-right:auto}.look-center .hero .ctas{justify-content:center}
.look-center .hero .eyebrow::before{display:none}
.look-center .card,.look-center .blocks article,.look-center .split .img{border-radius:16px;overflow:hidden}
.look-center .card{box-shadow:0 14px 40px -24px rgba(0,0,0,.35);border-color:transparent}
.look-center .split .img::after{display:none}.look-center .btn{border-radius:999px}
.look-center .rv{transform:scale(.97)}.look-center .rv.in{transform:none}

/* editorial : grands titres fins, filets, photos sans cadre */
.look-editorial h2{font-weight:400;letter-spacing:-.02em}.look-editorial .hero h1{font-weight:300;letter-spacing:-.03em}
.look-editorial .hero::before{background:linear-gradient(90deg,rgba(0,0,0,.72) 0%,rgba(0,0,0,.35) 55%,rgba(0,0,0,.1) 100%)}
.look-editorial .hero{place-items:center start}.look-editorial .hero .wrap{padding-bottom:0}
.look-editorial .split .img::after{inset:auto;left:-18px;top:-18px;width:90px;height:90px;border:0;background:var(--accent);opacity:.12}
.look-editorial .feat>div{border-top:2px solid var(--ink);padding-top:22px}
.look-editorial .quote{text-align:left;background:none;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.look-editorial .quote blockquote{margin-left:0;position:relative;padding-left:56px}.look-editorial .quote blockquote::before{content:"“";position:absolute;left:0;top:-.2em;font-size:4em;line-height:1;color:var(--gold)}
.look-editorial .quote p{margin-left:56px}
.look-editorial .rv{transform:translateX(-24px)}.look-editorial .rv.in{transform:none}

/* framed : photo d'accueil encadrée, coins arrondis, boutons ronds */
.look-framed .hero{margin:84px 16px 0;border-radius:24px;min-height:calc(100svh - 100px)}
.look-framed header:not(.open){background:var(--paper);color:var(--ink)}
.look-framed .hero.phead{min-height:34vh}
.look-framed .btn{border-radius:999px}.look-framed .split .img,.look-framed .card,.look-framed .gallery button,.look-framed .blocks article,.look-framed .banner{border-radius:18px;overflow:hidden}
.look-framed .banner{margin:0 16px}.look-framed .split .img::after{display:none}
.look-framed .card:hover{transform:translateY(-4px);box-shadow:0 20px 40px -26px rgba(0,0,0,.4)}.look-framed .card{transition:transform .3s,box-shadow .3s}

/* pop-up âge légal (domaines viticoles) */
.agegate{position:fixed;inset:0;z-index:300;background:color-mix(in srgb,var(--ink) 92%,transparent);display:grid;place-items:center;padding:20px;backdrop-filter:blur(6px)}
.agegate[hidden]{display:none}.agegate>div{background:var(--paper);color:var(--ink);max-width:440px;width:100%;padding:40px 32px;text-align:center;border-radius:6px}
.agegate h2{font-size:1.6rem;margin:14px 0 10px}.agegate p{color:var(--muted);font-size:.95rem}.agegate .ctas{display:flex;gap:12px;justify-content:center;margin-top:24px;flex-wrap:wrap}
.agegate .no-msg{margin-top:16px;color:var(--accent);font-size:.9rem}
/* formule de menu lisible */
.menu aside dl.courses{margin:14px 0 6px;text-align:left}.menu aside dl.courses div{padding:10px 0;border-top:1px solid rgba(255,255,255,.18)}
.menu aside dl.courses dt{font-size:.68rem;letter-spacing:.18em;text-transform:uppercase;opacity:.75;margin-bottom:4px}.menu aside dl.courses dd{font-size:.95rem;line-height:1.45}
.pdfview{margin-top:40px}.pdfview object{width:100%;height:80vh;border:1px solid var(--line);border-radius:6px;background:#fff}
</style>"""

LOOK_JS = r"""<script>(function(){const R=matchMedia('(prefers-reduced-motion:reduce)').matches;
document.querySelectorAll('.fig b').forEach(b=>{const m=b.innerHTML.match(/^(\d[\d\s]*)(.*)$/s);if(!m||R)return;const n=parseInt(m[1].replace(/\s/g,''),10);if(!n||n>100000)return;
const tail=m[2];const io=new IntersectionObserver(es=>{if(!es[0].isIntersecting)return;io.disconnect();const t0=performance.now(),d=1200;
const step=t=>{const k=Math.min(1,(t-t0)/d),v=Math.round(n*(1-Math.pow(1-k,3)));b.innerHTML=v.toLocaleString('fr-FR')+tail;if(k<1)requestAnimationFrame(step)};requestAnimationFrame(step)},{threshold:.4});io.observe(b)});
const A=document.getElementById('agegate');if(A){let ok=false;try{ok=localStorage.getItem('age_ok')==='1'}catch(e){}
if(!ok){A.hidden=false;document.body.style.overflow='hidden';A.querySelector('.yes').focus()}
A.querySelector('.yes').onclick=()=>{try{localStorage.setItem('age_ok','1')}catch(e){}A.hidden=true;document.body.style.overflow=''};
A.querySelector('.no').onclick=()=>{A.querySelector('.no-msg').hidden=false}}})()</script>"""


def agegate_html(d):
    if not d.get("agegate"):
        return ""
    return f'''<div class="agegate" id="agegate" role="dialog" aria-modal="true" aria-labelledby="ag-t" hidden><div>
<span class="eyebrow">{e(d["brand"])}</span><h2 id="ag-t">Avez-vous 18 ans ou plus ?</h2>
<p>L'accès à ce site est réservé aux personnes ayant l'âge légal pour consommer de l'alcool.</p>
<div class="ctas"><button class="btn solid yes" type="button">Oui, entrer</button><button class="btn ghost no" type="button" style="color:var(--ink);border-color:var(--ink)">Non</button></div>
<p class="no-msg" hidden>Désolé, vous devez avoir 18 ans pour accéder à ce site. L'abus d'alcool est dangereux pour la santé.</p></div></div>'''


def initials(name):
    stop = {"le", "la", "les", "de", "du", "des", "d", "l", "et", "&", "sarl", "selarl", "sas", "eurl", "entreprise", "domaine", "cabinet", "etude", "étude"}
    words = [w for w in re.split(r"[\s'’\-]+", name) if w and w.lower() not in stop]
    if not words:
        words = name.split()
    return ("".join(w[0] for w in words[:2])).upper()


def pick_look(d):
    t = d.get("theme", {})
    if t.get("look") in LOOKS:
        return t["look"]
    h = sum(ord(c) for c in d.get("slug", "x"))
    return LOOKS[h % len(LOOKS)]


def _navitems(d, page, prefix=""):
    """Liens du menu. Site multi-pages : Accueil + une entrée par page visible (+ ancres de l'accueil listées dans nav_extra).
    Sans page visible : les ancres de nav, préfixées vers l'accueil depuis une sous-page."""
    pref = prefix if page else ""
    visible = [pg for pg in d.get("pages", []) if not pg.get("hidden")]
    if not visible:
        return [(pref + "#" + i, l, "") for i, l in d["nav"]]
    items = [(pref or "./", d.get("home_label", "Accueil"), "" if page else ' aria-current="page"')]
    for pg in visible:
        cur = ' aria-current="page"' if page and page["slug"] == pg["slug"] else ""
        items.append((pref + pg["slug"] + "/", pg.get("label", pg["title"]), cur))
    for x in d.get("nav_extra", []):
        i, l = x[0], x[1]
        it = (pref + "#" + i, l, "")
        if len(x) > 2:            # 3e élément : position dans le menu (0 = avant Accueil)
            items.insert(int(x[2]), it)
        else:
            items.append(it)
    return items


PBOX_CSS = """<style>
.pbox{padding:clamp(120px,13vw,160px) 0 clamp(36px,5vw,64px);background:var(--paper-2)}
.pbox-g{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:clamp(28px,5vw,64px);align-items:center}
.pbox h1{font-size:clamp(2.2rem,5vw,3.6rem);margin:14px 0 14px}.pbox p{color:var(--muted);max-width:52ch}
.pbox figure{margin:0;justify-self:end;width:100%;max-width:500px;overflow:hidden;border-radius:14px;box-shadow:0 24px 50px -30px rgba(0,0,0,.45)}
.pbox figure img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}.pbox figure:hover img{transform:scale(1.03)}
.pplain{position:relative;overflow:hidden;padding-bottom:clamp(48px,6vw,80px)}.pplain .wrap{position:relative;z-index:1}
.pplain h1{font-size:clamp(2.6rem,6vw,4.4rem)}.prule{display:block;width:72px;height:2px;background:var(--gold);margin:4px 0 20px}
.pmono{position:absolute;right:max(4vw,calc((100vw - var(--max))/2));top:50%;transform:translateY(-38%);font-family:var(--serif);font-size:clamp(9rem,22vw,19rem);line-height:1;color:var(--accent);opacity:.08;letter-spacing:-.04em;pointer-events:none;animation:pm-in 1.4s cubic-bezier(.2,.7,.2,1) both}
@keyframes pm-in{from{opacity:0;transform:translateY(-30%)}to{opacity:.08;transform:translateY(-38%)}}
@media(prefers-reduced-motion:reduce){.pmono{animation:none}}
@media(max-width:820px){.pbox-g{grid-template-columns:minmax(0,1fr)}.pbox figure{justify-self:stretch;max-width:none}}
</style>"""


def _pagehead(pg, d=None):
    img = pg.get("img")
    if (pg.get("head") or (d or {}).get("phead")) == "plain":   # en-tête sobre sans photo : titre, filet doré, grand monogramme
        eb = f'<span class="eyebrow">{e(pg["eyebrow"])}</span>' if pg.get("eyebrow") else ""
        lead = f'<p>{e(pg["lead"])}</p>' if pg.get("lead") else ""
        mono = e((d or {}).get("monogram") or initials((d or {}).get("brand", "")))
        return f'''<section class="phead pbox pplain" id="accueil"><div class="wrap"><div class="rv in">{eb}<h1>{pg.get("h1", pg["title"])}</h1><i class="prule"></i>{lead}</div></div><span class="pmono" aria-hidden="true">{mono}</span></section>''' + PBOX_CSS
    if img and (pg.get("head") or (d or {}).get("phead")) == "box":   # photo d'en-tête petite : cadre net à côté du titre, pas étirée plein écran
        eb = f'<span class="eyebrow">{e(pg["eyebrow"])}</span>' if pg.get("eyebrow") else ""
        lead = f'<p>{e(pg["lead"])}</p>' if pg.get("lead") else ""
        return f'''<section class="phead pbox" id="accueil"><div class="wrap pbox-g"><div class="rv in">{eb}<h1>{pg.get("h1", pg["title"])}</h1>{lead}</div>
<figure><img src="{attr(img)}" alt="" referrerpolicy="no-referrer" style="object-position:{attr(pg.get("img_pos", "center"))}"></figure></div></section>''' + PBOX_CSS
    style = f"background-image:url('{attr(img)}')" if img else "background:var(--ink)"
    eb = f'<span class="eyebrow">{e(pg["eyebrow"])}</span>' if pg.get("eyebrow") else ""
    lead = f'<p>{e(pg["lead"])}</p>' if pg.get("lead") else ""
    return f'''<section class="hero phead" id="accueil" style="{style}"><div class="wrap">{eb}<h1>{pg.get("h1", pg["title"])}</h1>{lead}</div></section>'''


def _fixlinks(html, page, prefix, idmap, firsts=()):
    """Réécrit les liens internes #ancre vers la bonne page quand l'ancre est ailleurs."""
    if not idmap:
        return html
    cur = page["slug"] if page else ""
    def rw(m):
        anchor = m.group(1)
        where = idmap.get(anchor)
        if anchor in firsts and where:   # 1re section d'une page : on arrive en haut de la page, pas au milieu
            return 'href="' + ("./" if where == cur else prefix + where + "/") + '"'
        if where is None or where == cur:
            return m.group(0)
        return 'href="' + prefix + (where + "/" if where else "") + "#" + anchor + '"'
    return re.sub(r'href="#([\w-]+)"', rw, html)


def style_pages(d, full):
    """Styles sur mesure (releve, etabli…) : découpe la page rendue en plusieurs pages.
    d["pages"] = [{slug, label, title, keep: [ids de sections]}], d["home_keep"] = ids gardés sur l'accueil."""
    secs = list(re.finditer(r'<section\b[^>]*>.*?</section>', full, re.S))
    def sid(m):
        x = re.search(r'id="([^"]+)"', m.group(0)[:300])
        return x.group(1) if x else None
    idmap = {}
    for pg in d["pages"]:
        for k in pg["keep"]:
            idmap[k] = pg["slug"]
    def cut(keep, sub):
        out, last = [], 0
        for m in secs:
            out.append(full[last:m.start()])
            if sid(m) in keep:
                out.append(m.group(0))
            last = m.end()
        out.append(full[last:])
        h = "".join(out)
        if sub:   # retire l'en-tête d'accueil (tout ce qui précède la première section dans <main>) et met un titre de page
            mm = re.search(r'(<main\b[^>]*>)(.*?)(?=<section\b)', h, re.S)
            title = f'<section class="phead" style="padding:clamp(48px,8vw,90px) 0 10px"><div class="w"><h1 style="font-size:.85rem;letter-spacing:.2em;text-transform:uppercase;opacity:.75;margin:0">{e(sub["title"])}</h1></div></section>'
            if mm:
                h = h[:mm.start()] + mm.group(1) + title + h[mm.end():]
            h = h.replace("<title>", f"<title>{e(sub['title'])} | ", 1).replace(f"<title>{e(sub['title'])} | " + e(d["title"]), f"<title>{e(sub['title'])} | {e(d['brand'])}", 1)
        return h
    firsts = {pg["keep"][0] for pg in d["pages"] if pg.get("keep")}
    pages = {"": _fixlinks(cut(set(d.get("home_keep", [])) | {"accueil"}, None), None, "", idmap, firsts)}
    for pg in d["pages"]:
        pref = "../" * (pg["slug"].count("/") + 1)
        h = cut(set(pg["keep"]), pg)
        h = h.replace('href="#accueil"', f'href="{pref}"')
        pages[pg["slug"]] = _fixlinks(h, pg, pref, {**{k: "" for k in d.get("home_keep", [])}, "accueil": "", **idmap}, firsts)
    return pages


def build_all(d):
    """Rend la page d'accueil et, si le JSON a des "pages", une page par entrée : {slug: html}."""
    idmap = None
    if d.get("pages"):
        idmap = {}
        for blk in d["sections"]:
            if blk.get("id"):
                idmap.setdefault(blk["id"], "")
            if blk["kind"] == "visit":
                idmap.setdefault(blk.get("id", "contact"), "")
        for pg in d["pages"]:
            for blk in pg["sections"]:
                bid = blk.get("id") or ("contact" if blk["kind"] == "visit" else None)
                if bid:
                    idmap.setdefault(bid, pg["slug"])
    out = {"": build(d, None, "", idmap)}
    for pg in d.get("pages", []):
        out[pg["slug"]] = build(d, pg, "../" * (pg["slug"].count("/") + 1), idmap)
    return out


def build(d, page=None, prefix="", idmap=None):
    t = d["theme"]
    css = CSS % {**t, "heroem": t.get("heroem", "#f0d9b5")}
    h = d["hero"]
    sections = page["sections"] if page else d["sections"]
    navitems = _navitems(d, page, prefix)
    nav = "".join(f'<a href="{attr(hr)}"{cur}>{e(l)}</a>' for hr, l, cur in navitems)
    figs = "".join(f'<div class="fig rv"><b>{b}</b><span>{e(l)}</span></div>' for b, l in d.get("figures", []))
    blocks = []
    nstory = 0
    for blk in sections:
        kind = blk["kind"]
        if kind == "story":
            blk = {**blk, "_flip": nstory % 2 == 1}
            nstory += 1
        blocks.append({"story": section_story, "quote": section_quote, "features": section_features,
                       "cards": section_cards, "menu": section_menu, "gallery": section_gallery,
                       "banner": section_banner, "visit": section_visit, "booking": section_booking, "team": section_team, "resaform": section_resaform, "timeline": section_timeline, "blocks": section_blocks, "blog": section_blog, "article": section_article, "form": section_form, "reviews": section_reviews}[kind](blk))
    f = d["footer"]
    fcontact = "".join(f"<li>{c}</li>" for c in f["contact"])
    fnav = "".join(f'<li><a href="{attr(hr)}">{e(l)}</a></li>' for hr, l, cur in navitems)
    legal = f'<span>{e(f["legal"])}</span>' if f.get("legal") else ""
    lbhtml = LB if any(b["kind"] == "gallery" for b in sections) else ""
    an = d.get("announce") if not page else None
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
        _bg = lg["bg"].lstrip("#")
        _dark = len(_bg) == 6 and (0.299 * int(_bg[0:2], 16) + 0.587 * int(_bg[2:4], 16) + 0.114 * int(_bg[4:6], 16)) < 140
        hcls += f' style="background:{attr(lg["bg"])}{";color:#fff" if _dark else ""}"' 
    if lg:
        lg = dict(lg)
        if not re.match(r"^(https?:|/|data:)", lg["src"]):   # logo stocké avec la maquette : chemin relatif à la page
            lg["src"] = (prefix or "") + lg["src"]
        fb = 'onerror="this.parentElement.textContent=this.alt"'
        hlogo = f'<a href="{prefix or './'}" class="logo"{' style="display:flex;align-items:center;gap:12px"' if lg.get("with_name") else ""}><img src="{attr(lg["src"])}" alt="{attr(d["brand"])}" style="height:{lg.get("height", 44)}px" referrerpolicy="no-referrer" {fb}>{e(d["brand"]) if lg.get("with_name") else ""}</a>'
        flogo = f'<div class="flogo"{" style=\"background:" + attr(lg["bg"]) + "\"" if lg.get("bg") else ""}><img src="{attr(lg["src"])}" alt="{attr(d["brand"])}" style="height:{lg.get("height", 44)}px" referrerpolicy="no-referrer" {fb}></div>'
    else:
        ini = e(d.get("monogram") or initials(d["brand"]))
        tg = f'<small>{e(d["tagline"])}</small>' if d.get("tagline") else ""
        hlogo = f'<a href="{prefix or './'}" class="logo gen"><span class="mono" aria-hidden="true">{ini}</span><span class="nm">{e(d["brand"])}{tg}</span></a>'
        flogo = f'<div class="logo gen"><span class="mono" aria-hidden="true">{ini}</span><span class="nm">{e(d["brand"])}{tg}</span></div>'
    HOME_HERO = f'''<section class="hero" id="accueil" style="{("background-image:url('" + attr(h["img"]) + "')") if h.get("img") else "background:var(--ink)"}">{f'<video class="hv" autoplay muted loop playsinline poster="{attr(h["img"])}"><source src="{attr(h["video"])}" type="video/mp4"></video>' if h.get("video") else ""}<div class="wrap">
<span class="eyebrow">{e(h["eyebrow"])}</span><h1>{h["title"]}</h1><p>{e(h["lead"])}</p>
<div class="ctas"><a href="{attr(h["cta1"][1])}" class="btn solid">{e(h["cta1"][0])}</a><a href="{attr(h["cta2"][1])}" class="btn ghost">{e(h["cta2"][0])}</a></div></div></section>
'''
    html = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>{e((page["title"] + " | " + d["brand"]) if page else d["title"])}</title>
<meta name="description" content="{attr(d["description"])}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{attr(t["fonts"])}" rel="stylesheet">
<style>{css}</style>
{LOOK_CSS}
{('<style>' + d['extra_css'] + '</style>') if d.get('extra_css') else ''}
</head>
<body class="look-{pick_look(d)}"{(' data-logo="'+attr(d["logo"]["src"])+'"') if d.get("logo") else ""}>
{agegate_html(d)}
<header{hcls}><div class="wrap nav">{hlogo}
<nav class="links">{nav}</nav>
<button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span></button></div></header>
{_pagehead(page, d) if page else HOME_HERO}
{f'<div class="figures"><div class="wrap">{figs}</div></div>' if figs and not page else ""}
{"".join(blocks)}
<footer><div class="wrap"><div class="top"><div>{flogo}
<p style="margin-top:18px;max-width:340px;opacity:.75">{e(f["about"])}</p></div>
<div><h4>Explorer</h4><ul>{fnav}</ul></div><div><h4>Contact</h4><ul>{fcontact}</ul></div></div>
<div class="bottom"><span>© {e(d["brand"])} · {('<a href="' + attr(f['legal_url']) + '" target="_blank" rel="noopener" style="text-decoration:underline">Mentions légales</a>') if f.get('legal_url') else 'Mentions légales'} · Confidentialité</span>{legal}</div></div></footer>
{lbhtml}{annhtml}<div class="fyce" role="note"><span><b>Proposition de maquette</b> réalisée par <a href="{FYCE["site"]}" target="_blank" rel="noopener">{FYCE["brand"]}</a> · {FYCE["name"]} · <a href="tel:{FYCE["tel"]}">{FYCE["phone"]}</a></span>
<button aria-label="Masquer" onclick="this.parentElement.remove()">×</button></div>
<script>{JS}</script>
{LOGO_JS if (d.get("logo") and d["theme"].get("logo_accent", True)) else ""}
{LOOK_JS}
{ANALYTICS_JS}
</body>
</html>'''
    return _fixlinks(html, page, prefix, idmap)


def _figees():
    """Slugs des maquettes déjà envoyées aux prospects : on n'y touche plus (règle de Philippine)."""
    import csv
    f = pathlib.Path(__file__).resolve().parent / "prospects.csv"
    if not f.exists():
        return set()
    bloq = ("envoye", "a repondu", "relance", "sans suite", "refus")
    return {r.get("slug_maquette", "") for r in csv.DictReader(open(f, encoding="utf-8"))
            if r.get("slug_maquette") and r.get("statut", "").startswith(bloq)}


if __name__ == "__main__":
    force = "--force" in sys.argv
    figees = set() if force else _figees()
    for p in [a for a in sys.argv[1:] if a != "--force"]:
        d = json.load(open(p, encoding="utf-8"))
        if d["slug"] in figees:
            print("ignoré (maquette déjà envoyée, figée) :", d["slug"])
            continue
        out = ROOT / d["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        if d.get("style"):
            import importlib
            sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
            mod = importlib.import_module("styles." + d["style"])
            full = mod.render(d)
            if d.get("pages"):
                for sub, page_html in style_pages(d, full).items():
                    o = out.parent / sub / "index.html" if sub else out
                    o.parent.mkdir(parents=True, exist_ok=True)
                    o.write_text(page_html, encoding="utf-8")
            else:
                out.write_text(full, encoding="utf-8")
        else:
            for sub, page_html in build_all(d).items():
                o = out.parent / sub / "index.html" if sub else out
                o.parent.mkdir(parents=True, exist_ok=True)
                o.write_text(page_html, encoding="utf-8")
        print("écrit", out.relative_to(ROOT))
