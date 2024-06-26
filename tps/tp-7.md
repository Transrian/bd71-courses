# Canvas (2h)

Après avoir vu toutes les bases de Kibana, nous allons nous intéresser à un dernier point, Canvas, qui va nous permettre de créer une sorte de **Présentation dynamique** synthétique des données

## 1.1 Utilité

Mêmes si les dashboard Kibana sont énormément utilisés, il existe, dans Kibana, un autre moyen de visualiser les données, de manière synthétique, nommée [Canvas](https://www.elastic.co/fr/what-is/kibana-canvas).

Il va permettre, contrairement aux dashboard, d'avoir une présentation beaucoup plus libre, et légère, permettant de bien mettre en valeur les KPIs qui nous intéressent.

Ci-dessous des exemples de Canvas, réaliser dans Kibana ([source](https://www.elastic.co/fr/what-is/kibana-canvas)):


**Monitoring du hub d'un aéroport**:

![canvas clothes sales](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/bltd3bcb6c0c16af459/5c3047b6e71ce40c6e4ad94b/airport4-upd.gif)

**Ventes d'une entreprise par type d'habits**:

![canvas clothes sales](https://static-www.elastic.co/v3/assets/bltefdd0b53724fa2ce/blte86a13ae6e0733c3/5ce2b0f1932da9737b262b85/screenshot-canvas-business-analytics.png)

**Monitoring d'une infrastructure simple**:

![canvas infra monitoring](https://static-www.elastic.co/v3/assets/bltefdd0b53724fa2ce/blt3e1c8c55e9aa879b/5ce2b0dc1df9c928761cdc20/screenshot-canvas-infrastructure.png)

**Suivi de la vente de café en temps réel**:

![canvas clothes sales](https://static-www.elastic.co/v3/assets/bltefdd0b53724fa2ce/blt801ffea51d590277/5c18b20b1e9a48990b55d354/screenshot-canvas-inspire-coffee.jpg)



Tous ces exemples sont beaucoup plus séduisants que des dashboard, n'est-ce pas ? Quel est le piège, alors ?
- Les **Canvas** sont adaptès à afficher des informations simples, et n'entrent pas dans les détails
- Il est **impossible de filter** sur des valeurs dans un Canvas (mis à part à la construction de la dashboard)
- Les dashboard, comparativement, sont **beaucoup plus simples à faire**. Elles sont conçues pour être facilement créées, modifiables, et utilisables. Pour **Canvas**, seule sa facilité de compréhension et de récapitulation compte (et ça passe par le **design**, qui est un métier en soi).
- Généralement, même si des exceptions existent, la **cible** de ces deux outils est **différente**:
    - Les **dashboard** sont utilisés par les **dev**, les **responsables des applications**, ... et vont permettre d'**entrer dans les détails**
    - Les **Canvas**, du fait de leur simplicité apparente, et de leur simplification extrême des données, sont plutôt utilisés par les chefs / la **hiérarchie**

Même si pour ces exemples nous n'avons qu'une seule **page**, il est possible, comme un PowerPoint, d'en avoir **plusieurs**, et de les faire changer automatiquement, **à un interval de temps donné**, comme un carrousel.

## 1.2 Interface

L'interface de Canvas (Analytics > Canvas) va se présenter comme ci-dessous:

![canvas interface](images/canvas_full_picture.png)

Nous avons une **fenêtre centrale** (dont nous pouvons configurer la taille, sur la droite), qui est notre *feuille de travail*, sur lequel nous allons pouvoir rajouter des composants.

Si nous **ajoutons des composants**, nous en avons de trois types principaux:
    - Du **texte**, pour afficher des informations, comme un titre
    - Des **visualisations Canvas**, présent dans plusieurs catégories
    - Des **visualisations Kibana**, que nous utilisons par exemple dans les dashboard

Même s'il est possible d'utiliser des **visualisations classiques**, c'est **fortement déconseillé**. En effet, les **visualisations Canvas sont par design minimaliste**, ce qui n'est pas le cas des visualisations classiques ; et le but de Canvas est d'afficher des informations de la manière la plus simplifiée possible!

Si nous essayons d'ajouter **un graphe de type ligne** (Chart > Lines), il va être **ajouté à la feuille de travail**, avec un jeu de données de démo. Pour changer celui-ci, sur la partie de droite, il nous faut aller dans la partie **Data**

À partir de là, pour sélectionner notre source de donnée, le processus va être différent du processus classique que nous avons vu avec **Lens**, car les requêtes nous permettant de **récupérer les données** doivent-être fait en **SQL**.

Dans un premier temps, il va falloir changer la source de donnée par défaut, en cliquant sur "**Demo data**"

![canvas default datasource](images/canvas_pannel_data.png)

Ensuite, sélectionner l'**Elasticsearch SQL**

![canvas default datasource](images/pannel_canvas_source.png)

Dans cette partie, c'est là que nous allons **définir la requête SQL**. Dans cet exemple, nous allons utiliser la **requête 6**, appelé **"Nombre de naissance par sexe"**, présent dans la suite du TP. Pour la tester à tout moment, nous pouvons cliquer sur **Preview data**, dont un exemple de résultat est afficher ci-dessous, et si le résultat semble correct, nous allons pouvoir sauvegarder

![canvas default datasource](images/pannel_canvas_query.png)

Lorsque nous affichons la **preview**, le résultat (les données utilisables dans notre visualisation) sera affiché dans une table! Comme pour du SQL classique, plus nous récupérons de données, plus l'execution de la requête sera longue, il faut donc faire des requêtes optimisées au possible, afin de récupérer le moins de données que possible!

![canvas default datasource](images/pannel_canvas_ds_preview.png)

Une fois sauvegardé, dans la partie **Display**, nous avons accès aux options de **Canvas**, qui même si moins nombreuses, permettent de faire sensiblement la même chose que pour Lens.

> La principale différence est que le **split** de Lens est ici appelé **Color**

Dans cet exemple:
    - l'**axe X** représente le **temps**
    - l'**axe Y** représente la moyenne (de la somme) des prénoms données = **total des naissances**
    - la **couleur** représente le **sexe** : féminin ou masculin

![canvas default datasource](images/canvas_display_options.png)

Ce qui vas nous donner le résultat suivant, sur la feuille de travail:

![canvas default datasource](images/pannel_canvas_simple_result.png)

Il existe d'autres types de visualisations, mais de manière général la **documentation** de **Canvas** est présente à la page [suivante](https://www.elastic.co/guide/en/kibana/current/canvas.html)

### 2.1 Remarques

Dans Canvas, à l'heure actuel, des **regressions** ont été commises, et il y a plusieurs **bugs**, potentiellement très **problématiques**:

- Par défaut, les Canvas sont **sauvegardé automatiquement**
- Si **plusieurs personnes édite un même Canvas** en même temps, certains éléments risquent de ne **pas être sauvegardés**
- Quelquefois, même s'il n'y a pas d'erreurs sur une visualisation, **rien de s'affiche**. Dans ce cas là, il suffit (généralement) de **quitter la page Canvas, et revenir dessus**

### 2.2 Créations d'une dashboard sur les prénoms en France

En nous servans du jeu de donnée du TP précédant (avec l'index pattern `prenoms-france`), nous allons créer un canvas représentant au minimum les éléments suivants:

- Un sélecteur de temps (par défaut, sur les 100 dernières années)

En termes de visualisations:

1) Total de naissance de garçon (une colonne, une ligne)
2) Total de naissance de filles (une colonne, une ligne)
3) 10 (au moins) prénoms masculins les plus répandus (deux colonnes, multiples lignes)
4) 10 (au moins) prénoms féminins les plus répandus (deux colonnes, multiples lignes)
5) 10 départements avec le plus de naissances (deux colonnes, multiples lignes)
6) nombre de naissances par sexe (trois colonnes, multiples lignes)
7) diversité des colonnes par sexe (trois colonnes, multiples lignes)

