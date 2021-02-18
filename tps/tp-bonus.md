# TP Bonus

*Ce TP est facultatif, et rien de ce qui sera dedans ne contera dans l'examen.*

**Mise en place d'une stack Elastic & Kibana en local.**

## 1. Installation d'Elasticsearch

> Il est **extremmement recommandé** d'executer les commandes suivantes dans un repertoire **local**, et non pas sur un **disque réseau**

Ouvrez un shell et taper les commandes suivantes:

```bash
# Téléhcharger l'archive contenant logstash
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.11.1-linux-x86_64.tar.gz -O elasticsearch.tar.gz

# Décompresser l'archive
tar -zxvf elasticsearch.tar.gz

# Entez dans le répertoire de logstash
cd elasticsearch-7.11.0
```

Maintenant, testons le fait qu'Elasticsearch fonctionne bien:

```bash
JAVA_HOME="" ./bin/elasticsearch
```

S'il n'y a aucun message d'erreur, essayer d'accéder à Elasticsearch depuis le navigateur à l'adresse suivante : http://localhost:9200

```json
{
  "name": "X970670",
  "cluster_name": "elasticsearch",
  "cluster_uuid": "S2yGWEdxSvqWnYYDtUn3WQ",
  "version": {
    "number": "7.11.1",
    "build_flavor": "default",
    "build_type": "tar",
    "build_hash": "ff17057114c2199c9c1bbecc727003a907c0db7a",
    "build_date": "2021-02-15T13:44:09.394032Z",
    "build_snapshot": false,
    "lucene_version": "8.7.0",
    "minimum_wire_compatibility_version": "6.8.0",
    "minimum_index_compatibility_version": "6.0.0-beta1"
  },
  "tagline": "You Know, for Search"
}
```

Si Elasticsearch ne fonctionne pas, parce que le port est déjà pris, vous pouvez le changer : > 1000 si non root, sinon libre (dans le fichier `conf/elasticsearch.yml`, décommentez la ligne `#http.port: 9200`, en précisant votre port)

Si tout fonctionne bien, quitter le processur (CTRL+C), et lancer Elaticsearch en tant que daemon (il fonctionnera en arrière plan) avec la commande:

```bash
JAVA_HOME="" ./bin/elasticsearch -d
```