# TP Bonus 2

*Ce TP est facultatif, et rien de ce qui sera dedans ne comptera pas dans l'examen.*

**Interrogation de l'API Elasticsearch.**

**Prérequis**: TP2

## Elasticsearch queries

Même si lors de ces TPs, nous allons exclusivement utiliser Kibana pour accéder et visualiser nos données, il est également possible d'y accéder à **travers des APIs Elasticsearch**, pour faire des recherches, des aggrégations, etc.

Comme lors du TP3, nous allons pouvoir nous servir du **Dev Tools** de Kibana, pour lancer ces queries (il est également possible de se servir de l'API Elasticsearch en ligne de commande, même si c'est moins pratique).

Ces APIs sont ceux dont on peux se **servir** dans **des applications**, utilisant Elasticsearch comme stockage, par exemple.

Dans le dev tools, la syntaxe minimale pour executer une query est la suivante:

```json
GET GROUPEX_ACCESS/_search
{

}
```

Avec:
- le **verbe http**: GET, POST, DELETE, ...
- l'**index** ou l'**alias** ciblé
- la sous partie de l'index / l'**action**
- dans les lignes suivantes, le **body** json

A l'intérieur de ce body, nous allons pouvoir mettre des filtres, afin de filtrer la donnée. Par exemple, pour **afficher les évènements uniquement en erreur**:

```json
GET GROUPEX_ACCESS/_search
{
  "query": {
    "term": {
      "event.outcome": {
        "value": "failure"
      }
    }
  }
}
```

Il existe beaucoup de documentation sur la partie query, que vous pouvez trouver à cette addresse : https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html

Vous pouvez essayer de réaliser les queries suivantes:

- **Récupération des données de la dernière heure seulement**
- **Récuperation du nombre d'évènement, sur la dernière heure**
- **Récupération du nombre d'évènement, heure par heure, sur les 12 dernières heures**
- **Récupération du nombre d'évènement, heure par heure, sur les 12 dernières heures, par serveur**