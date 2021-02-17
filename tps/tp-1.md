# TP 1

Introduction à la collecte et au traitement des données.

**TLDR**: Nous allons voir comment **récupérer des données**, les **analyser**, et les **envoyer dans Elasticsearch**, de deux manière différentes : avec *Filebeat*, et avec *Logstash*

## 1. Logstash

[Logstash](https://www.elastic.co/fr/logstash) est un outils multi-fonctions, de type [ETL](https://fr.wikipedia.org/wiki/Extract-transform-load). Commercialisé par [Elastic](www.elastic.co), il est historiquement l'outils de prédilection pour récuperer et transformer des données pour [Elasticsearch](https://www.elastic.co/fr/elasticsearch).

En tant qu'ETL, il est capable de:

- **lire et écrire** depuis de **nombreuses sources de données**: fichier, tcp, http, sql, kafka, redis, ...
- **transformer** les données, pour qu'elles soient interprétable et utilisable dans Elasticsearch (et donc visualisable dans Kibana)

### 1.1 Installation , test et configuration de Logstash

Dans un premier temps, nous allons **installer Logstash**, et dans un second temps, **le tester**, pour voir si tout fonctionne bien ; et le **configurer** dans un dernier temps.

#### 1.1.1 Installation de Logstash

> Il est **extremmement recommandé** d'executer les commandes suivantes dans un repertoire **local**, et non pas sur un **disque réseau**

Ouvrez un shell et taper les commandes suivantes:

```bash
# Téléhcharger l'archive contenant logstash
wget https://artifacts.elastic.co/downloads/logstash/logstash-7.11.0-linux-x86_64.tar.gz -O logstash.tar.gz

# Décompresser l'archive
tar -zxvf logstash.tar.gz

# Entez dans le répertoire de logstash
cd logstash-7.11.0
```

Maintenant que Logstash est téléchargé, effectuons un test sommaire pour voir si il est correctement configuré:

```bash
# Vérification de la version de logstash
JAVA_HOME='' ./bin/logstash --version
```

Vous devez obtenir un message comme celui-ci (le chemin du jdk utilisé est important):

```
Using bundled JDK: /my/path/to/logstash/directory/logstash-7.11.0/jdk
logstash 7.11.0
```

Si ce n'est pas le cas, il y a probablement un problème.

Néanmoins, si tout fonctionne, nous pouvons supprimer l'archive de Logstash précédament téléchargée:

```bash
rm logstash.tar.gz
```

#### 1.1.2 Test de Logstash

Lancez la commande suivante:

```bash
# Entrez dans le répertoire de logstash
cd logstash-7.11.0

# Lancement de logstash avec une configuration en ligne de commande
JAVA_HOME='' ./bin/logstash --log.level=error -e "input { stdin { type => stdin } } output { stdout { codec => rubydebug } }"
```

Une fois la ligne suivante affichée:

> The stdin plugin is now waiting for input:

Taper une chaine de caractère, suivis de la touche entrée : cette première devrait-être répété, avec des métadonnées supplémentaires, comme dans l'exemple suivant:

```
The stdin plugin is now waiting for input:
Ceci est un simple test
{
          "host" => "X970670",
      "@version" => "1",
       "message" => "Ceci est un simple test",
    "@timestamp" => 2021-02-16T18:43:22.222Z,
          "type" => "stdin"
}
```

**N.B.**: Vous pouvez faire CTRL+C pour quitter à tout moment

#### 1.1.3 Configuration de Logstash

Comme nous n'allons pas à chaque fois entrer la configuration en ligne de commande, nous allons configurer Logstash afin qu'il prenne en compte des fichiers de configuration

Recréons le fichier de configuration logstash `logstash.yml` situé dans le dossier `config` à partir de la configuration suivante:

```yml
# Chemin vers le dossier de data
path.data: "./data2"

# Si les évènements en sortie doivent-être ordonnés ou non
pipeline.ordered: auto

# Log level
log.level: info

# Chemin vers les fichiers de logs
path.logs: "./logs"
```

Puis créez le dossier qui va servir à contenir nos fichiers de configurations:

```bash
mkdir -p "./conf/my-first-test"
```

Ainsi que deux autres dossiers, que nous utiliserons plus tard:

```bash
mkdir output input
```

Puis nous allons créer dans ce dossier notre fichier de configuration logstash, au chemin `./conf/my-first-test/logstash.conf`:

```ruby
input {
    stdin {
        type => stdin
    }
} 

output {
    stdout {
        codec => rubydebug
    }
}
```

Enfin lançons Logstash, en prenant en compte ces fichiers de configuration:

```bash
JAVA_HOME='' ./bin/logstash -f conf/my-first-test/*.conf
```

Si tout fonctionne bien, vous devriez avoir le même résultat qu'au premier test que nous avons effectuer (avec plus de logs)!

### 1.2 Fonctionnement de Logstash

#### 1.2.1 Arborescense des fichiers

Même s'il y a beaucoup plus de dossier que ça, voici les fichiers et dossier qui vont nous intéresser:

```
logstash-7.11.0
├── bin
├── conf
│   └── my-first-test
│       └── logstash.yml
├── config
│   ├── jvm.options
│   ├── log4j2.properties
│   ├── logstash.yml
│   ├── pipelines.yml
├── data2
│   ├── dead_letter_queue
│   ├── queue
│   └── uuid
├── logs
│   ├── logstash-deprecation.log
│   ├── logstash-plain.log
│   └── logstash-slowlog-plain.log
├── input
├── output
```

Le dossier:
- `bin` va contenir les fichiers binaires de Logstash, nous permettant, entre autre, de l'éxecuter
- `conf` va contenir, dans ses sous-dossiers, les configurations logstash que nous allons réaliser
- `config` est le dossier contenant toute la configuration. On peux noter, entre autre:
    - `jvm.options`: la configuration de Java
    - `log4j.properties`: la gestion des fichiers de logs de Logstash
    - `logstash.yml`: le fichier de configuration principal de Logstash
    - `pipelines.yml`: le fichier de configuration de pipelines Logstash (détaillé plus tard)
- `data`: Le dossier contenant les données temporaires internes Logstash
- `input`: Le dossier qui va contenir nos fichiers de données initiaux 
- `data`: Le dossier contenant nos données, une fois transformés

#### 1.2.2 Pipelines Logstash

Les pipelines sont une notion très importante: elles sont le coeur de Logstash, et ce sont elles qui vont permettre de recevoir des données, les transformer, et les transféré ailleurs.

Une pipeline peux contenir quatre types de module différents:

- Les **input**, permettant de **lire** les données. Dans l'exemple précédant, nous avons utilisé un [input stdin](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-stdin.html) -> ~ l'entrée utilisateur
- Les **filters**, non présent dans l'exemple précédent, qui vont permettre la **transformation** de la donnée
- Les **output**, qui vont nous permettre de transféré les données ailleurs. Dans l'exemple précédent, nous avons fait écrire Logstash sur l'[output stdout](https://www.elastic.co/guide/en/logstash/current/plugins-outputs-stdout.html) -> ~ la console
- Les **codecs**, qui vont permettre des transformation légères de données, utilisable seulement dans les **input** et **output**

Vous pouvez trouver, dans la [documentation Logstash](https://www.elastic.co/guide/en/logstash/current/index.html), la liste:

- des [inputs](https://www.elastic.co/guide/en/logstash/current/input-plugins.html)
- des [filters](https://www.elastic.co/guide/en/logstash/current/filter-plugins.html)
- des [outputs](https://www.elastic.co/guide/en/logstash/current/output-plugins.html)
- des [codces](https://www.elastic.co/guide/en/logstash/current/codec-plugins.html)

Dans un environement complexe, nous pouvons lancer de **multiples pipelines** en parralèles, d'où le fichier de configuration **pipelines.yml**, mais dans notre cas, nous utiliserons uniquement la ligne de commande, pour indiquer l'emplacement des configuration à traiter

Une pipeline peux contenir **plusieurs fichiers de configuration** (d'où le pattern que nous précisons en ligne de commande, `*.conf`). Si on utilise un pattern, les fichiers de configurations seront chargés séquentiellements, **par ordre alphabétique** -> leur ordre est important.

#### 1.2.3 Protocole de création d'une nouvelle pipeline

Pour chaque nouvel exercice, il va vous être demandé, pour créer une nouvelle pipeline:

- De créer le / les fichiers de données initiaux, à faire dans le dossier `input` (si nécessaire)
- De créer un nouveau dossier, qui correspondra au nom de votre pipeline, dans `conf` (et de mettre les fichiers de configuration Logstash dedans)
- De modifier la ligne de commande, utilisé lors du dernier test, pour pointer vers le bon dossier (`JAVA_HOME='' ./bin/logstash -f conf/<mon-dossier-pipeline>/*.conf`)

### 2. Exercices

#### 2.1 Exercice guidé

Nous allons nous intéressé au parsing d'un fichier de log nommé **auth.log**, présent dans presque toutes les distributions Linux, et qui correspond à la surveillance des utilisateurs, de leur authentification, et de leurs usage de privilèges.

Créons dans un premier temps notre jeux de donnée : le fichier `input/auth.log`, avec le contenu suivant:

```elixir
Apr  3 18:01:16 valentin-test sshd[13824]: Accepted publickey for ubuntu from 172.16.180.99 port 53332 ssh2: RSA ...
Apr 23 18:01:16 valentin-test sshd[13824]: pam_unix(sshd:session): session opened for user ubuntu by (uid=0)
Apr 23 18:02:25 valentin-test su[14053]: Successful su for root by root
Apr 23 18:02:25 valentin-test su[14053]: + /dev/pts/0 root:root
Apr 23 18:02:25 valentin-test su[14053]: pam_unix(su:session): session opened for user root by ubuntu(uid=0)
Apr 23 18:02:25 valentin-test su[14053]: pam_systemd(su:session): Cannot create session: Already running in a session
Apr 23 17:05:01 valentin-test CRON[13781]: pam_unix(cron:session): session opened for user root by (uid=0)
```

A partir de cet extrait de données, nous allons essayé de déterminer les **patterns**, ou **motifs**, qui se répètent.

En effet, la structure, au moins au début, est très similaire entre les différentes lignes (prenons example sur la première ligne):

> Apr 23 18&#5801&#5816 valentin-test sshd[13824]: Accepted publickey for ubuntu from 172.16.180.99 port 53332 ssh2: RSA ...

- Le premier motif est `Apr  3 18:01:16`, et correspond à une date, avec une heure
- Le second motif est `valentin-test`, une chaine de caractère
- Le troisième motif est `sshd`, une chaine de caractère
- Le quatrième motif est `13824`, un nombre, entouré de crochets
- La fin du message, après le caractère  `:`, varie et est ici `Accepted publickey for ubuntu from 172.16.180.99 port 53332 ssh2: RSA SHA256:3rzOXXM+dv3rtFQqjmyLUz2y0OjLbcYWrFeIEt2if+c`

Si nous créons un tableau (pour l'illustration), ces patterns sont très visibles:

| Motif 1 (date)  | Motif 2       | Motif 3 | Motif 4 (nombre) | Motif 5 (texte)                                                                                                          |
|-----------------|---------------|---------|------------------|--------------------------------------------------------------------------------------------------------------------------|
| Apr  3 18&#58;01&#58;16 | valentin-test | sshd    | 13824            | Accepted publickey for ubuntu from 172.16.180.99 port 53332 ssh2: RSA ... |
| Apr 23 18&#58;01&#58;16 | valentin-test | sshd    | 13824            | pam_unix(sshd:session): session opened for user ubuntu by (uid=0)                                                        |
| Apr 23 18&#58;02&#58;25 | valentin-test | su      | 14053            | Successful su for root by root                                                                                           |
| Apr 23 18&#58;02&#58;25 | valentin-test | su      | 14053            | + /dev/pts/0 root:root                                                                                                   |
| Apr 23 18&#58;02&#58;25 | valentin-test | su      | 14053            | pam_unix(su:session): session opened for user root by ubuntu(uid=0)                                                      |
| Apr 23 18&#58;02&#58;25 | valentin-test | su      | 14053            | pam_systemd(su:session): Cannot create session: Already running in a session                                             |
| Apr 23 17&#58;05&#58;01 | valentin-test | su      | 13781            | pam_unix(cron:session): session opened for user root by (uid=0)                                                          |


En l'occurence, il s'agit d'un format, dérivé du format de log [syslog](https://fr.wikipedia.org/wiki/Syslog#Le_format_Syslog), qui à le schéma suivant:

> date machine programme[process_id]: message

A partir de là, nous savons comment transformer la donnée : il suffit de répliquer ce concept, en langage compréhensible par Logstash!

Commencons déjà par créer la pipeline de Logstash:

```bash
mkdir -p conf/auth
```

**Input**

Dans un premier temps, nous allons dire à Logstash que nous voulons lire le fichier en question. Pour celà, nous allons utiliser l'[input file](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-file.html), qui permet de lire un fichier sur disque.

Avec quelques modifications, cela va nous donner:

```ruby
input {
    file {
        path => "<chemin complet>/input/auth.log"
        sincedb_path => "/dev/null"                                    
    }
}
```

**Filter**

La partie filtre, est très souvent le plus compliqué à faire. Dans ce cas là, cela va se traduire par ça:

```ruby
filter {
  
  grok {
    match => {
      "message" => ["%{SYSLOGTIMESTAMP:date} %{PROG:machine} %{WORD:programme}\[%{INT:pid}\]: %{GREEDYDATA:contenu}"]
    }
  }
  
  mutate {
    convert => {
      "pid" => "integer"
    }
  }
  
  date {
      match => [ "[date]", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss" ]
      target => "date"
  }
  
}
```

Les 3 filtres utilisés sont les plus courant, et sont utilisés dans la majorité des configurations:
    - le [grok](https://www.elastic.co/guide/en/logstash/current/plugins-filters-grok.html) va nous permettre de **découper** le message en morceaux (contenu, par défaut, dans le champs `message`). Il s'agit de ce que nous avons fait tout à l'heure
    - le [mutate](https://www.elastic.co/guide/en/logstash/current/plugins-filters-mutate.html) va nous permettre de convertir le **pid** du processus en nombre. En effet, le grok précédent n'interprette pas les données : pour lui, toutes les parties qu'il récupèrera seront considérés comme du texte
    - le [date](https://www.elastic.co/guide/en/logstash/current/plugins-filters-date.html) va permettre de standardiser le format de la date. Ce format de date est particulié, car il existe deux version différente, mais ils sont construit à partir de la définition dans la documentation du module. La date résultante (qui va écraser le format initial) sera sous format [ISO8601](https://fr.wikipedia.org/wiki/ISO_8601), un format nativement reconnu par Elasticsearch.


**Output**

La sortie sera tout aussi simple, nous allons écrire dans un fichier, avec un [codec](https://www.elastic.co/guide/en/logstash/current/codec-plugins.html) personnalisé ([rubydebug](https://www.elastic.co/guide/en/logstash/current/plugins-codecs-rubydebug.html)), afin que l'affichage soit un peu plus lisible:

```ruby
output {
    file {
        path => "<chemin complet>/output/auth-transforme.log"
        codec => rubydebug 
    }
}
```

**Résultats**

Une fois ces parties faites (vous pourrez réutiliser l'input & l'output pour les exercices prochains, en modifiant les chemins), nous allons pouvoir voir le résultat:

Créons le fichier `conf/auth/logstash.conf` avec pour contenu la concaténation de ces trois parties:

```ruby
input {
    file {
        path => "<chemin complet>/input/auth.log"
        sincedb_path => "/dev/null"
        start_position => "beginning"                              
    }
}

filter {
  
  grok {
    match => {
      "message" => ["%{SYSLOGTIMESTAMP:date} %{PROG:machine} %{WORD:programme}\[%{INT:pid}\]: %{GREEDYDATA:contenu}"]
    }
  }
  
  mutate {
    convert => {
      "pid" => "integer"
    }
  }
  
  date {
      match => [ "[date]", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss" ]
      target => "date"
  }
  
}

output {
    file {
        path => "<chemin complet>/output/auth-transforme.log"
        codec => rubydebug 
    }
}
```

Et lançons Logstash:

```bash
JAVA_HOME='' ./bin/logstash -f conf/auth/*.conf
```

Le résultat du fichier de destination, `output/auth-transforme.log`, devrait-être tel que [celui-ci](resources/tp-1/output_auth.md)

Le **@timestamp** et l'**host** seront différents, car ils correspondent respectivement à:

- la date d'ingestion par Logstash de la donnée
- la machine sur laquel l'ingestion à été effectuée

On peux également noté l'**absence de guillements** autour des valeurs des champs *date* et *pid*: cela signifie qu'ils ont bien été convertis, respectivement en date et en nombre, dans un format compréhensible par une base de donnée

#### 2.2 Logs multilines

Partons de l'exercice précédent : quelqu'un à créer un nouveau format de logs, basé sur celui de l'exercice précédent, mais avec un contenu pouvant s'étendre sur plusieurs lignes :

```elixir
Apr  3 18:01:16 valentin-test sshd[13824]: Accepted publickey for ubuntu from 172.16.180.99 port 53332 ssh2: 
  RSA key was accepted
Apr 23 18:01:16 valentin-test sshd[13824]: pam_unix(sshd:session): session opened for user ubuntu by (uid=0)
Apr 23 18:02:25 valentin-test su[14053]: Successful su for root by root
Apr 23 18:02:25 valentin-test su[14053]: + /dev/pts/0 root:root
Apr 23 18:02:25 valentin-test su[14053]: pam_unix(su:session): session opened:
  User is root, logged-in by ubuntu (uid=0)
Apr 23 18:02:25 valentin-test su[14053]: pam_systemd(su:session): Cannot create session: Already running in a session
Apr 23 17:05:01 valentin-test CRON[13781]: pam_unix(cron:session): session opened for user root by (uid=0)
```

Vous pouvez partir du **filtre précédent**, qui ne **demande pas de modification**. Néanmoins, il faudra faire une modification ailleurs ..
Si vous le tester sans modification, certains message auront un **tags** `_grokparsefailure`, signifiant qu'il y a eu un problème lors du **grok**.

> Aide: Le mot clé est dans le titre

#### 2.3 Apache access logs

Nouveau format de logs, il faudra donc construire le filtre depuis le début!

```elixir
83.149.9.216 - - [17/May/2015:10:05:03 +0000] "GET /presentations/logstash-monitorama-2013/images/kibana-search.png HTTP/1.1" 200 203023 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:43 +0000] "GET /presentations/logstash-monitorama-2013/images/kibana-dashboard3.png HTTP/1.1" 200 171717 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:47 +0000] "GET /presentations/logstash-monitorama-2013/plugin/highlight/highlight.js HTTP/1.1" 200 26185 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:12 +0000] "GET /presentations/logstash-monitorama-2013/plugin/zoom-js/zoom.js HTTP/1.1" 200 7697 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:07 +0000] "GET /presentations/logstash-monitorama-2013/plugin/notes/notes.js HTTP/1.1" 200 2892 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:34 +0000] "GET /presentations/logstash-monitorama-2013/images/sad-medic.png HTTP/1.1" 200 430406 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:57 +0000] "GET /presentations/logstash-monitorama-2013/css/fonts/Roboto-Bold.ttf HTTP/1.1" 200 38720 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:50 +0000] "GET /presentations/logstash-monitorama-2013/css/fonts/Roboto-Regular.ttf HTTP/1.1" 200 41820 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:24 +0000] "GET /presentations/logstash-monitorama-2013/images/frontend-response-codes.png HTTP/1.1" 200 52878 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:50 +0000] "GET /presentations/logstash-monitorama-2013/images/kibana-dashboard.png HTTP/1.1" 200 321631 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:46 +0000] "GET /presentations/logstash-monitorama-2013/images/Dreamhost_logo.svg HTTP/1.1" 200 2126 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:11 +0000] "GET /presentations/logstash-monitorama-2013/images/kibana-dashboard2.png HTTP/1.1" 200 394967 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:19 +0000] "GET /presentations/logstash-monitorama-2013/images/apache-icon.gif HTTP/1.1" 200 8095 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:33 +0000] "GET /presentations/logstash-monitorama-2013/images/nagios-sms5.png HTTP/1.1" 200 78075 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:00 +0000] "GET /presentations/logstash-monitorama-2013/images/redis.png HTTP/1.1" 200 25230 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:25 +0000] "GET /presentations/logstash-monitorama-2013/images/elasticsearch.png HTTP/1.1" 200 8026 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:59 +0000] "GET /presentations/logstash-monitorama-2013/images/logstashbook.png HTTP/1.1" 200 54662 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:30 +0000] "GET /presentations/logstash-monitorama-2013/images/github-contributions.png HTTP/1.1" 200 34245 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:53 +0000] "GET /presentations/logstash-monitorama-2013/css/print/paper.css HTTP/1.1" 200 4254 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:24 +0000] "GET /presentations/logstash-monitorama-2013/images/1983_delorean_dmc-12-pic-38289.jpeg HTTP/1.1" 200 220562 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:54 +0000] "GET /presentations/logstash-monitorama-2013/images/simple-inputs-filters-outputs.jpg HTTP/1.1" 200 1168622 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:33 +0000] "GET /presentations/logstash-monitorama-2013/images/tiered-outputs-to-inputs.jpg HTTP/1.1" 200 1079983 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:56 +0000] "GET /favicon.ico HTTP/1.1" 200 3638 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
24.236.252.67 - - [17/May/2015:10:05:40 +0000] "GET /favicon.ico HTTP/1.1" 200 3638 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0"
93.114.45.13 - - [17/May/2015:10:05:14 +0000] "GET /articles/dynamic-dns-with-dhcp/ HTTP/1.1" 200 18848 "http://www.google.ro/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&ved=0CCwQFjAB&url=http%3A%2F%2Fwww.semicomplete.com%2Farticles%2Fdynamic-dns-with-dhcp%2F&ei=W88AU4n9HOq60QXbv4GwBg&usg=AFQjCNEF1X4Rs52UYQyLiySTQxa97ozM4g&bvm=bv.61535280,d.d2k" "Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0"
93.114.45.13 - - [17/May/2015:10:05:04 +0000] "GET /reset.css HTTP/1.1" 200 1015 "http://www.semicomplete.com/articles/dynamic-dns-with-dhcp/" "Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0"
93.114.45.13 - - [17/May/2015:10:05:45 +0000] "GET /style2.css HTTP/1.1" 200 4877 "http://www.semicomplete.com/articles/dynamic-dns-with-dhcp/" "Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0"
93.114.45.13 - - [17/May/2015:10:05:14 +0000] "GET /favicon.ico HTTP/1.1" 200 3638 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0"
93.114.45.13 - - [17/May/2015:10:05:17 +0000] "GET /images/jordan-80.png HTTP/1.1" 200 6146 "http://www.semicomplete.com/articles/dynamic-dns-with-dhcp/" "Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0"
93.114.45.13 - - [17/May/2015:10:05:21 +0000] "GET /images/web/2009/banner.png HTTP/1.1" 200 52315 "http://www.semicomplete.com/style2.css" "Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0"
66.249.73.135 - - [17/May/2015:10:05:40 +0000] "GET /blog/tags/ipv6 HTTP/1.1" 200 12251 "-" "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
```

En vous servant de la [documentation logging apache](https://httpd.apache.org/docs/2.4/fr/mod/mod_log_config.html), essayer de trouver la structure, et la signification de toutes ces champs, puis réaliser le filter, et tester-le.

> Ne PAS utiliser le [grok pattern](https://www.elastic.co/guide/en/logstash/current/plugins-filters-grok.html#_description_129) `COMBINEDAPACHELOG`

#### 2.4 Data venant d'un CSV

Nous pouvons traiter de nombreux types de données avec Logstash, dont des [CSV](https://fr.wikipedia.org/wiki/Comma-separated_values)!

```
firstname,name,address,City,city_initials,city_postal_code
John,Doe,120 jefferson st.,Riverside, NJ,8075
Jack,McGinnis,220 hobo Av.,Phila, PA,9119
"John ""Da Man""",Repici,120 Jefferson St.,Riverside, NJ,8075
Stephen,Tyler,"7452 Terrace ""At the Plaza"" road",SomeTown,SD,91234
Michael,Blankman,3th road of JK,SomeTown, SD,298
"Joan ""the bone"", Anne",Jet,"9th, at Terrace plc",Desert City,CO,123
```

Réaliser le filter, et tester

#### 2.5 JSON logs

Nous avons maintenant des logs web, dans un format [JSON](https://fr.wikipedia.org/wiki/JavaScript_Object_Notation).

```json
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.738Z","bytes":203023,"message":"83.149.9.216 - - [17/May/2015:10:05:03 +0000] \"GET /presentations/logstash-monitorama-2013/images/kibana-search.png HTTP/1.1\" 200 203023 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:03.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/images/kibana-search.png","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.742Z","bytes":171717,"message":"83.149.9.216 - - [17/May/2015:10:05:43 +0000] \"GET /presentations/logstash-monitorama-2013/images/kibana-dashboard3.png HTTP/1.1\" 200 171717 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:43.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/images/kibana-dashboard3.png","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.742Z","bytes":26185,"message":"83.149.9.216 - - [17/May/2015:10:05:47 +0000] \"GET /presentations/logstash-monitorama-2013/plugin/highlight/highlight.js HTTP/1.1\" 200 26185 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:47.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/plugin/highlight/highlight.js","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.742Z","bytes":7697,"message":"83.149.9.216 - - [17/May/2015:10:05:12 +0000] \"GET /presentations/logstash-monitorama-2013/plugin/zoom-js/zoom.js HTTP/1.1\" 200 7697 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:12.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/plugin/zoom-js/zoom.js","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.743Z","bytes":2892,"message":"83.149.9.216 - - [17/May/2015:10:05:07 +0000] \"GET /presentations/logstash-monitorama-2013/plugin/notes/notes.js HTTP/1.1\" 200 2892 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:07.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/plugin/notes/notes.js","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.743Z","bytes":430406,"message":"83.149.9.216 - - [17/May/2015:10:05:34 +0000] \"GET /presentations/logstash-monitorama-2013/images/sad-medic.png HTTP/1.1\" 200 430406 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:34.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/images/sad-medic.png","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.743Z","bytes":38720,"message":"83.149.9.216 - - [17/May/2015:10:05:57 +0000] \"GET /presentations/logstash-monitorama-2013/css/fonts/Roboto-Bold.ttf HTTP/1.1\" 200 38720 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:57.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/css/fonts/Roboto-Bold.ttf","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.743Z","bytes":41820,"message":"83.149.9.216 - - [17/May/2015:10:05:50 +0000] \"GET /presentations/logstash-monitorama-2013/css/fonts/Roboto-Regular.ttf HTTP/1.1\" 200 41820 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:50.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/css/fonts/Roboto-Regular.ttf","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.744Z","bytes":52878,"message":"83.149.9.216 - - [17/May/2015:10:05:24 +0000] \"GET /presentations/logstash-monitorama-2013/images/frontend-response-codes.png HTTP/1.1\" 200 52878 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:24.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/images/frontend-response-codes.png","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.744Z","bytes":321631,"message":"83.149.9.216 - - [17/May/2015:10:05:50 +0000] \"GET /presentations/logstash-monitorama-2013/images/kibana-dashboard.png HTTP/1.1\" 200 321631 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:50.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/images/kibana-dashboard.png","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.744Z","bytes":2126,"message":"83.149.9.216 - - [17/May/2015:10:05:46 +0000] \"GET /presentations/logstash-monitorama-2013/images/Dreamhost_logo.svg HTTP/1.1\" 200 2126 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:46.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/images/Dreamhost_logo.svg","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.744Z","bytes":394967,"message":"83.149.9.216 - - [17/May/2015:10:05:11 +0000] \"GET /presentations/logstash-monitorama-2013/images/kibana-dashboard2.png HTTP/1.1\" 200 394967 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:11.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/images/kibana-dashboard2.png","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.745Z","bytes":8095,"message":"83.149.9.216 - - [17/May/2015:10:05:19 +0000] \"GET /presentations/logstash-monitorama-2013/images/apache-icon.gif HTTP/1.1\" 200 8095 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:19.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/images/apache-icon.gif","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.745Z","bytes":78075,"message":"83.149.9.216 - - [17/May/2015:10:05:33 +0000] \"GET /presentations/logstash-monitorama-2013/images/nagios-sms5.png HTTP/1.1\" 200 78075 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:33.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/images/nagios-sms5.png","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.745Z","bytes":25230,"message":"83.149.9.216 - - [17/May/2015:10:05:00 +0000] \"GET /presentations/logstash-monitorama-2013/images/redis.png HTTP/1.1\" 200 25230 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:00.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/images/redis.png","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.745Z","bytes":8026,"message":"83.149.9.216 - - [17/May/2015:10:05:25 +0000] \"GET /presentations/logstash-monitorama-2013/images/elasticsearch.png HTTP/1.1\" 200 8026 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:25.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/images/elasticsearch.png","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.746Z","bytes":54662,"message":"83.149.9.216 - - [17/May/2015:10:05:59 +0000] \"GET /presentations/logstash-monitorama-2013/images/logstashbook.png HTTP/1.1\" 200 54662 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:59.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/images/logstashbook.png","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.746Z","bytes":34245,"message":"83.149.9.216 - - [17/May/2015:10:05:30 +0000] \"GET /presentations/logstash-monitorama-2013/images/github-contributions.png HTTP/1.1\" 200 34245 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:30.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/images/github-contributions.png","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.746Z","bytes":4254,"message":"83.149.9.216 - - [17/May/2015:10:05:53 +0000] \"GET /presentations/logstash-monitorama-2013/css/print/paper.css HTTP/1.1\" 200 4254 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:53.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/css/print/paper.css","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.746Z","bytes":220562,"message":"83.149.9.216 - - [17/May/2015:10:05:24 +0000] \"GET /presentations/logstash-monitorama-2013/images/1983_delorean_dmc-12-pic-38289.jpeg HTTP/1.1\" 200 220562 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:24.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/images/1983_delorean_dmc-12-pic-38289.jpeg","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.746Z","bytes":1168622,"message":"83.149.9.216 - - [17/May/2015:10:05:54 +0000] \"GET /presentations/logstash-monitorama-2013/images/simple-inputs-filters-outputs.jpg HTTP/1.1\" 200 1168622 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:54.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/images/simple-inputs-filters-outputs.jpg","host":"localhost","ident":"-"}
{"referrer":"\"http://semicomplete.com/presentations/logstash-monitorama-2013/\"","@timestamp":"2021-02-17T08:07:01.747Z","bytes":1079983,"message":"83.149.9.216 - - [17/May/2015:10:05:33 +0000] \"GET /presentations/logstash-monitorama-2013/images/tiered-outputs-to-inputs.jpg HTTP/1.1\" 200 1079983 \"http://semicomplete.com/presentations/logstash-monitorama-2013/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:33.000Z","auth":"-","httpversion":1.1,"request":"/presentations/logstash-monitorama-2013/images/tiered-outputs-to-inputs.jpg","host":"localhost","ident":"-"}
{"referrer":"\"-\"","@timestamp":"2021-02-17T08:07:01.747Z","bytes":3638,"message":"83.149.9.216 - - [17/May/2015:10:05:56 +0000] \"GET /favicon.ico HTTP/1.1\" 200 3638 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","@version":"1","clientip":"83.149.9.216","agent":"\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:56.000Z","auth":"-","httpversion":1.1,"request":"/favicon.ico","host":"localhost","ident":"-"}
{"referrer":"\"-\"","@timestamp":"2021-02-17T08:07:01.747Z","bytes":3638,"message":"24.236.252.67 - - [17/May/2015:10:05:40 +0000] \"GET /favicon.ico HTTP/1.1\" 200 3638 \"-\" \"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0\"","@version":"1","clientip":"24.236.252.67","agent":"\"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:40.000Z","auth":"-","httpversion":1.1,"request":"/favicon.ico","host":"localhost","ident":"-"}
{"referrer":"\"http://www.google.ro/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&ved=0CCwQFjAB&url=http%3A%2F%2Fwww.semicomplete.com%2Farticles%2Fdynamic-dns-with-dhcp%2F&ei=W88AU4n9HOq60QXbv4GwBg&usg=AFQjCNEF1X4Rs52UYQyLiySTQxa97ozM4g&bvm=bv.61535280,d.d2k\"","@timestamp":"2021-02-17T08:07:01.747Z","bytes":18848,"message":"93.114.45.13 - - [17/May/2015:10:05:14 +0000] \"GET /articles/dynamic-dns-with-dhcp/ HTTP/1.1\" 200 18848 \"http://www.google.ro/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&ved=0CCwQFjAB&url=http%3A%2F%2Fwww.semicomplete.com%2Farticles%2Fdynamic-dns-with-dhcp%2F&ei=W88AU4n9HOq60QXbv4GwBg&usg=AFQjCNEF1X4Rs52UYQyLiySTQxa97ozM4g&bvm=bv.61535280,d.d2k\" \"Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0\"","@version":"1","clientip":"93.114.45.13","agent":"\"Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:14.000Z","auth":"-","httpversion":1.1,"request":"/articles/dynamic-dns-with-dhcp/","host":"localhost","ident":"-"}
{"referrer":"\"http://www.semicomplete.com/articles/dynamic-dns-with-dhcp/\"","@timestamp":"2021-02-17T08:07:01.747Z","bytes":1015,"message":"93.114.45.13 - - [17/May/2015:10:05:04 +0000] \"GET /reset.css HTTP/1.1\" 200 1015 \"http://www.semicomplete.com/articles/dynamic-dns-with-dhcp/\" \"Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0\"","@version":"1","clientip":"93.114.45.13","agent":"\"Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:04.000Z","auth":"-","httpversion":1.1,"request":"/reset.css","host":"localhost","ident":"-"}
{"referrer":"\"http://www.semicomplete.com/articles/dynamic-dns-with-dhcp/\"","@timestamp":"2021-02-17T08:07:01.747Z","bytes":4877,"message":"93.114.45.13 - - [17/May/2015:10:05:45 +0000] \"GET /style2.css HTTP/1.1\" 200 4877 \"http://www.semicomplete.com/articles/dynamic-dns-with-dhcp/\" \"Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0\"","@version":"1","clientip":"93.114.45.13","agent":"\"Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:45.000Z","auth":"-","httpversion":1.1,"request":"/style2.css","host":"localhost","ident":"-"}
{"referrer":"\"-\"","@timestamp":"2021-02-17T08:07:01.748Z","bytes":3638,"message":"93.114.45.13 - - [17/May/2015:10:05:14 +0000] \"GET /favicon.ico HTTP/1.1\" 200 3638 \"-\" \"Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0\"","@version":"1","clientip":"93.114.45.13","agent":"\"Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:14.000Z","auth":"-","httpversion":1.1,"request":"/favicon.ico","host":"localhost","ident":"-"}
{"referrer":"\"http://www.semicomplete.com/articles/dynamic-dns-with-dhcp/\"","@timestamp":"2021-02-17T08:07:01.748Z","bytes":6146,"message":"93.114.45.13 - - [17/May/2015:10:05:17 +0000] \"GET /images/jordan-80.png HTTP/1.1\" 200 6146 \"http://www.semicomplete.com/articles/dynamic-dns-with-dhcp/\" \"Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0\"","@version":"1","clientip":"93.114.45.13","agent":"\"Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:17.000Z","auth":"-","httpversion":1.1,"request":"/images/jordan-80.png","host":"localhost","ident":"-"}
{"referrer":"\"http://www.semicomplete.com/style2.css\"","@timestamp":"2021-02-17T08:07:01.748Z","bytes":52315,"message":"93.114.45.13 - - [17/May/2015:10:05:21 +0000] \"GET /images/web/2009/banner.png HTTP/1.1\" 200 52315 \"http://www.semicomplete.com/style2.css\" \"Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0\"","@version":"1","clientip":"93.114.45.13","agent":"\"Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:21.000Z","auth":"-","httpversion":1.1,"request":"/images/web/2009/banner.png","host":"localhost","ident":"-"}
{"referrer":"\"-\"","@timestamp":"2021-02-17T08:07:01.748Z","bytes":12251,"message":"66.249.73.135 - - [17/May/2015:10:05:40 +0000] \"GET /blog/tags/ipv6 HTTP/1.1\" 200 12251 \"-\" \"Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)\"","@version":"1","clientip":"66.249.73.135","agent":"\"Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)\"","verb":"GET","response":200,"timestamp":"2015-05-17T10:05:40.000Z","auth":"-","httpversion":1.1,"request":"/blog/tags/ipv6","host":"localhost","ident":"-"}
```

Même processus.

### 3. Questions ouvertes

Qui seront discutés à la fin du tp:

- Est-ce que la transformation des données est simple ?
- Les données de l'exercice 2.2 et 2.4 sont les mêmes : lesquelles sont plus simple à traiter ? et pourquoi ?
- Vaut-il mieux formatter ses logs dans une application elle-même, ou à postériori, dans un phase de transformation ?