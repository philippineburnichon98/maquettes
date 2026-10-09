# Maquettes Fyce

- `site/` : le dossier publié (Cloudflare : répertoire `site`, aucune commande de build).
- `_generateur/` : générateur privé.
  - `python3 _generateur/build.py _generateur/sites/<prospect>.json` écrit `site/<slug>/index.html`.
  - Le champ `"style"` du JSON choisit la mise en page dans `_generateur/styles/` :
    - `chrono` : domaine à forte histoire (pellicule photo, frise, cuvées en étiquettes avec fiche technique). Exemple : domaine-de-la-folie.json
    - `bouchon` : bouchon / brasserie traditionnelle (nappe à carreaux, ardoise, carte imprimée, réservation intégrée, cave, groupes). Exemple : bouchon-des-cordeliers.json
    - `affiche` : lieu au ton audacieux (affiche, bandeau défilant, carte en catalogue, équipe). Exemple : bouchon-des-artistes.json
    - `cellier` : domaine avec beaucoup de cuvées (parole du vigneron, étagères de bouteilles cliquables, achat, points de vente, souvenirs). Exemple : domaine-bernard-jomain.json
  - Pour un métier qui ne correspond à aucun style, créer un nouveau fichier dans `styles/` (fonction `render(d)` qui s'appuie sur `core.page()`), avec sa propre direction artistique.
- `_generateur/prospects.csv` : suivi des prospects. `_generateur/MODELE_MAIL.md` : modèle de mail validé.

Toutes les maquettes sont non indexées (balise meta, `robots.txt`, `_headers`) et portent le bandeau Fyce.
