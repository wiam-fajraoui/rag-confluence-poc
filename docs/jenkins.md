# Jenkins

## Présentation

Jenkins est un serveur d'automatisation open source principalement utilisé pour mettre en œuvre des pipelines d'intégration continue et de déploiement continu, également appelés CI/CD.

Il permet d'automatiser les différentes étapes du cycle de développement d'une application, depuis la compilation du code jusqu'au déploiement en production.

Jenkins est extensible grâce à un grand nombre de plugins qui lui permettent de s'intégrer avec de nombreux outils.

---

## Intégration Continue

L'intégration continue consiste à vérifier automatiquement qu'une modification du code ne casse pas l'application.

À chaque modification du dépôt Git, Jenkins peut :

- récupérer le code source ;
- installer les dépendances ;
- compiler le projet ;
- exécuter les tests ;
- générer des rapports.

Cette automatisation permet de détecter rapidement les erreurs.

---

## Déploiement Continu

Jenkins peut également automatiser le déploiement d'une application.

Selon la configuration du pipeline, une application peut être publiée :

- sur un serveur Linux ;
- dans un conteneur Docker ;
- sur un cluster Kubernetes ;
- sur Microsoft Azure ;
- sur AWS ;
- sur Google Cloud Platform.

---

## Architecture

Jenkins repose sur une architecture composée d'un serveur principal et éventuellement de plusieurs agents.

Le serveur principal orchestre les pipelines.

Les agents exécutent les tâches demandées.

Cette architecture permet d'exécuter plusieurs pipelines en parallèle.

---

## Les Pipelines

Un Pipeline décrit les différentes étapes d'un processus d'automatisation.

Chaque Pipeline est composé de plusieurs stages.

Chaque stage contient une ou plusieurs étapes.

Les pipelines permettent de standardiser les déploiements.

---

## Le Jenkinsfile

Les pipelines modernes sont décrits dans un fichier appelé Jenkinsfile.

Ce fichier est enregistré directement dans le dépôt Git.

Le Jenkinsfile est écrit dans un langage basé sur Groovy.

Cette approche permet de versionner les pipelines avec le reste du projet.

---

## Les Stages

Un stage représente une étape importante du pipeline.

Quelques exemples :

- Checkout
- Build
- Test
- Package
- Deploy

Les stages facilitent la lecture des pipelines.

---

## Les Steps

Chaque stage contient plusieurs steps.

Une step exécute une action précise.

Par exemple :

- lancer une commande ;
- exécuter un script ;
- construire une image Docker ;
- copier un fichier.

Les steps sont exécutées dans l'ordre.

---

## Les Agents

Les agents exécutent les pipelines.

Ils peuvent être installés sur plusieurs machines afin de répartir la charge de travail.

Chaque agent peut posséder son propre environnement logiciel.

---

## Les Plugins

L'un des principaux atouts de Jenkins est son système de plugins.

Il existe plusieurs milliers de plugins permettant d'intégrer Jenkins avec différents outils.

Quelques exemples :

- Git
- Docker
- Kubernetes
- Azure
- Maven
- Gradle
- SonarQube
- Slack

Les plugins ajoutent facilement de nouvelles fonctionnalités.

---

## Les Déclencheurs

Un pipeline peut être lancé automatiquement.

Les déclencheurs les plus courants sont :

- un commit Git ;
- une Pull Request ;
- une planification horaire ;
- un webhook ;
- un lancement manuel.

Cette automatisation évite les interventions répétitives.

---

## Les Variables

Les pipelines utilisent des variables afin de réutiliser certaines valeurs.

Par exemple :

- un numéro de version ;
- un nom d'environnement ;
- une URL ;
- un chemin.

Les variables facilitent la maintenance des pipelines.

---

## Les Credentials

Les Credentials permettent de stocker des informations sensibles.

Ils peuvent contenir :

- des mots de passe ;
- des clés SSH ;
- des jetons d'accès ;
- des certificats.

Les Credentials évitent d'enregistrer des informations confidentielles dans le code.

---

## Jenkins et Git

Jenkins s'intègre naturellement avec Git.

Il peut récupérer automatiquement le code d'un dépôt lors de chaque modification.

Les pipelines peuvent être déclenchés après un commit ou une Pull Request.

---

## Jenkins et Docker

Jenkins peut construire des images Docker.

Il peut également publier ces images dans un registre comme Docker Hub ou Azure Container Registry.

Les applications conteneurisées peuvent ensuite être déployées automatiquement.

---

## Jenkins et Kubernetes

Jenkins peut déployer des applications sur Kubernetes.

Il est également possible d'exécuter les agents Jenkins directement dans des Pods Kubernetes.

Cette approche améliore la scalabilité des pipelines.

---

## Jenkins et Azure

Jenkins peut déployer des applications sur Microsoft Azure.

Il prend en charge :

- Azure App Service ;
- Azure Virtual Machines ;
- Azure Kubernetes Service ;
- Azure Container Registry.

Des plugins facilitent cette intégration.

---

## Jenkins et Terraform

Jenkins est souvent utilisé pour automatiser les déploiements d'infrastructure.

Les pipelines peuvent exécuter :

- terraform init ;
- terraform plan ;
- terraform apply.

Cette automatisation réduit les interventions manuelles.

---

## Avantages

Jenkins présente plusieurs avantages :

- open source ;
- très flexible ;
- vaste bibliothèque de plugins ;
- compatible avec de nombreux outils ;
- adapté aux projets de toutes tailles.

---

## Limites

L'administration de Jenkins peut devenir complexe.

La maintenance des plugins et du serveur nécessite une surveillance régulière.

Pour les petits projets, GitHub Actions peut être plus simple à mettre en place.

---

## Bonnes pratiques

Il est recommandé de :

- versionner les Jenkinsfiles ;
- limiter les droits des Credentials ;
- automatiser les tests ;
- maintenir les plugins à jour ;
- utiliser des agents dédiés ;
- surveiller les performances du serveur Jenkins.

---

## Résumé

Jenkins est une plateforme d'automatisation utilisée pour mettre en place des pipelines CI/CD.

Les principaux concepts à retenir sont :

- les Pipelines automatisent les déploiements ;
- le Jenkinsfile décrit le pipeline sous forme de code ;
- les Stages organisent les différentes étapes ;
- les Plugins étendent les fonctionnalités ;
- les Agents exécutent les pipelines ;
- les Credentials protègent les informations sensibles ;
- Jenkins s'intègre avec Git, Docker, Kubernetes, Terraform et Microsoft Azure.