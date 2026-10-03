# Docker

## Présentation

Docker est une plateforme de conteneurisation permettant de créer, distribuer et exécuter des applications dans des conteneurs.

Un conteneur regroupe une application avec toutes les bibliothèques et dépendances nécessaires à son fonctionnement. Ainsi, une application peut être exécutée de manière identique sur différents environnements.

Docker simplifie le développement, les tests et le déploiement des applications.

---

## Architecture Docker

L'architecture Docker est composée de plusieurs éléments.

Le Docker Engine est le moteur qui exécute les conteneurs.

Le Docker Daemon est un service qui gère les images, les conteneurs, les réseaux et les volumes.

Le Docker CLI est l'interface en ligne de commande utilisée pour communiquer avec le Docker Daemon.

Les images Docker sont généralement stockées dans un registre comme Docker Hub.

---

## Les images Docker

Une image Docker est un modèle en lecture seule utilisé pour créer un conteneur.

Une image contient le système d'exploitation, les bibliothèques et l'application.

Les images sont créées à partir d'un Dockerfile.

Une image peut être identifiée par un nom et une version, appelés tag.

Exemples :

- python:3.12
- ubuntu:24.04
- nginx:latest

---

## Dockerfile

Un Dockerfile est un fichier texte décrivant les étapes nécessaires à la construction d'une image.

Il contient différentes instructions comme :

- FROM
- WORKDIR
- COPY
- RUN
- CMD

Après avoir créé un Dockerfile, une image peut être construite avec la commande :

docker build -t mon-api .

---

## Les conteneurs

Un conteneur est une instance d'une image Docker.

Plusieurs conteneurs peuvent être créés à partir d'une même image.

Chaque conteneur possède son propre système de fichiers, ses processus et sa configuration.

Commandes courantes :

docker run nginx

docker ps

docker stop <container_id>

docker rm <container_id>

---

## Docker Hub

Docker Hub est un registre public permettant de télécharger ou publier des images Docker.

Il contient des milliers d'images officielles et communautaires.

Exemple :

docker pull nginx

---

## Docker Compose

Docker Compose permet de lancer plusieurs conteneurs en même temps.

Les services sont décrits dans un fichier nommé docker-compose.yml.

Chaque service représente généralement une application ou une base de données.

Docker Compose est particulièrement utile pour les applications composées de plusieurs services.

Commandes principales :

docker compose up

docker compose down

docker compose ps

---

## Les volumes

Les volumes permettent de conserver les données même après la suppression d'un conteneur.

Ils sont principalement utilisés pour les bases de données et les fichiers persistants.

Commande :

docker volume create data

---

## Les réseaux

Docker crée automatiquement un réseau permettant aux conteneurs de communiquer entre eux.

Il est également possible de créer des réseaux personnalisés.

Commande :

docker network create backend

---

## Les variables d'environnement

Les variables d'environnement permettent de configurer une application sans modifier son code.

Elles sont souvent utilisées pour définir :

- les ports
- les mots de passe
- les URL des bases de données
- le mode de fonctionnement de l'application

Exemple :

docker run -e ENV=production mon-api

---

## Les logs

Docker permet de consulter les journaux d'un conteneur afin de diagnostiquer un problème.

Commande :

docker logs <container_id>

---

## Gestion des conteneurs

Docker permet également de redémarrer, suspendre ou supprimer un conteneur.

Quelques commandes utiles :

docker start <container_id>

docker restart <container_id>

docker pause <container_id>

docker unpause <container_id>

---

## Bonnes pratiques

Pour utiliser Docker efficacement, il est recommandé de :

- utiliser des images officielles lorsqu'elles existent ;
- privilégier des images légères ;
- utiliser des versions explicites plutôt que le tag latest ;
- limiter le nombre de couches dans un Dockerfile ;
- ne pas exécuter les conteneurs avec les privilèges root ;
- utiliser des volumes pour les données persistantes ;
- utiliser Docker Compose pour les applications comportant plusieurs services.

---

## Résumé

Docker permet de développer, distribuer et exécuter des applications dans des conteneurs.

Les principaux concepts à retenir sont :

- une image est un modèle ;
- un conteneur est une instance d'une image ;
- un Dockerfile sert à construire une image ;
- Docker Compose permet d'exécuter plusieurs conteneurs ;
- les volumes assurent la persistance des données ;
- les réseaux permettent la communication entre les conteneurs.