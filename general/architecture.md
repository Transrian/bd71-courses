# Architecture de l'infrastructure

## Architecture des composants d'un server

Dans chaque serveurs, les logiciels suivant sont installés:

**Pour les éléments principaux**:

- [Elasticsearch](https://www.elastic.co/fr/elasticsearch/): base de donnée NoSQL, avec moteur de recherche distribué
- [Kibana](https://www.elastic.co/fr/kibana/): interface web pour la visualisation des données Elasticsearch
- [Nginx](https://www.nginx.com/): Serveur web haute performance
- [Redis](https://redis.io/): base de donnée stockant les données en mémoire

**Pour les outils de monitoring**:

- [Filebeat](https://www.elastic.co/fr/beats/filebeat): Agent de transfer de logs
- [Metricbeat](https://www.elastic.co/fr/beats/metricbeat): Agent de collecte de métriques
- [Heartbeat](https://www.elastic.co/fr/beats/heartbeat): Moniteur de surveillance (http, tcp, ...)

Les **flux de communications** sont telles qu'indiqués sur le schéma ci-dessous:

![Architecture des composants d'un server](images/internal_server_architecture.png)

Seuls Elasticsearch, Nginx & Redis sont accessibles depuis l'extérieur du serveur.

## Architecture global et interconnection des composants

En plus de l'échelle individuelle, nous devons considérer l'architecture global, car celle-ci est très interconnecté.

- Les différents **noeuds Elasticsearch** forment un clusteur 3 noeuds, avec un tolérence de faute à n - 1
    - Si nous perdons un noeud, le cluster reste fonctionnel
- Les 3 **instances Kibana** sont toutes configurées pour communiquer avec **chacun des noeuds** elasticsearch
    - Tant qu'une instance est fonctionnelle, nous pourrons visualisez les données
- Les 3 **instances Nginx** sont configuré en tant que de [proxy inverse](https://frwikipedia.org/wiki/Proxy_inverse) et [repartiteur de charge](https://fr.wikipedia.org/wiki/R%C3%A9partition_de_charge) pour les instances Kibana. Cela signifie que si une des instances Kibana tombe, une autre prendra le relais, et cela transparent pour l'utilisateur
- Les 3 **instances Redis**, quand-à elles, sont totalement **indépendantes** : leur état n'as aucune influence sur le reste de l'architecture

Ci dessous un schéma simplifié de l'architecture (certaines flèches sont manquantes, pour gagner en clarté):

![Interconnection des composants](images/server_interconnection_architecture.png)
