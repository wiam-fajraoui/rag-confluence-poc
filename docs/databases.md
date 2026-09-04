# Bases de données

## Présentation

Une base de données permet de stocker, organiser et retrouver des informations de manière fiable.

Les applications modernes utilisent une base de données pour conserver les données des utilisateurs, les produits, les commandes, les journaux ou toute autre information persistante.

Une base de données est généralement administrée par un système appelé SGBD, ou Système de Gestion de Base de Données.

---

## Les bases de données relationnelles

Les bases de données relationnelles organisent les données sous forme de tables.

Chaque table contient des lignes et des colonnes.

Les tables peuvent être reliées entre elles grâce à des relations.

Quelques bases de données relationnelles populaires sont :

- PostgreSQL
- MySQL
- MariaDB
- Microsoft SQL Server
- Oracle Database

---

## Les bases de données NoSQL

Les bases de données NoSQL utilisent d'autres modèles de stockage.

Selon le besoin, elles peuvent stocker :

- des documents ;
- des paires clé-valeur ;
- des graphes ;
- des colonnes.

Quelques exemples :

- MongoDB
- Redis
- Cassandra
- Neo4j

Les bases NoSQL sont souvent utilisées lorsque les données évoluent rapidement ou lorsque les volumes sont très importants.

---

## Les tables

Une table représente un ensemble de données du même type.

Par exemple :

- utilisateurs ;
- produits ;
- commandes ;
- clients.

Chaque ligne représente un enregistrement.

Chaque colonne représente une propriété.

---

## Les clés primaires

Chaque ligne possède généralement une clé primaire.

La clé primaire identifie de manière unique un enregistrement.

Elle est souvent constituée d'un entier ou d'un identifiant unique.

---

## Les clés étrangères

Une clé étrangère permet de relier deux tables.

Par exemple, une commande peut contenir l'identifiant du client qui l'a passée.

Les clés étrangères assurent la cohérence des données.

---

## Les requêtes SQL

SQL est le langage utilisé pour interroger les bases de données relationnelles.

Les principales opérations sont :

- SELECT
- INSERT
- UPDATE
- DELETE

SQL permet également de créer et modifier les tables.

---

## Les index

Un index accélère la recherche des données.

Sans index, la base doit parcourir toutes les lignes d'une table.

Avec un index, les recherches deviennent beaucoup plus rapides.

En contrepartie, les index occupent de l'espace supplémentaire et ralentissent légèrement les opérations d'écriture.

---

## Les transactions

Une transaction regroupe plusieurs opérations.

Toutes les opérations doivent réussir.

Si une erreur survient, la transaction est annulée.

Les transactions garantissent la cohérence des données.

---

## Les propriétés ACID

Les bases de données relationnelles respectent généralement les propriétés ACID.

Ces propriétés garantissent :

- l'atomicité ;
- la cohérence ;
- l'isolation ;
- la durabilité.

Elles assurent la fiabilité des transactions.

---

## Les sauvegardes

Les sauvegardes permettent de restaurer une base de données après une panne.

Les sauvegardes doivent être réalisées régulièrement.

Elles peuvent être complètes ou incrémentales.

---

## La réplication

La réplication consiste à copier automatiquement les données sur plusieurs serveurs.

Elle améliore :

- la disponibilité ;
- la tolérance aux pannes ;
- les performances en lecture.

---

## La haute disponibilité

Une base de données peut être installée sur plusieurs serveurs.

En cas de panne d'un serveur, un autre prend automatiquement le relais.

Cette approche réduit les interruptions de service.

---

## Les performances

Les performances dépendent notamment :

- des index ;
- de la qualité des requêtes ;
- de la mémoire disponible ;
- du processeur ;
- du stockage.

Une mauvaise conception peut ralentir fortement une application.

---

## PostgreSQL

PostgreSQL est une base de données relationnelle open source.

Elle est réputée pour sa robustesse, ses performances et sa conformité aux standards SQL.

Elle est largement utilisée dans les applications professionnelles.

---

## MySQL

MySQL est également une base de données relationnelle très populaire.

Elle est souvent utilisée pour les applications web.

MariaDB est une alternative compatible avec MySQL.

---

## MongoDB

MongoDB est une base de données orientée documents.

Les données sont stockées sous forme de documents JSON.

Cette approche offre une grande flexibilité lorsque la structure des données évolue.

---

## Redis

Redis est une base de données en mémoire.

Elle est principalement utilisée comme cache.

Redis améliore considérablement les performances des applications.

---

## Bases de données et Docker

Les bases de données peuvent être exécutées dans des conteneurs Docker.

Les volumes permettent de conserver les données même après la suppression du conteneur.

Cette approche est très utilisée en développement.

---

## Bases de données et Kubernetes

Kubernetes peut exécuter des bases de données grâce aux Persistent Volumes.

Les StatefulSets sont souvent utilisés pour gérer les applications ayant besoin d'un stockage persistant.

---

## Bases de données et Azure

Microsoft Azure propose plusieurs services de bases de données managés.

Parmi les principaux :

- Azure SQL Database ;
- Azure Database for PostgreSQL ;
- Azure Database for MySQL ;
- Azure Cosmos DB.

Ces services simplifient l'administration des bases de données.

---

## Bonnes pratiques

Il est recommandé de :

- utiliser des index lorsque cela est nécessaire ;
- sauvegarder régulièrement les données ;
- protéger les accès à la base ;
- limiter les droits des utilisateurs ;
- surveiller les performances ;
- tester régulièrement les restaurations.

---

## Résumé

Une base de données permet de stocker durablement les informations d'une application.

Les principaux concepts à retenir sont :

- les bases relationnelles utilisent des tables ;
- SQL permet d'interroger les données ;
- les index accélèrent les recherches ;
- les transactions garantissent la cohérence ;
- PostgreSQL et MySQL sont des bases relationnelles populaires ;
- MongoDB est une base orientée documents ;
- Redis est principalement utilisé comme cache ;
- Docker, Kubernetes et Azure proposent des solutions pour héberger des bases de données.