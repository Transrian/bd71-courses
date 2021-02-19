# TP Bonus

*Ce TP est facultatif, et rien de ce qui sera dedans ne comptera pas dans l'examen.*

**Mise en place d'une stack Elastic & Kibana en local.**

## 1. Installation d'Elasticsearch

> Il est **extrêmement recommandé** d'exécuter les commandes suivantes dans un répertoire **local**, et non pas sur un **disque réseau**

Ouvrez un shell et tapez les commandes suivantes:

```bash
# Télécharger l'archive contenant logstash
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.11.1-linux-x86_64.tar.gz -O elasticsearch.tar.gz

# Décompresser l'archive
tar -zxvf elasticsearch.tar.gz

# Suppression de l'archive
rm elasticsearch.tar.gz

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

Si tout fonctionne bien, quitter le processus (CTRL+C), et lancer Elaticsearch en tant que daemon (il fonctionnera en arrière-plan) avec la commande:

```bash
JAVA_HOME="" ./bin/elasticsearch -d
```

Pour l'**éteindre**, vous pourrez faire, à tout moment:

```bash
# Récupération du pid du processus
# Il s'agira de la deuxième colonne
# valentin >19860<  2689 85 09:43 pts/5    00:00:40 /home/valentin/elasticsearch-7.11.1/jdk/bin/java..
ps -eaf | grep elasticsearch | grep -v grep

# Envoie de la commande SIGKILL au processus, pour qu'il s'arrête
kill -9 19860
```

Vous pourrez suivre les logs du processeur à tout moment, en regardant dans le dossier `logs`:

```bash
tail -f logs/elasticsearch.log
```

## 2. Installation de Kibana

Ouvrez un shell et tapez les commandes suivantes:

```bash
# Télécharger l'archive contenant logstash
wget https://artifacts.elastic.co/downloads/kibana/kibana-7.11.1-linux-x86_64.tar.gz -O kibana.tar.gz

# Décompresser l'archive
tar -zxvf kibana.tar.gz

# Suppression de l'archive
rm kibana.tar.gz

# Entez dans le répertoire de logstash
cd kibana-7.11.1-linux-x86_64/
```

Testons à présent Kibana (il faut qu'Elasticsearch soit démarré!):

```bash
./bin/kibana
```

Si vous n'avez pas d'erreurs, une fois le message suivant affiché :

```
[info][server][Kibana][http] http server running at http://localhost:5601 
```

Vous aurez accès à Kibana depuis un navigateur web à l'adresse suivante : http://localhost:5601.

Si vous avez un problème de port déjà utilisé, documenté, dans le fichier `config/kibana.yml`, la ligne `#server.port: 5601`, en en choisissant un autre.

Pour lancer Kibana en temps que daemon, vous pouvez utiliser la commande:

```bash
nohup ./bin/kibana &
# N'oubliez pas de récupérer le pid du daemon
# Par exemple
# [1] 23421
```

Pour l'arrêter à tout moment, même principe que pour Elasticsearch, mais nous allons nous servir du pid précédemment récupéré:

```bash
kill -9 23421
```

## Suite

A partir de là, vous pouvez essayer de **reproduire les TP Logstash** que nous avons faits dans le [TP 2](tp-2.md?id=tp-2), en modifiant **l'output Elasticsearch** avec l'URL pour Elasticsearch de votre cluster local!

En plus d'une URL différente, il vous faudra:
- supprimer le nom d'utilisateur / mot de passe (le cluster local n'est pas authentifié)
- supprimer les paramètres concernant le TLS (TLS désactivé par défaut)
