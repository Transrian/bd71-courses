# Base de connaissance Linux

Linux est basé en lignes de commandes, et vous allez probablement devoir utiliser certaines commandes pour lancer des processus, modifier des fichier de configurations, etc.

## Architecture des répertoires

Exemple de chemin de fichier sur Linux:

> /var/log/apache/access.log:

When we **split this path**, we got:
- the `/` at the start is the root directory, every path start with it
- `/var/log/apache` is the name of the directory
- `access.log` is the filename (except some rare cases, directory don't have a prefix)
  - `access` is the name of the file
  - `log` is the extension of the file -> in this case, mean it's a log file

For all those command, **a path can either be**:
- **absolute**: that mean the full path to an element
    - eg: `/var/log/apache/access.log`
- **relative**: the path is relative to the directory we are in now
    - eg: if we are in `/var/log`, `apache/access.log` is valid

**Special directories and patterns**:
- `.` is *current directory*
- `..` is the *upper directory*
  - For `/var/log/apache`, upper directory is `/var/log`
- `*` match all files and directories, and is called wildcard
  - From there, you can build custom patterns. Eg, to see all log files : `*.log`

## System command

### System

```bash
# Afficher tous les processus actifs
ps -eaf

# Tuer un processus en se servant d'un PID
kill -9 process_pid

# Voir la documentation d'un programme
man my_command
```

### Pipe

Le caractère **barre vertical** `|` est un caractère spécial, très utilisé dans le monde Linux. Il va vous permettre de **rediriger la sortie d'une commande vers une autre**, pour faire des modifications sur celle-ci, par exemple.

**Exemples**:

```bash
# Afficher le fichier access.log, et filter pour afficher seulement les lignes contenant le mot 'INFO'
cat access.log | grep "INFO"

# On peux aussi les cumuler!
# Affichage des logs contenant le mot 'ERRORR', mais pas le mot 'CONNECTION'
cat access.log | grep "ERROR" | grep -v "CONNECTION"
```


### Directories

```bash
# Go into a directory
cd /var/log/apache

# Know in which directory we are
pwd

# Go back into upper directory
# If we are in /var/log/apache, we will go to /var/log
cd ..

# Create a directory
mkdir apache

# Delete an empty directory
rmdir apache

# Edit a file, lots of binary available: nano, vim, emac, ..
nano apache/access.log

# Display the files and directories in current directory
ls

# Display the files and directories in current directories with more infos
ls -altrh

# Display files ending with ".log" extension
ls *.log

# Display current arborescense as a tree
tree .

# Create an empty file
touch empty.log
```

## File

```bash
# Create an empty file
touch empty.log

# Edit a file, lots of program available: nano, vim, emac, ..
nano access.log

# Display a file content
cat access.log

# Afficher un fichier en mode tabulé
less access.log

# Display a file that is updating in real time
tail -f access.log
```

## Mixed

Applicable for both files and directories

```bash
# Move a file
mv my_file new_filename

# Copy a file
mv my_file new_copied_filename

# Delete files and directories
rm -r things_to_delete
```

## Web related command

```bash
# Download a file from http & write it to disk
wget https://artifacts.elastic.co/downloads/logstash/logstash-7.11.0-linux-x86_64.tar.gz -O logstash.tar.gz

# Get answer from an API from command line
curl -k -u username:password https://localhost:9200
```