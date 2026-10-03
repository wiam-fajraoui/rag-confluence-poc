# Kubernetes

## Présentation

Kubernetes est une plateforme open source d'orchestration de conteneurs.

Il permet d'automatiser le déploiement, la mise à l'échelle et la gestion des applications conteneurisées.

Kubernetes est souvent utilisé avec Docker ou d'autres technologies de conteneurisation.

Il facilite le fonctionnement des applications distribuées et améliore leur disponibilité.

---

## Architecture Kubernetes

Une architecture Kubernetes est composée d'un plan de contrôle (Control Plane) et d'un ou plusieurs nœuds de travail (Worker Nodes).

Le Control Plane prend les décisions concernant le cluster.

Les Worker Nodes exécutent les applications sous forme de Pods.

L'ensemble des machines constitue un cluster Kubernetes.

---

## Le Control Plane

Le Control Plane est responsable de la gestion du cluster.

Il planifie les Pods.

Il surveille l'état du cluster.

Il applique les configurations définies par les utilisateurs.

Il veille à ce que l'état réel du cluster corresponde à l'état souhaité.

---

## Les Worker Nodes

Les Worker Nodes exécutent les charges de travail.

Chaque Worker Node possède un agent appelé kubelet.

Le kubelet communique avec le Control Plane afin de recevoir les instructions de déploiement.

Les Worker Nodes exécutent également le moteur de conteneurs.

---

## Les Pods

Le Pod est la plus petite unité déployable dans Kubernetes.

Un Pod contient un ou plusieurs conteneurs.

Les conteneurs d'un même Pod partagent le réseau et le stockage.

Les Pods sont temporaires et peuvent être recréés automatiquement en cas de défaillance.

---

## Les Deployments

Un Deployment permet de gérer un ensemble de Pods.

Il assure le maintien du nombre souhaité de Pods.

Il facilite les mises à jour des applications.

Il permet également de revenir à une version précédente en cas de problème.

---

## Les ReplicaSets

Un ReplicaSet garantit qu'un nombre précis de Pods est toujours en fonctionnement.

Si un Pod est supprimé ou tombe en panne, Kubernetes en crée automatiquement un nouveau.

Les ReplicaSets sont généralement gérés par les Deployments.

---

## Les Services

Un Service permet d'exposer une application exécutée dans un ou plusieurs Pods.

Il fournit une adresse réseau stable.

Les Services permettent aux applications de communiquer entre elles.

Ils facilitent également l'accès aux applications depuis l'extérieur du cluster.

---

## L'Ingress

Un Ingress permet de gérer les accès HTTP et HTTPS vers les applications.

Il peut rediriger les requêtes vers différents Services.

Il facilite la publication de plusieurs applications à l'aide d'une seule adresse IP.

---

## Les ConfigMaps

Les ConfigMaps permettent de stocker des paramètres de configuration.

Ils évitent d'intégrer les paramètres directement dans l'application.

Les Pods peuvent lire ces informations au démarrage.

---

## Les Secrets

Les Secrets permettent de stocker des informations sensibles.

Ils sont utilisés pour conserver des mots de passe, des clés API ou des certificats.

Les applications peuvent accéder à ces informations sans les enregistrer directement dans leur code.

---

## Les Volumes Persistants

Les Pods étant temporaires, les données doivent être stockées dans un espace persistant.

Les Persistent Volumes permettent de conserver les données indépendamment du cycle de vie des Pods.

Ils sont principalement utilisés avec les bases de données.

---

## Mise à l'échelle

Kubernetes permet d'augmenter ou de diminuer automatiquement le nombre de Pods.

Cette fonctionnalité est appelée autoscaling.

Elle permet d'adapter les ressources aux besoins des utilisateurs.

---

## Mise à jour des applications

Kubernetes permet de mettre à jour une application sans interruption de service.

Les nouvelles versions sont déployées progressivement.

En cas d'erreur, il est possible de revenir automatiquement à la version précédente.

---

## Surveillance du cluster

Kubernetes surveille en permanence l'état des Pods.

Si un Pod cesse de fonctionner correctement, il est automatiquement remplacé.

Cette capacité améliore la disponibilité des applications.

---

## Commandes courantes

Créer un Deployment :

kubectl create deployment mon-api --image=nginx

Afficher les Pods :

kubectl get pods

Afficher les Services :

kubectl get services

Afficher les Deployments :

kubectl get deployments

Décrire un Pod :

kubectl describe pod <nom_du_pod>

Supprimer un Pod :

kubectl delete pod <nom_du_pod>

---

## Bonnes pratiques

Il est recommandé de :

- utiliser des Deployments plutôt que de créer directement des Pods ;
- limiter les ressources CPU et mémoire des applications ;
- utiliser des ConfigMaps pour la configuration ;
- utiliser des Secrets pour les informations sensibles ;
- surveiller régulièrement l'état du cluster ;
- mettre en place des stratégies de sauvegarde des données persistantes.

---

## Résumé

Kubernetes est une plateforme d'orchestration de conteneurs.

Les principaux concepts à retenir sont :

- un cluster est composé d'un Control Plane et de Worker Nodes ;
- les Pods exécutent les conteneurs ;
- les Deployments gèrent les Pods ;
- les ReplicaSets garantissent leur disponibilité ;
- les Services permettent la communication ;
- les ConfigMaps stockent la configuration ;
- les Secrets protègent les données sensibles ;
- les Persistent Volumes assurent la persistance des données ;
- Kubernetes automatise le déploiement, la mise à l'échelle et la gestion des applications.