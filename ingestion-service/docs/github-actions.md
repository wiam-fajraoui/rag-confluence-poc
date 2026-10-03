# GitHub Actions

## Présentation

GitHub Actions est un service d'intégration continue et de déploiement continu, également appelé CI/CD.

Il permet d'automatiser des tâches directement depuis un dépôt GitHub.

Les workflows sont exécutés automatiquement lorsqu'un événement se produit, comme un commit, une Pull Request ou la création d'un tag.

GitHub Actions facilite l'automatisation du développement, des tests et des déploiements.

---

## Intégration Continue

L'intégration continue, appelée Continuous Integration ou CI, consiste à vérifier automatiquement le code à chaque modification.

Les principales étapes sont :

- récupérer le code ;
- installer les dépendances ;
- exécuter les tests ;
- vérifier la qualité du code ;
- générer les artefacts.

Cette approche permet de détecter rapidement les erreurs.

---

## Déploiement Continu

Le déploiement continu, appelé Continuous Deployment ou CD, permet de publier automatiquement une application.

Le déploiement peut être effectué vers :

- un serveur Linux ;
- Docker ;
- Kubernetes ;
- Microsoft Azure ;
- AWS ;
- Google Cloud Platform.

---

## Les Workflows

Un Workflow décrit les tâches à automatiser.

Les Workflows sont écrits au format YAML.

Ils sont enregistrés dans le dossier :

.github/workflows

Un dépôt peut contenir plusieurs Workflows.

---

## Les événements

Un Workflow est déclenché par un événement.

Les événements les plus courants sont :

- push
- pull_request
- workflow_dispatch
- release
- schedule

Un Workflow peut également être lancé manuellement.

---

## Les Jobs

Un Workflow est composé d'un ou plusieurs Jobs.

Chaque Job représente un ensemble de tâches.

Les Jobs peuvent être exécutés en parallèle ou de manière séquentielle.

Chaque Job est exécuté sur une machine virtuelle temporaire.

---

## Les Steps

Un Job est composé de plusieurs Steps.

Une Step peut :

- exécuter une commande ;
- utiliser une Action ;
- lancer un script.

Les Steps sont exécutées dans l'ordre.

---

## Les Actions

Une Action est un composant réutilisable.

Les Actions permettent de réaliser rapidement des opérations courantes.

Exemples :

- récupérer le dépôt ;
- installer Python ;
- construire une image Docker ;
- publier une application.

GitHub fournit de nombreuses Actions officielles.

---

## Les Runners

Les Runners exécutent les Workflows.

GitHub propose des Runners hébergés.

Il est également possible d'utiliser des Self-Hosted Runners installés sur ses propres serveurs.

Les systèmes d'exploitation disponibles sont :

- Ubuntu
- Windows
- macOS

---

## Les Secrets

Les Secrets permettent de stocker des informations sensibles.

Ils sont utilisés pour :

- les mots de passe ;
- les clés API ;
- les jetons d'accès ;
- les identifiants de connexion.

Les Secrets sont chiffrés et ne sont jamais affichés dans les journaux d'exécution.

---

## Les Variables

Les Variables permettent de réutiliser des valeurs dans plusieurs Workflows.

Elles facilitent la maintenance des pipelines.

Une variable peut représenter :

- un nom d'environnement ;
- une version de Python ;
- une URL ;
- un nom d'application.

---

## Les Artefacts

Les Artefacts sont les fichiers générés pendant un Workflow.

Ils peuvent être téléchargés après l'exécution.

Exemples :

- application compilée ;
- rapport de tests ;
- fichiers ZIP ;
- images Docker.

---

## GitHub Actions et Docker

GitHub Actions peut construire une image Docker.

Il peut ensuite publier cette image dans un registre comme Docker Hub ou GitHub Container Registry.

Cette automatisation simplifie le déploiement des applications conteneurisées.

---

## GitHub Actions et Azure

GitHub Actions permet de déployer automatiquement une application sur Microsoft Azure.

Les services Azure peuvent être authentifiés grâce à des Secrets.

Il est possible de déployer :

- Azure App Service ;
- Azure Functions ;
- Azure Kubernetes Service ;
- Azure Container Registry.

---

## GitHub Actions et Kubernetes

GitHub Actions peut déployer automatiquement une application sur un cluster Kubernetes.

Le pipeline peut :

- construire une image Docker ;
- publier l'image ;
- mettre à jour le cluster Kubernetes.

---

## Avantages

GitHub Actions présente plusieurs avantages :

- intégré directement à GitHub ;
- configuration simple en YAML ;
- nombreuses Actions disponibles ;
- automatisation complète du cycle de développement ;
- intégration avec de nombreux services Cloud.

---

## Limites

GitHub Actions est principalement destiné aux projets hébergés sur GitHub.

Pour certaines grandes entreprises, des solutions comme Azure DevOps ou Jenkins peuvent offrir davantage de fonctionnalités d'administration.

---

## Bonnes pratiques

Il est recommandé de :

- créer un Workflow par objectif ;
- utiliser des Secrets pour les informations sensibles ;
- exécuter les tests avant chaque déploiement ;
- limiter les droits des jetons d'accès ;
- documenter les pipelines ;
- réutiliser les Actions officielles lorsque cela est possible.

---

## Résumé

GitHub Actions est une plateforme CI/CD intégrée à GitHub.

Les principaux concepts à retenir sont :

- les Workflows automatisent les tâches ;
- les événements déclenchent les pipelines ;
- les Jobs regroupent plusieurs étapes ;
- les Steps exécutent les actions ;
- les Runners exécutent les Workflows ;
- les Secrets protègent les informations sensibles ;
- GitHub Actions automatise les tests et les déploiements vers Docker, Kubernetes et Azure.