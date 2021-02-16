# Base de connaissance Linux

Linux est basé en lignes de commandes, et vous allez probablement devoir utiliser certaines commandes pour lancer des processus, modifier des fichier de configurations, etc.

## Architecture des répertoires

Exemple de chemin de fichier sur Linux:

> /var/log/apache/access.log

Quand nous **séparons** le chemin en morceaux, nous avons:
- le `/` au début est le répertoire racine, tous les chemins absolu commencent par lui
- `/var/log/apache` est le nom du répertoire
- `access.log` est le nom complet du fichier
  - `access` est le nom du fichier
  - `log` est l'extension du fichier -> dans ce cas, il s'agit d'un fichier de log

Pour toutes les commandes, un **chemin peut-être absolu ou relatif**:
- **absolu**: il s'agit du chemin complet vers l'élément
    - ex: `/var/log/apache/access.log`
- **relatif**: le chemin est relatif au répertoire dans lequel nous nous trouvons
    - ex: si nous sommes dans `/var/log`, le fichier `apache/access.log` est valide

**Répertoires & caractères spéciaux**:
- `.` est *le répertoire actuel*
- `..` est *le répertoire parent*
  - Pour le répertoire `/var/log/apache`, le répertoire parent est `/var/log`
- `*` est un pattern qui correspond à tous les fichiers & répertoires
  - A partir de celui-ci, on peux construire des patterns spéciaux. Par exemple, tous les fichiers de logs : `*.log`

## Commandes système

### Processus

```bash
# Afficher tous les processus actifs
ps -eaf

# Tuer un processus en se servant d'un PID
kill -9 process_pid

# Voir la documentation d'un programme
man my_command
```

### Opérateur barre vertical

Le caractère **barre vertical** `|` est un caractère spécial, très utilisé dans le monde Linux. Il va vous permettre de **rediriger la sortie d'une commande vers une autre**, pour faire des modifications sur celle-ci, par exemple.

**Exemples**:

```bash
# Afficher le fichier access.log, et filter pour afficher seulement les lignes contenant le mot 'INFO'
cat access.log | grep "INFO"

# On peux aussi les cumuler!
# Affichage des logs contenant le mot 'ERRORR', mais pas le mot 'CONNECTION'
cat access.log | grep "ERROR" | grep -v "CONNECTION"
```


### Répertoires

```bash
# Aller dans le répertoire en question
cd /var/log/apache

# Afficher le répertoire actuel
pwd

# Aller dans le répertoire parent
cd ..

# Créer un répertoire
mkdir apache

# Supprimer un répertoire VIDE
rmdir apache

# Afficher les fichiers et répertoires dans le répertoire actuel
ls

# Afficher les fichiers et répertoires dans le répertoire actuel avec plus d'informations
ls -altrh

# Afficher les fichiers de logs (avec l'extension '.log')
ls *.log

# Afficher l'arborescense de fichier comme un arbre
tree .
```

## Fichiers

```bash
# Créer un fichier vide
touch empty.log

# Modifier un fichier, d'autres commandes sont possibles : vim, emac, ..
nano access.log

# Afficher le contenu d'un fichier
cat access.log

# Afficher un fichier en mode tabulé
less access.log

# Afficher un fichier avec une mise à jour en temps réel
tail -f access.log
```

## Fichier & répertoires

Fonctionne pour les fichiers et répertoires

```bash
# Déplacer un fichier ou répertoire
mv my_file new_filename

# Copier un fichier ou répertoire
cp my_file new_copied_filename

# Supprimer un fichier ou répertoire
rm -r things_to_delete
```

## Web

```bash
# Télécharger un fichier et l'écrire sur disque
wget https://artifacts.elastic.co/downloads/logstash/logstash-7.11.0-linux-x86_64.tar.gz -O logstash.tar.gz

# Avoir la réponse d'un API authentifié par ligne de commande
curl -k -u username:password https://localhost:9200
```

## Chaînes de caractères

Comme vous avez pu le voir, aucune des chaînes de caractère dans les exemples ne contiennent d'espaces.

En effet, par défaut, une chaîne de caractère ne contient pas d'espace sous Linux.

Si vous voulez qu'elle en contienne, il va falloir l'entourer des caractères guillemet double (`"`) ou guillement simple(`'`)

```bash
echo "Bonjour, comment allez-vous ?"
```

## Autres

```bash
# Compresser des fichiers et répertoires dans une archive
tar -zxvf target_archive.tar.gz file1 file2 dir1 dir2

# Décompresser une archive .tar.gz
tar -zxvf my_archive.tar.gz
```