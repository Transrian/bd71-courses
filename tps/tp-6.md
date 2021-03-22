# Rollups (2h)

Maintenant que nous avons vu les bases de la visualisations de données, et l'utilisation du machine learning sur nos données, nous allons nous intéresser à une autre problématique, le stockage des données, ou plus précisément, comment réduire la volumétrie des données.

## 1. Contexte

Prenons un cas fictif.

> Vous avez **mis en place un clusteur Elasticsearch** pour stocker les logs d'une de vos applications, et celles-ci sont visualisables à travers Kibana. Vous stocker **les logs de celle-ci 1 mois**, et tout fonctionne bien. Néanmoins, votre chef souhaite que vous stockiez les **données 1 an**, pour que vous puissiez voir l'**évolution** dans le temps de celles-ci, ainsi que les impacts qu'on eu les montées de version.

La problématique soulevée ici est toute simple : si vous avez la place, ce n'est pas un problème (x12 par rapport au besoin initial), mais si ce n'est pas le cas, à part accroître les disques ou augmenter le nombre d'instances ; vous êtes dans une impasse.

Il est **très rare** de devoir stocker les logs plus de 1 mois. En effet, à moins que ça soit justifié par des **contraintes légales**, le plus souvent, ce qui nous intéresse sont justes les **KPIs** affichés par Kibana.

Par défaut, avec Kibana, ils sont **calculés dynamiquement** (à partir des données brut), comme une moyenne, ou une somme. Néanmoins, il est possible de faire autrement!

Dans Elasticsearch, il existe deux moyens d'aggréger les données déjà existantes : avec des [transform](https://www.elastic.co/guide/en/elasticsearch/reference/current/transforms.html), et des [rollups](https://www.elastic.co/guide/en/elasticsearch/reference/current/xpack-rollup.html). C'est cette dernière méthode qui va nous intéresser ici.

Ci-dessous une traduction de leur [page de description](https://www.elastic.co/guide/en/elasticsearch/reference/current/xpack-rollup.html) de la fonctionnalité, très pertinente:

> Garder les données historiques pour réaliser des analyses est très utiles, mais souvent évité à cause du haut coup de stockage (à cause de l'archivage de toutes ces données). Les périodes de retentions sont alors définies pour des raisons financières, plutôt que par des raisons d'utilité des données.
> 
> La fonction Data Rollup fourni un moyen de résumé et stocker des données historiques, pour qu'elles puissent-être utiliser dans les analyses, mais à une fraction du coup de stockage des données bruts.

## 2. Cas concret

## 2.1 Jeu de données

Comme nous devons avoir un jeu de données relativement conséquent en taille, nous allons utiliser l'historique des prenom en France, par département, de 1900 à 2019.

> Pour les personnes utilisant le clusteur de BD71, aucun import des données n'est nécessaire, utiliser l'index `prenoms-france`, vous pouvez directement passer au point 2.2

Les données sont téléchargeables à cette adresse: https://www.insee.fr/fr/statistiques/fichier/2540004/dpt2019_csv.zip ([page d'origine](https://www.insee.fr/fr/statistiques/2540004?sommaire=4767262))

Télécharger et dézipper le fichier zip, et vous devriez avoir un fichier CSV d'environ 70Mb.

> Il faudra environ 140Mo de disque libre sur le clusteur Elasticsearch

Ensuite, importer les données à l'aide du pannel dans le machine learning (comme pour le TP précédent), et dans la partie **Override settings**, copié les paramètres ci-dessous:

![custom settings prenoms](images/override_settings_prenoms.png)

Une fois valider, et passer à la page suivante, vous allez vous mettre en mode **Advanced**, et faire deux choses supplémentaires (le département est considéré comme un nombre, mais cela devrait-être une chaine). Comme sur l'image suivante:

![advanced import prenoms](images/advanced_import_prenoms.png)

Il faut:

- Changer le mapping du champs `departement` de **long** à **string** (partie surligné sur le bloc central)
- Supprimer de la partie **Ingest pipeline** le **convert du champs ``departement`` en ``long``** (partie surlignée sur le bloc de droite)

Une fois l'import lancé (vous devriez avoir des erreurs, due à des erreurs dans le fichier d'origine), l'index pattern sera créer, et vous n'avez plus qu'à passer à l'étape suivante!

## 2.2 Structure du jeu de données

Si vous regarder les données sur **100 ans**, dans le discover (après avoir créer l'index pattern pour l'index `prenoms-france`), vous pouvez voir beaucoup de données (~ 3 millions).

Ce jeu de données contient les données **annuelles des prénoms donnés aux nouveaux-nés, par départements**

Néanmoins, la **structure** de celles-ci est toute simple:

| Champ       | Signification                                                            |
|-------------|--------------------------------------------------------------------------|
| departement | Numero du département                                                    |
| @timestamp  | Date (équivaut à l'année)                                                |
| sexe        | Sexe (1 = masculin, 2 = feminin)                                         |
| annee       | Année (sous forme de texte)                                              |
| prenom      | Prénom                                                                   |
| nombre      | Nombre de fois que le prénom à été donné dans ce département cette année |

C'est un bonne exemple de ce que l'on peut trouver dans le monde de l'entreprise : des **données simples**, mais avec une **grosse volumétrie**