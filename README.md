# Maquettes Fyce

- `site/` : le dossier publié (Cloudflare : répertoire `site`, aucune commande de build).
- `_generateur/` : générateur privé.
  - `python3 _generateur/build.py _generateur/sites/<prospect>.json` écrit `site/<slug>/index.html`.
  - **Mise en page standard pour TOUS les prospects : la mise en page « classique » (JSON SANS champ `"style"`, fonction build() de build.py).** Choix définitif de Philippine (9 oct. 2026). On ne varie que les couleurs (`theme`), les polices, les photos et les sections utilisées selon le métier.
    - Sections disponibles : story (+ `logos`), quote, features (+ pictos), cards (+ `sheet` fiche technique, bouteilles, médailles, prix), menu (avec ou sans `aside`), booking (widget intégré type TheFork), resaform (module de réservation en 4 étapes : couverts + calendrier des jours d'ouverture `days`, créneaux midi/soir, coordonnées, confirmation ; la demande part par e-mail au restaurant), team (+ grande photo d'équipe `img`), timeline (frise des générations), gallery, banner, visit (+ carte). Popup `announce`, `logo`, vidéo de fond `hero.video`.
    - Exemples : bouchon-des-artistes.json, bouchon-des-cordeliers.json, domaine-de-la-folie.json, domaine-bernard-jomain.json
    - S'il manque un type de bloc pour reprendre un contenu du site d'origine, ajouter une section à build.py (pas un nouveau style).
  - Les styles sur mesure de `_generateur/styles/` (chrono, bouchon, affiche, cellier) sont ABANDONNÉS : Philippine préfère la mise en page classique. Ne plus les utiliser.
- `_generateur/prospects.csv` : suivi des prospects. `_generateur/MODELE_MAIL.md` : modèle de mail validé.

Toutes les maquettes sont non indexées (balise meta, `robots.txt`, `_headers`) et portent le bandeau Fyce.

## Règle photos (demandée par Philippine)
Reprendre TOUTES les images utiles du site d'origine, chacune à l'endroit qui lui correspond : grande image d'en-tête de chaque page (ex. la photo de groupe en tête de la page équipe va en tête de la section équipe), photos de chaque produit, portraits, pictogrammes des rubriques (champ 3e élément des items `features`), logos des labels et certifications (champ `logos` d'une `story`), photos de la salle, de la terrasse, de la façade. Ne jamais laisser une photo du site d'origine de côté sans raison.


- EXCEPTION validée par Philippine (9 oct. 2026) : ARGOS Diagnostic garde le style `releve` (plan coté, mètre ruban), avec les photos du site et le vert du logo. Ne pas le convertir en mise en page classique.
- EXCEPTION validée par Philippine (9 oct. 2026) : Girod-Roux Menuiserie garde le style `etabli` (mètre pliant, avant/après à glisser). Ne pas le convertir en mise en page classique.

## Règle couleurs (demande de Philippine)
- Chaque maquette reprend les couleurs du prospect : la couleur principale de son LOGO (ex. le rouge du logo) devient `theme.accent` (boutons, liens, sélection), `theme.accent2` une version un peu plus foncée ; les autres couleurs (`paper`, `ink`, `gold`, `heroem`) s'accordent avec sa charte (couleurs de son site actuel).
- Relève les codes couleur dans le CSS du site d'origine quand c'est possible (WebFetch sur la page ou ses feuilles de style), sinon d'après le logo.
- En plus, build.py applique automatiquement, dans le navigateur du visiteur, la couleur dominante du logo à `--accent` quand l'hébergeur de l'image l'autorise (CORS). Désactivable avec `"logo_accent": false` dans `theme` ; `"logo_vars"` choisit les variables CSS à colorer (par défaut `--accent,--accent-2`, `--cote` pour le style releve). Fonctionne aussi pour les styles (core.page). Le thème statique reste la valeur de secours : il doit donc déjà être juste.

## Statistiques de visite
- Toutes les maquettes chargent Cloudflare Web Analytics (sans cookie), ajouté automatiquement par build.py et core.page.
- Philippine exclut ses propres visites en ouvrant une fois une maquette avec `?moi` à la fin de l'adresse (mémorisé sur ce navigateur) ; `?pasmoi` annule.

## Règle blog et SEO (demande de Philippine, 9 oct. 2026)
- Un blog ou des actualités tenus à jour, c'est précieux pour le référencement : on les GARDE toujours, et en entier.
- Section `blog` de build.py : cartes d'articles (photo, thème, titre, résumé, lien « Lire l'article »), filtres par thème, bouton « Voir plus d'articles » (par paquets de `step`), lien vers toutes les actualités (`all`). Reprendre au moins tous les articles de la première page du blog d'origine, avec leurs images. Exemple : odin-blondot.json.
- Le reproche « actualités anciennes » ne s'utilise que si le blog est vraiment figé.

## Contrôle photos obligatoire avant chaque push (demande de Philippine, 9 oct. 2026)
- Une maquette sans logo ou sans les photos du site d'origine est inacceptable.
- Avant de pousser : relever, page par page, TOUTES les images du site d'origine (logo, bandeau d'en-tête de chaque page, photos de personnes, de produits/réalisations, des lieux, logos de labels) et vérifier que chacune est dans le JSON (pour Wix, comparer l'identifiant média ; pour Jimdo, l'identifiant `i…`).
- Les sections classiques acceptent une grande photo d'en-tête facultative `img` (cards, menu, gallery, blocks, visit, team) : y mettre le bandeau de la page d'origine correspondante.
- Pied de page : `footer.legal_url` = page Mentions légales du site d'origine. Carte en PDF : `pdf` dans la section menu. Descriptions des plats : 3e élément de chaque ligne de menu.
- Seules exceptions : logo du concepteur du site, icônes génériques (téléphone, e-mail, réseaux sociaux), images de banque sans rapport.
