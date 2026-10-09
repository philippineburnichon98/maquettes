# Maquettes Fyce

- `site/` : le dossier publié (Cloudflare : répertoire `site`, aucune commande de build).
- `_generateur/` : générateur privé.
  - `python3 _generateur/build.py _generateur/sites/<prospect>.json` écrit `site/<slug>/index.html`.
  - Le champ `"style"` du JSON choisit la mise en page dans `_generateur/styles/` :
    - `chrono` : domaine à forte histoire (pellicule photo, frise, cuvées en étiquettes avec fiche technique). Exemple : domaine-de-la-folie.json
    - `bouchon` : bouchon / brasserie traditionnelle (nappe à carreaux, ardoise, carte imprimée, réservation intégrée, cave, groupes). Exemple : bouchon-des-cordeliers.json
    - `affiche` : REFUSÉ par Philippine (trop « affiche », pas assez chaleureux pour un restaurant). Ne pas réutiliser.
    - `cellier` : domaine avec beaucoup de cuvées (parole du vigneron, étagères de bouteilles cliquables, achat, points de vente, souvenirs). Exemple : domaine-bernard-jomain.json
  - Mise en page « classique » (sans champ style, fonction build() de build.py) : validée par Philippine pour Le Bouchon des Artistes (photo plein écran, carte, équipe, formulaire de réservation par e-mail `resaform`, réservation intégrée `booking`). Exemple : bouchon-des-artistes.json
  - Pour un métier qui ne correspond à aucun style, créer un nouveau fichier dans `styles/` (fonction `render(d)` qui s'appuie sur `core.page()`), avec sa propre direction artistique.
- `_generateur/prospects.csv` : suivi des prospects. `_generateur/MODELE_MAIL.md` : modèle de mail validé.

Toutes les maquettes sont non indexées (balise meta, `robots.txt`, `_headers`) et portent le bandeau Fyce.

## Règle photos (demandée par Philippine)
Reprendre TOUTES les images utiles du site d'origine, chacune à l'endroit qui lui correspond : grande image d'en-tête de chaque page (ex. la photo de groupe en tête de la page équipe va en tête de la section équipe), photos de chaque produit, portraits, pictogrammes des rubriques (champ 3e élément des items `features`), logos des labels et certifications (champ `logos` d'une `story`), photos de la salle, de la terrasse, de la façade. Ne jamais laisser une photo du site d'origine de côté sans raison.
