# Modèle de site avec blog modifiable par le client

Pour Philippine (Fyce). Ce dossier est le point de départ d'un VRAI site client (pas une maquette) : site vitrine rapide,
hébergé chez Cloudflare, dont le client gère lui-même son blog depuis une interface en ligne (Pages CMS), sans rien installer.

## Comment ça marche
1. Le client va sur https://app.pagescms.org, se connecte avec son e-mail, ouvre « Articles du blog » et clique « Ajouter ».
2. Il écrit son article (titre, date, thème, photo, résumé, texte mis en forme) et enregistre.
3. Pages CMS enregistre l'article dans le dépôt GitHub du site ; Cloudflare reconstruit le site tout seul (environ 1 minute).
4. L'article a sa propre page (/blog/adresse-de-l-article/), apparaît dans la liste du blog, sur l'accueil (3 derniers),
   dans le plan du site envoyé à Google (sitemap.xml) et dans le flux RSS. Une case « Brouillon » permet de préparer sans publier.

Coût : 0 € (GitHub, Cloudflare et Pages CMS gratuits pour ce volume). Rien à mettre à jour côté sécurité (pas de base de données, pas de WordPress).

## Mettre en place un nouveau client (une fois, environ 30 minutes)
1. **Dépôt** : créer un dépôt GitHub privé pour le client (ex. `site-domaine-de-la-folie`) et y copier le contenu de ce dossier.
2. **Contenu** : remplir `content/site.json` (nom, coordonnées, couleur, adresse du site dans `url`, menu), mettre le logo
   et les photos dans `public/images/`, reprendre les articles existants dans `content/articles/`
   (un fichier `AAAA-MM-JJ-adresse.md` par article, avec l'en-tête titre/date/thème/photo/résumé, voir les exemples).
   Les pages vitrine (accueil, présentation, prestations…) se règlent dans `src/build.mjs` ; je peux les générer
   à partir de la maquette validée.
3. **Cloudflare** : Workers & Pages → Créer → Importer un dépôt GitHub → choisir le dépôt.
   Commande de build : `npm install && npm run build`. Le fichier `wrangler.jsonc` indique de publier le dossier `dist`.
   Puis Paramètres → Domaines : brancher le nom de domaine du client.
4. **Pages CMS** : aller sur https://app.pagescms.org, se connecter avec GitHub, installer l'application Pages CMS sur le dépôt
   du client, ouvrir le dépôt (le fichier `.pages.yml` décrit déjà les champs), puis dans « Collaborators »
   inviter le client par e-mail. Il reçoit un lien de connexion, sans compte GitHub.
5. **Référencement (indispensable si le client avait déjà un site)** :
   - reprendre TOUS les anciens articles et pages ;
   - pour chaque ancienne adresse, ajouter une ligne dans `public/_redirects` :
     `/ancienne-adresse.html  /blog/nouvelle-adresse/  301` ;
   - après la mise en ligne, déclarer `https://www.site-du-client.fr/sitemap.xml` dans Google Search Console.

## Tester en local
```
npm install
npm run build        # écrit le site dans dist/
```

## Ce qu'on peut vendre
- Option « Blog modifiable par vous-même » (interface + formation de 30 minutes).
- Reprise des articles existants et redirections (conservation du référencement).
