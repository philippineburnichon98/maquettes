# Maquettes Fyce

- `site/` : le dossier publié (Cloudflare : répertoire `site`, aucune commande de build).
- `_generateur/` : générateur privé.
  - `python3 _generateur/build.py _generateur/sites/<prospect>.json` écrit `site/<slug>/index.html`.
  - **Mise en page standard pour TOUS les prospects : la mise en page « classique » (JSON SANS champ `"style"`, fonction build() de build.py).** Choix définitif de Philippine (9 oct. 2026). On ne varie que les couleurs (`theme`), les polices, les photos et les sections utilisées selon le métier.
    - Sections disponibles : story (+ `logos`), quote, features (+ pictos), cards (+ `sheet` fiche technique, bouteilles, médailles, prix), menu (avec ou sans `aside`), booking (widget intégré type TheFork), resaform (réservation par e-mail), team (+ grande photo d'équipe `img`), timeline (frise des générations), gallery, banner, visit (+ carte). Popup `announce`, `logo`, vidéo de fond `hero.video`.
    - Exemples : bouchon-des-artistes.json, bouchon-des-cordeliers.json, domaine-de-la-folie.json, domaine-bernard-jomain.json
    - S'il manque un type de bloc pour reprendre un contenu du site d'origine, ajouter une section à build.py (pas un nouveau style).
  - Les styles sur mesure de `_generateur/styles/` (chrono, bouchon, affiche, cellier) sont ABANDONNÉS : Philippine préfère la mise en page classique. Ne plus les utiliser.
- `_generateur/prospects.csv` : suivi des prospects. `_generateur/MODELE_MAIL.md` : modèle de mail validé.

Toutes les maquettes sont non indexées (balise meta, `robots.txt`, `_headers`) et portent le bandeau Fyce.

## Règle photos (demandée par Philippine)
Reprendre TOUTES les images utiles du site d'origine, chacune à l'endroit qui lui correspond : grande image d'en-tête de chaque page (ex. la photo de groupe en tête de la page équipe va en tête de la section équipe), photos de chaque produit, portraits, pictogrammes des rubriques (champ 3e élément des items `features`), logos des labels et certifications (champ `logos` d'une `story`), photos de la salle, de la terrasse, de la façade. Ne jamais laisser une photo du site d'origine de côté sans raison.
