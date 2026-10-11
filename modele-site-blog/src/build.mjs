// Générateur du site (Fyce) : lit content/site.json et content/articles/*.md, écrit le site dans dist/.
// Lancé automatiquement par Cloudflare à chaque modification (npm run build).
import { readFileSync, writeFileSync, mkdirSync, readdirSync, existsSync, cpSync, rmSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { marked } from "marked";
import YAML from "yaml";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const DIST = join(ROOT, process.env.OUT_DIR || "dist");
const site = JSON.parse(readFileSync(join(ROOT, "content/site.json"), "utf8"));
const NOINDEX = process.env.NOINDEX === "1";       // pour une démonstration non référencée
const BASE = process.env.BASE_PATH || "";          // si le site est servi dans un sous-dossier (démo)
const ACCENT = site.accent || "#24505e";

const esc = (s = "") => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const url = p => BASE + p;
const abs = p => (site.url || "").replace(/\/$/, "") + p;
const fmtDate = d => new Date(d + "T12:00:00").toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" });
const catSlug = c => (c || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");

// --- Articles ---------------------------------------------------------------
function readArticles() {
  const dir = join(ROOT, "content/articles");
  if (!existsSync(dir)) return [];
  return readdirSync(dir).filter(f => f.endsWith(".md")).map(f => {
    const raw = readFileSync(join(dir, f), "utf8");
    const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
    const data = m ? (YAML.parse(m[1]) || {}) : {};
    const body = m ? m[2] : raw;
    const slug = f.replace(/\.md$/, "").replace(/^\d{4}-\d{2}-\d{2}-/, "");
    const date = data.date instanceof Date ? data.date.toISOString().slice(0, 10) : String(data.date || "").slice(0, 10);
    return { ...data, date, slug, html: marked.parse(body) };
  }).filter(a => a.title && !a.draft).sort((a, b) => (b.date || "").localeCompare(a.date || ""));
}

// --- Gabarit commun -----------------------------------------------------------
const CSS = `:root{--accent:${ACCENT};--ink:#1d2226;--muted:#5d666d;--paper:#f6f5f1;--line:rgba(0,0,0,.12)}
*{box-sizing:border-box;margin:0;padding:0}body{background:var(--paper);color:var(--ink);font:300 1.04rem/1.7 "Inter",system-ui,sans-serif}
a{color:inherit}img{max-width:100%;display:block}.w{max-width:1120px;margin:0 auto;padding:0 20px}
h1,h2,h3{font-family:"Fraunces",Georgia,serif;font-weight:500;line-height:1.15}
header{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}
header .w{display:flex;align-items:center;justify-content:space-between;gap:20px;min-height:72px;flex-wrap:wrap}
.logo{font-family:"Fraunces",Georgia,serif;font-size:1.35rem;text-decoration:none}.logo img{height:46px;width:auto}
nav{display:flex;gap:22px;flex-wrap:wrap;font-size:.82rem;letter-spacing:.1em;text-transform:uppercase}nav a{text-decoration:none;padding:6px 0}nav a[aria-current]{border-bottom:2px solid var(--accent)}
.hero{background:var(--ink) center/cover no-repeat;color:#fff;padding:clamp(80px,14vw,160px) 0}.hero h1{font-size:clamp(2.2rem,6vw,4rem);max-width:780px}.hero p{max-width:620px;margin-top:16px;opacity:.9}
.hero.small{padding:clamp(56px,9vw,100px) 0}
section{padding:clamp(56px,8vw,96px) 0}.eyebrow{font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);font-weight:600}
h2.t{font-size:clamp(1.8rem,4vw,2.6rem);margin:10px 0 26px}
.btn{display:inline-block;background:var(--accent);color:#fff;text-decoration:none;padding:13px 24px;font-size:.82rem;letter-spacing:.12em;text-transform:uppercase;font-weight:500;border:0;cursor:pointer}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
.card{background:#fff;border:1px solid var(--line);display:flex;flex-direction:column;text-decoration:none}.card[hidden]{display:none}
.card .th{aspect-ratio:16/10;background:#e6e8e6 center/cover}.card .bd{padding:18px 20px 22px;display:flex;flex-direction:column;gap:8px;flex:1}
.card .ct{font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:600}.card h3{font-size:1.2rem}.card p{color:var(--muted);font-size:.93rem}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:24px}.filters button{font:inherit;font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;padding:8px 14px;border:1px solid var(--line);background:#fff;cursor:pointer}
.filters button[aria-pressed=true]{background:var(--accent);border-color:var(--accent);color:#fff}
.art{max-width:760px;margin:0 auto}.art .meta{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:600}
.art .cover{width:100%;aspect-ratio:16/9;object-fit:cover;margin:22px 0 28px}.art h2{font-size:1.7rem;margin:34px 0 12px}.art h3{font-size:1.3rem;margin:26px 0 10px}
.art p,.art ul,.art ol{margin:0 0 14px}.art ul,.art ol{padding-left:22px}.art a{color:var(--accent)}.art img{margin:18px 0}.art blockquote{border-left:3px solid var(--accent);padding-left:16px;color:var(--muted)}
.art table{width:100%;border-collapse:collapse;margin:10px 0 20px}.art th,.art td{border-bottom:1px solid var(--line);padding:9px 8px;text-align:left}
.pn{display:flex;justify-content:space-between;gap:16px;margin-top:40px;border-top:1px solid var(--line);padding-top:20px;font-size:.92rem}
.contact{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:30px}.contact dl div{padding:10px 0;border-bottom:1px solid var(--line)}.contact dt{font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
footer{background:var(--ink);color:#fff;padding:40px 0;font-size:.88rem}footer .w{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;opacity:.85}
@media(max-width:900px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:620px){.grid,.contact{grid-template-columns:minmax(0,1fr)}}`;

function page({ path, title, description, body, image, jsonld }) {
  const navHtml = (site.nav || []).map(([l, h]) => `<a href="${esc(url(h))}"${(h === path || (h !== "/" && path.startsWith(h) && !h.includes("#"))) ? ' aria-current="page"' : ""}>${esc(l)}</a>`).join("");
  const logo = site.logo ? `<img src="${esc(url(site.logo))}" alt="${esc(site.name)}">` : esc(site.name);
  return `<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title><meta name="description" content="${esc(description || site.tagline || "")}">
${NOINDEX ? '<meta name="robots" content="noindex, nofollow">' : `<link rel="canonical" href="${esc(abs(path))}">`}
<meta property="og:title" content="${esc(title)}"><meta property="og:description" content="${esc(description || "")}">${image ? `<meta property="og:image" content="${esc(abs(image))}">` : ""}
<link rel="alternate" type="application/rss+xml" title="${esc(site.name)}" href="${esc(url("/rss.xml"))}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>${CSS}</style>${jsonld ? `<script type="application/ld+json">${JSON.stringify(jsonld)}</script>` : ""}
</head><body>
<header><div class="w"><a class="logo" href="${esc(url("/"))}">${logo}</a><nav>${navHtml}</nav></div></header>
<main>${body}</main>
<footer><div class="w"><span>© ${new Date().getFullYear()} ${esc(site.name)}</span><span>${esc(site.address || "")}</span></div></footer>
</body></html>`;
}

const card = a => `<a class="card" href="${esc(url(`/blog/${a.slug}/`))}" data-cat="${esc(catSlug(a.category))}">
<div class="th"${a.image ? ` style="background-image:url('${esc(url(a.image))}')"` : ""}></div>
<div class="bd"><span class="ct">${esc(a.category || "")}${a.date ? " · " + esc(fmtDate(a.date)) : ""}</span><h3>${esc(a.title)}</h3><p>${esc(a.description || "")}</p></div></a>`;

function write(path, html) {
  const out = join(DIST, path.replace(/^\//, ""), path.endsWith(".xml") || path.endsWith(".txt") || path.endsWith(".html") ? "" : "index.html");
  mkdirSync(dirname(out), { recursive: true });
  writeFileSync(out, html);
}

// --- Construction --------------------------------------------------------------
rmSync(DIST, { recursive: true, force: true });
mkdirSync(DIST, { recursive: true });
if (existsSync(join(ROOT, "public"))) cpSync(join(ROOT, "public"), DIST, { recursive: true });
const articles = readArticles();

// Accueil
write("/", page({
  path: "/", title: `${site.name} | ${site.tagline || ""}`, description: site.intro,
  body: `<section class="hero"${site.hero_image ? ` style="background-image:linear-gradient(rgba(0,0,0,.45),rgba(0,0,0,.45)),url('${esc(url(site.hero_image))}')"` : ""}><div class="w"><h1>${esc(site.tagline || site.name)}</h1><p>${esc(site.intro || "")}</p></div></section>
<section><div class="w"><span class="eyebrow">Le blog</span><h2 class="t">Nos derniers articles</h2><div class="grid">${articles.slice(0, 3).map(card).join("")}</div>
<p style="margin-top:28px"><a class="btn" href="${esc(url("/blog/"))}">Tous les articles</a></p></div></section>
<section id="contact" style="background:#fff"><div class="w contact"><div><span class="eyebrow">Contact</span><h2 class="t">Parlons de votre projet</h2></div>
<dl>${[["Téléphone", site.phone && `<a href="tel:${esc(site.phone.replace(/\s/g, ""))}">${esc(site.phone)}</a>`], ["E-mail", site.email && `<a href="mailto:${esc(site.email)}">${esc(site.email)}</a>`], ["Adresse", site.address && esc(site.address)], ["Horaires", site.hours && esc(site.hours)]].filter(r => r[1]).map(([k, v]) => `<div><dt>${k}</dt><dd>${v}</dd></div>`).join("")}</dl></div></section>`
}));

// Liste des articles, avec filtre par thème
const cats = [...new Set(articles.map(a => a.category).filter(Boolean))];
write("/blog/", page({
  path: "/blog/", title: `Le blog | ${site.name}`, description: `Actualités et conseils de ${site.name}.`,
  body: `<section class="hero small"><div class="w"><h1>Le blog</h1><p>Actualités et conseils de ${esc(site.name)}.</p></div></section>
<section><div class="w"><div class="filters" role="group" aria-label="Filtrer par thème"><button aria-pressed="true" data-f="">Tous</button>${cats.map(c => `<button aria-pressed="false" data-f="${esc(catSlug(c))}">${esc(c)}</button>`).join("")}</div>
<div class="grid">${articles.map(card).join("") || "<p>Aucun article pour l'instant.</p>"}</div></div></section>
<script>document.querySelectorAll('.filters button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.filters button').forEach(x=>x.setAttribute('aria-pressed',x===b));
document.querySelectorAll('.card').forEach(c=>c.hidden=!!b.dataset.f&&c.dataset.cat!==b.dataset.f)})</script>`
}));

// Une page par article
articles.forEach((a, i) => {
  const prev = articles[i + 1], next = articles[i - 1];
  write(`/blog/${a.slug}/`, page({
    path: `/blog/${a.slug}/`, title: `${a.title} | ${site.name}`, description: a.description, image: a.image,
    jsonld: { "@context": "https://schema.org", "@type": "BlogPosting", headline: a.title, datePublished: a.date, description: a.description || "", image: a.image ? abs(a.image) : undefined, author: { "@type": "Organization", name: site.name } },
    body: `<section><div class="w"><article class="art"><span class="meta">${esc(a.category || "")}${a.date ? " · " + esc(fmtDate(a.date)) : ""}</span>
<h1 style="font-size:clamp(2rem,5vw,3rem);margin:10px 0 18px">${esc(a.title)}</h1>${a.image ? `<img class="cover" src="${esc(url(a.image))}" alt="">` : ""}${a.html}
<div class="pn"><span>${prev ? `<a href="${esc(url(`/blog/${prev.slug}/`))}">← ${esc(prev.title)}</a>` : ""}</span><span>${next ? `<a href="${esc(url(`/blog/${next.slug}/`))}">${esc(next.title)} →</a>` : ""}</span></div>
<p style="margin-top:24px"><a href="${esc(url("/blog/"))}">Tous les articles</a></p></article></div></section>`
  }));
});

// Plan du site, flux RSS, robots, page 404
const urls = ["/", "/blog/", ...articles.map(a => `/blog/${a.slug}/`)];
write("/sitemap.xml", `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls.map(u => `<url><loc>${esc(abs(u))}</loc></url>`).join("")}</urlset>`);
write("/rss.xml", `<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>${esc(site.name)}</title><link>${esc(abs("/"))}</link><description>${esc(site.tagline || "")}</description>${articles.map(a => `<item><title>${esc(a.title)}</title><link>${esc(abs(`/blog/${a.slug}/`))}</link><guid>${esc(abs(`/blog/${a.slug}/`))}</guid>${a.date ? `<pubDate>${new Date(a.date + "T12:00:00Z").toUTCString()}</pubDate>` : ""}<description>${esc(a.description || "")}</description></item>`).join("")}</channel></rss>`);
write("/robots.txt", NOINDEX ? "User-agent: *\nDisallow: /\n" : `User-agent: *\nAllow: /\nSitemap: ${abs("/sitemap.xml")}\n`);
write("/404.html", page({ path: "/404", title: `Page introuvable | ${site.name}`, body: `<section><div class="w"><h1>Page introuvable</h1><p style="margin:16px 0 24px">Cette page n'existe pas ou a été déplacée.</p><a class="btn" href="${esc(url("/"))}">Retour à l'accueil</a></div></section>` }));

console.log(`Site construit : ${articles.length} article(s) publié(s), ${urls.length} pages.`);
