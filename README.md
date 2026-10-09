# Maquettes Fyce

- `site/` : le dossier publié (Cloudflare Pages : répertoire de sortie `site`, aucune commande de build).
- `_generateur/` : générateur privé. `python3 _generateur/build.py _generateur/sites/<prospect>.json` écrit `site/<slug>/index.html`.

Toutes les maquettes sont non indexées (balise meta, `robots.txt`, `_headers` / `.htaccess`).
