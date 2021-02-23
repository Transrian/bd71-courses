# Prise en main de Kibana

Maintenant que nous avons vu les **bases de l'ingestion de données** dans Elasticsearch, nous allons étudier la partie la plus intéressante, la **visualisation de données**!

Mais dans un premier temps, il va falloir comprendre le **fonctionnement** de Kibana.

## Composants

### Index pattern

*(Stack Management > Kibana > Index patterns)*

Un **index pattern**, dans Kibana, est la **représentation** de la *structure* de nos évènements. Il est associé à un ou plusieurs **index** Elasticsearch ou **alias**, et va synthétiser les différents champs, leur types, ansi que l'affichage que nous allons en faire dans Kibana.

Lors de la **définition** d'un index pattern, il faut définir, si possible, un **champ de type date**, la *date principale*, correspondant à la date de génération des données. Elle va permettre à Kibana, lorsque nous allons réaliser des visualisations, de savoir quelle champ utiliser, pour certains types de visualisations (eg. histogrammes)

Prenons par exemple cet index pattern:

![Exemple index pattern](resources/tp-3/images/exemple_index_pattern.png)

Nous pouvons voir:
- la majorité des champs sont de type **string**
- certains autres **types de champs** existent aussi, comme **ip**, **number**, **geopoint**
- pour tous les champs **string**, il existe un champ **.keyword**
    - le champ sans *.keyword* n'est **pas agrégable** -> il est uniquement utile lorsque nous allons faire des recherche de text dans son contenu
    - le champ avec *.keyword* **est aggrégable** -> nous allons l'utiliser principalement lors des **aggrégations**, dans les différentes visualisations Kibana.

Même si nous ne pouvons **pas modifier leur contenu** directement, nous pouvons modifier, à travers l'interface, la **manière** dont le champs sera **affiché** dans l'interface. Si nous prenons example d'un champs sous format nombre (alors qu'il s'agit en réalité de bytes), nous allons être capable de le définir pour le champ en question, comme dans la capture suivante:

![Exemple index pattern](resources/tp-3/images/pattern_number_to_bytes.png)

### Visualisations

Les visualisations sont les **briques** essentiels à la représentation visuelles des données, et chaque visualisation va contenir une ou plusieurs métriques.

Le terme **cardinalité** vas souvent être employé pour définir la pertinence des visualisations, en fonction des données. La **cardinalité** d'un champ correspond au **nombre de valeurs distinctes** présente dans celui-ci.

Si un champs possède:
- 5 valeurs distinctes, il a une cardinalité faible
- 100 valeurs distinctes, il a une cardinalité élevé

TODO


## 1. Dashboard de suivis des logs web

Pour **créer une dashboard**, plusieurs éléments sont impliqués:
- Un **index pattern Kibana**, qui va correspondre aux données utilisées. Comme nous venons de mettre en place un **alias**, nous l'utiliserons pour créer le pattern
- Des **visualisations**, qui correspondent à un élément unique
- Des **saved search**, qui correspondent à une **vue** des logs
- Enfin, les **dashboards** en elles-mêmes, qui **regroupent** des visualisations & saved-search

Pour créer un **index pattern Kibana**, allez dans Stack Management > Kibana > Index Patterns, et:
- Créer en un nouveau
- L'**Index pattern name** correspond au nom des indexes ou alias, nous allons donc entrer notre alias précédement créer, **GROUPEX_ACCESS**)
- Le **time field** correspond au champs date utilisé par défaut dans toutes les visualisations : dans notre cas, le champs date correspondant à la génération de l'évènement s'apelle `@timestamp`

Une fois créer, vous pouvez **aller** dans la partie **Discover** de Kibana, ou vous verrez vos logs!

Ci-dessous un exemple de ce que vous devriez voir:

![Kibana discover](resources/tp-3/images/expected_picture_dataflow.png)

