# Azure DevOps

## Présentation

Azure DevOps est une plateforme de collaboration et de gestion du cycle de vie des applications développée par Microsoft.

Elle permet aux équipes de planifier les projets, gérer le code source, automatiser les tests et déployer les applications.

Azure DevOps est composé de plusieurs services intégrés qui facilitent le développement logiciel et les pratiques DevOps.

---

## Les services Azure DevOps

Azure DevOps est composé de plusieurs modules principaux :

- Azure Boards
- Azure Repos
- Azure Pipelines
- Azure Test Plans
- Azure Artifacts

Chaque module répond à un besoin spécifique du cycle de développement.

---

## Azure Boards

Azure Boards permet de gérer les projets et les tâches.

Les équipes peuvent créer :

- des User Stories ;
- des Bugs ;
- des Features ;
- des Epics ;
- des Tasks.

Azure Boards facilite le suivi de l'avancement des projets.

---

## Les Work Items

Les éléments de travail, appelés Work Items, représentent les différentes tâches du projet.

Chaque Work Item possède :

- un identifiant ;
- un titre ;
- une description ;
- un responsable ;
- un état ;
- une priorité.

Les Work Items facilitent l'organisation du travail.

---

## Azure Repos

Azure Repos est un service d'hébergement de dépôts Git.

Les développeurs peuvent collaborer sur le même projet grâce aux branches et aux Pull Requests.

Azure Repos fonctionne de manière similaire à GitHub.

---

## Les branches

Les branches permettent de développer plusieurs fonctionnalités en parallèle.

Chaque nouvelle fonctionnalité peut être développée dans une branche dédiée.

Une fois terminée, la branche est fusionnée avec la branche principale.

Cette approche réduit les conflits et améliore la qualité du code.

---

## Les Pull Requests

Une Pull Request permet de proposer une modification du code.

Avant la fusion, les autres membres de l'équipe peuvent :

- relire le code ;
- ajouter des commentaires ;
- demander des modifications ;
- approuver les changements.

Cette étape améliore la qualité du projet.

---

## Azure Pipelines

Azure Pipelines est le moteur CI/CD d'Azure DevOps.

Il permet d'automatiser :

- la compilation ;
- les tests ;
- la création des artefacts ;
- le déploiement.

Les pipelines sont généralement décrits dans des fichiers YAML.

---

## Intégration Continue

L'intégration continue consiste à vérifier automatiquement le projet après chaque modification.

Les pipelines exécutent automatiquement :

- les tests ;
- les analyses de qualité ;
- la compilation ;
- la génération des artefacts.

Cette automatisation réduit les erreurs.

---

## Déploiement Continu

Le déploiement continu permet de publier automatiquement une application.

Azure Pipelines peut déployer une application vers :

- Azure App Service ;
- Azure Kubernetes Service ;
- Azure Virtual Machines ;
- Docker ;
- Kubernetes.

---

## Les Agents

Les pipelines sont exécutés par des Agents.

Microsoft fournit des Agents hébergés.

Les entreprises peuvent également installer leurs propres Agents sur leurs serveurs.

Les Agents peuvent fonctionner sous Linux, Windows ou macOS.

---

## Azure Artifacts

Azure Artifacts permet de partager des packages entre plusieurs projets.

Les équipes peuvent publier des bibliothèques et des dépendances internes.

Azure Artifacts prend en charge plusieurs gestionnaires de paquets.

---

## Azure Test Plans

Azure Test Plans permet de gérer les campagnes de tests.

Les équipes peuvent créer :

- des scénarios de test ;
- des plans de test ;
- des campagnes de validation.

Les résultats sont centralisés dans Azure DevOps.

---

## Les Variables

Les pipelines utilisent des variables afin d'éviter les valeurs codées en dur.

Les variables permettent notamment de définir :

- un environnement ;
- une version ;
- un nom d'application ;
- une région Azure.

Les variables améliorent la réutilisation des pipelines.

---

## Les Secrets

Les informations sensibles sont stockées sous forme de Secrets.

Les Secrets permettent de protéger :

- les mots de passe ;
- les clés API ;
- les chaînes de connexion ;
- les jetons d'accès.

Les Secrets ne sont jamais affichés dans les journaux des pipelines.

---

## Azure DevOps et Git

Azure DevOps intègre Git pour la gestion du code source.

Les développeurs peuvent créer des branches, réaliser des Pull Requests et consulter l'historique des commits.

---

## Azure DevOps et Docker

Azure Pipelines peut construire automatiquement une image Docker.

L'image peut ensuite être publiée dans Azure Container Registry ou Docker Hub.

Cette automatisation facilite le déploiement des applications conteneurisées.

---

## Azure DevOps et Kubernetes

Azure Pipelines peut déployer automatiquement des applications sur Azure Kubernetes Service.

Les nouvelles versions peuvent être publiées sans interruption de service.

---

## Azure DevOps et Terraform

Azure DevOps est souvent utilisé pour exécuter automatiquement les commandes Terraform.

Les pipelines peuvent lancer :

- terraform init
- terraform plan
- terraform apply

Cette approche automatise entièrement le déploiement de l'infrastructure.

---

## Avantages

Azure DevOps présente plusieurs avantages :

- plateforme complète ;
- intégration native avec Microsoft Azure ;
- gestion centralisée des projets ;
- pipelines CI/CD performants ;
- prise en charge de Git ;
- gestion des tests et des artefacts.

---

## Limites

Azure DevOps est une plateforme très riche.

Sa prise en main peut être plus complexe que celle de GitHub Actions pour les petits projets.

Les nombreuses fonctionnalités nécessitent un temps d'apprentissage.

---

## Bonnes pratiques

Il est recommandé de :

- utiliser des pipelines YAML ;
- automatiser les tests ;
- protéger les branches principales ;
- utiliser les Pull Requests ;
- stocker les informations sensibles dans les Secrets ;
- documenter les pipelines ;
- versionner les configurations d'infrastructure.

---

## Résumé

Azure DevOps est une plateforme complète dédiée au développement logiciel et aux pratiques DevOps.

Les principaux concepts à retenir sont :

- Azure Boards gère les projets ;
- Azure Repos héberge les dépôts Git ;
- Azure Pipelines automatise les déploiements ;
- Azure Test Plans facilite les campagnes de tests ;
- Azure Artifacts partage les dépendances ;
- les Agents exécutent les pipelines ;
- Azure DevOps s'intègre naturellement avec Git, Docker, Kubernetes, Terraform et Microsoft Azure.