> Toutes les **requêtes SQL** sont faites et présentes pour-être utilisées dans la partie suivante!

### 2.3 Requêtes SQL à utiliser

**1) Total de naissances de garçons**

```sql
SELECT sum(nombre)
FROM "prenoms-france"
WHERE sexe=1
```

**2) Total de naissances de filles**

```sql
SELECT sum(nombre)
FROM "prenoms-france"
WHERE sexe=2
```

**3) 100 prénoms masculins les plus répandus**

```sql
SELECT prenom, sum(nombre) as total
FROM "prenoms-france"
WHERE sexe=1 and prenom != '_PRENOMS_RARES'
GROUP BY prenom
ORDER BY 2 DESC
LIMIT 100
```

**4) 100 prénoms féminins les plus répandus**

```sql
SELECT prenom, sum(nombre) as total
FROM "prenoms-france"
WHERE sexe=2 and prenom != '_PRENOMS_RARES'
GROUP BY prenom
ORDER BY 2 DESC
LIMIT 100
```

**5) Les 10 départements avec le plus de naissances**

```sql
SELECT sum(nombre) as total, departement
FROM "prenoms-france"
GROUP BY  departement
ORDER BY total desc
LIMIT 10
```

**6) Nombre de naissance par sexe**

```sql
SELECT "@timestamp", sum(nombre), CASE WHEN sexe = 1 THEN 'masculin' ELSE 'feminin' END as sexe
FROM "prenoms-france"
GROUP BY "@timestamp", sexe
```

**7) Diversité des prénoms par sexe**

```sql
SELECT "@timestamp", count(*) as total, CASE WHEN sexe = 1 THEN 'garcon' ELSE 'fille' END as sexe
FROM "prenoms-france"
GROUP BY "@timestamp", sexe
```

### 2.3 Exemple de Canvas

Ci-dessous un exemple de Canvas que j'ai réalisé, en utilisasnt les requêtes précédentes. (PS. et oui, je ne suis vraiment pas doué en graphisme). 

**Essayer de faire quelque chose de mieux**, en explorant toutes les fonctionnalités de Canvas!

![canvas picture](images/canvas_image.png)

> Vous n'êtes pas obligé d'utiliser les mêmes types de visualisations, utiliser ce que vous pensez être le plus pertinent

**Question**: Que pouvez-vous dire à propos de ces données sur les prénoms & naissances ? Quels sont les tendances, différences, etc ?