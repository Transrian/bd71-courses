# Exploitation de données immobilières (~4h)

**Modalités**:
  - TP à effectuer en groupe, note commune aux personnes du groupe
  - Utiliser le Kibana dans le cloud: https://bd71.transrian.fr:5601
  - Lisez le tp de bout en bout au début, et n'hésitez pas si vous avez des questions concernant la compréhension du TP
  - 6 jours pour le faire, jusqu'au 13 avril à minuit, 5 points retirés par jour de retard.
  - pour le rendu, m'envoyer un mail à valentin.bourdier@utbm.fr, avec les informations suivantes:
    - le groupe & les personnes le composant
    - un lien vers la dashboard
    - les réponses aux questions sous format PDF

## 1.1 Contexte

Vous travaillez pour un [fonds d'investissement immobilier](https://www.scpi-8.com/opci/definition-fpi) **Australien**, et vous cherchez à savoir s'il est **rentable d'investir dans l'immobilier** des 5 plus grandes villes australiennes (Sydney, Perth, Adelaide, Brisbane & Canberra).

On considèrera ici qu'il est intéressant de faire des achats si le **prix de vente augmente par rapport au prix d'achat**. Les **critères** à prendre en compte seront principalement le **nombre de pièces**, le **type de bien**, et **le quartier**.

Pour ce faire, chaque groupe aura un **jeu de données légèrement différent**, avec les **ventes immobilières** entre mi-2018 à mi-2020.

## 1.2 Donnée

Basé sur [ce jeu de données](https://www.kaggle.com/htagholdings/aus-real-estate-sales-march-2019-to-april-2020)

| Nom du champ    | Description                               | Exemple                             |
| --------------- | ----------------------------------------- | ----------------------------------- |
| `@timestamp`    | Date de l'évènement                       | Jul 16, 2020 @ 00&#58;00&#58;00.000 |
| `bedrooms`      | Nombre de pièces                          | 3                                   |
| `city_name`     | Nom de la ville                           | Adelaide                            |
| `date_sold`     | Quand à été vendu le bien (=~ @timestamp) | Jul 16, 2020 @ 02&#58;00&#58;00.000 |
| `location`      | Localisation géographique du bien         | -34.9005324,138.53064443            |
| `price`         | Prix du bien (peut-être nul  )            | 311000                              |
| `property_type` | Type de bien (house, unit or townhouse)   | unit                                |
| `suburb`        | Voisinage (quartier)                      | Findon                              |

## 1.3 Import des données

**Récupérer le jeu de donnée** associé à votre groupe à l'adresse suivante: https://mega.nz/folder/3a5wEBrD#sYkoPgnro8jH7-zLxchzkQ, et ouvrir l'archive, un fichier json se trouve dedans.

Pour **importer** le jeu de donnée **de votre groupe**, utiliser la fonctionnalité **Import Data**, comme pour les TPs précédent, dans la partie Machine Learning > Data Visualizer.

Veuillez **nommer** votre **index** comme ceci: `<groupeX>-australia-sales` 

Sur la **seconde fenêtre**, une fois les paramètres validés, cliquer sur **Advanced**, comme sur l'image suivante:

![Advanced button](images/import_file_advanced.png)

Et changer le **type** du champ `location` de **keyword** à **geo_point**, dans le cadre  appelé **Mappings**, comme sur l'image suivante:

![Advanced button](images/modification_geopoint.png)

> Vous ne devriez pas avoir d'erreurs d'insertion

## 1.4 Vérification de l'import des données

Une fois les données importées, allez vérifier dans les Index patterns Kibana si vos données sont bien typées:
    - les champs `bedrooms` & `price` devrait-être des **nombres**
    - le champ `location` devrait-être un **geo_point**

Comme sur l'image suivante:

![Australia sales index pattern](images/australia_sales_index_pattern.png)

De la même manière, dans le **Discover**, si vous regardez sur trois ans, vous devriez voir des données:

![Australia basic discover](images/discover_australia.png)

> Comme chaque jeu de données est unique, vous n'aurez pas le même nombre d'évènements que sur cette capture d'écran, ni que vos camarades

## 2. TP

### 2.1 Dashboard (/10)

(0.6 point pour chaque, 2 points pour l'aspect esthétique & pratique pour l'utilisation de la dashboard)

Réaliser une **dashboard Kibana**, permettant de visualiser:

1) l'évolution du nombre d'évènement au cours du temps
2) le total des prix, pour tous les biens vendu
3) le prix moyens des biens vendus
4) la répartition des types de biens vendus
5) le nombre de vente, au cours du temps, par type de biens
6) le total des ventes, au cours du temps, par type de biens
7) Une carte, avec pour métrique le total des ventes, pour les zones couvertes en Australie
8) Une représentation du prix moyen des ventes, par ville & par quartier (sur la même visualisation)
9) L'évolution de la moyenne du prix ventes, par ville
10) La répartition des ventes par nombre de pièces
11) L'évolution du prix de vente, en fonction du nombre de pièces, au cours du temps
12) Une saved search, permettant de visualiser les données, avec pour colonnes:
    - Date
    - Nom de la ville
    - Type
    - Quartier
    - Nombre de pièces
    - Prix

> La carte à réaliser n'est pas du même type que nous avons utiliser jusqu'à présent, vous pouvez utiliser `Heat Map`

### 2.2 Machine learning (/3)

Réalisez trois jobs de **machines learning** (interval de temps recommandé):

1) *(1pt)* Un **single** metric, concernant le **nombre** d'évènements
2) *(1pt)* Un **single** metric, concernant le **prix moyen**
3) *(1pt)* Un **multi** métrique, concernant le **prix moyen**, avec:
  - split par ville
  - avec pour influenceurs
    - ville
    - nombre de pièces
    - quartier
    - type de propriétés

### 2.3 Questions (/7)

> A rendre sous format PDF, par mail

**Argumentez les réponses si nécessaire**, avec des captures d'écran et / ou une description de ce que vous avez fait pour obtenir le résultat

**Dashboard** *(/2)*:

Sur toute la période des données:

  - *(1pt)* Pour la ville de Sydney, pour quel nombre de pièces les variations de prix ont été les plus importantes ? Jusqu'à combien aurions-nous pu gagner en investissant au bon moment dans ce type de bien (arrondi à 100k)
  - *(1pt)* Pour les **villes autres que Sydney**, quel **type de bien est le plus vendu** ? Quel est le total du prix des ventes effectuées pour ce type de bien ? (Arrondi au milliard)


**Machine learning** *(/3)*:

  - *(1pt)* En corrélant visuellement avec le résultat du **job 1** et **job 2**, la baisse des prix fin décembre 2019 / début janvier 2020 vous semble-t-elle logique ? Pourquoi ?
  - *(1pt)* D'après le résultat du **job 2**, si nous étions le 14 juin 2020:
    - serions-nous dans une bonne période pour investir, et acheter un logement ?
    - a-t-il existé dans le passé une période plus propice aux investissements ?
  - *(1pt)* D'après le résultat du **job 3**, il semblerait qu'il y a eu beaucoup d'anomalies à Melbourne, aux alentours de Décembre 2019. Quels sont les facteurs communs entre les anomalies les plus prononcées ?

**Question libre** *(/2)*: Qu'auriez-vous fait, dans cette situation, si vous aviez cette dashboard, et les jobs de machine learning configurés durant la période des données ? Auriez-vous investi, ou pas, et pourquoi ?
