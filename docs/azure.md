# Azure

## Présentation

Microsoft Azure est une plateforme de cloud computing développée par Microsoft.

Elle permet de créer, déployer et gérer des applications dans le cloud.

Azure fournit des centaines de services couvrant l'infrastructure, le stockage, les bases de données, l'intelligence artificielle, la sécurité et le DevOps.

Les entreprises utilisent Azure pour héberger leurs applications tout en bénéficiant d'une infrastructure évolutive et hautement disponible.

---

## Les régions Azure

Azure est réparti dans de nombreuses régions à travers le monde.

Une région est un ensemble de centres de données situés dans une même zone géographique.

Le choix d'une région dépend généralement de la proximité avec les utilisateurs, des contraintes réglementaires et de la disponibilité des services.

---

## Les Resource Groups

Un Resource Group est un conteneur logique permettant de regrouper plusieurs ressources Azure.

Toutes les ressources d'une même application peuvent être organisées dans un même Resource Group.

Cette organisation facilite la gestion, le suivi des coûts et la suppression des ressources.

---

## Les Machines Virtuelles

Azure Virtual Machines permet de créer des serveurs virtuels dans le cloud.

Une machine virtuelle peut exécuter Windows ou Linux.

Les machines virtuelles sont utilisées pour héberger des applications, des bases de données ou des services réseau.

Les ressources comme le processeur, la mémoire et le stockage peuvent être adaptées selon les besoins.

---

## Azure App Service

Azure App Service est un service permettant de déployer rapidement des applications web.

Les développeurs peuvent publier leurs applications sans gérer directement les serveurs.

App Service prend en charge plusieurs langages comme Python, Java, .NET, Node.js et PHP.

---

## Azure Blob Storage

Azure Blob Storage est un service de stockage d'objets.

Il permet de stocker des fichiers tels que des images, des vidéos, des documents ou des sauvegardes.

Les données sont organisées dans des conteneurs.

Blob Storage est souvent utilisé pour l'archivage ou le stockage de fichiers volumineux.

---

## Azure SQL Database

Azure SQL Database est une base de données relationnelle entièrement administrée.

Microsoft assure automatiquement les sauvegardes, les mises à jour et la haute disponibilité.

Ce service permet de réduire les tâches d'administration des bases de données.

---

## Azure Kubernetes Service

Azure Kubernetes Service, également appelé AKS, est un service permettant d'exécuter des clusters Kubernetes.

Azure prend en charge la gestion du Control Plane.

Les utilisateurs administrent principalement les applications et les Worker Nodes.

AKS facilite le déploiement des applications conteneurisées.

---

## Azure Functions

Azure Functions permet d'exécuter du code sans gérer de serveur.

Ce modèle est appelé Serverless.

Une fonction est déclenchée par un événement comme une requête HTTP, un fichier ajouté dans un stockage ou un message reçu dans une file d'attente.

---

## Azure AI Search

Azure AI Search est un service de recherche documentaire.

Il permet d'indexer des documents afin de les retrouver rapidement.

Azure AI Search prend en charge la recherche textuelle, la recherche vectorielle et l'enrichissement des documents grâce à l'intelligence artificielle.

Ce service est souvent utilisé dans les applications RAG.

---

## Azure Key Vault

Azure Key Vault permet de stocker des informations sensibles.

Les mots de passe, certificats, clés de chiffrement et secrets applicatifs peuvent y être conservés de manière sécurisée.

Les applications peuvent accéder aux secrets sans les stocker directement dans leur code.

---

## Azure Monitor

Azure Monitor permet de superviser les ressources Azure.

Il collecte les métriques, les journaux et les événements produits par les applications.

Les administrateurs peuvent créer des alertes afin d'être informés rapidement d'un problème.

---

## La sécurité dans Azure

Azure fournit de nombreux mécanismes de sécurité.

Les accès sont contrôlés grâce à Azure Active Directory.

Les autorisations sont gérées par le contrôle d'accès basé sur les rôles, appelé RBAC.

Les données peuvent être chiffrées au repos et pendant leur transfert.

---

## Haute disponibilité

Azure est conçu pour assurer une forte disponibilité des applications.

Les ressources peuvent être réparties sur plusieurs zones de disponibilité.

Cette architecture limite les interruptions de service en cas de panne matérielle.

---

## Scalabilité

Azure permet d'augmenter ou de diminuer automatiquement les ressources selon la charge.

Cette fonctionnalité permet de répondre aux variations du trafic tout en optimisant les coûts.

---

## Cas d'utilisation

Azure est utilisé pour :

- héberger des applications web ;
- exécuter des API ;
- stocker des fichiers ;
- entraîner des modèles d'intelligence artificielle ;
- déployer des applications conteneurisées ;
- créer des pipelines DevOps ;
- mettre en place des solutions de sauvegarde.

---

## Bonnes pratiques

Il est recommandé de :

- organiser les ressources dans des Resource Groups ;
- utiliser des noms cohérents pour les ressources ;
- protéger les secrets avec Azure Key Vault ;
- surveiller les ressources avec Azure Monitor ;
- utiliser le principe du moindre privilège pour les accès ;
- automatiser les déploiements avec des outils DevOps.

---

## Résumé

Microsoft Azure est une plateforme de cloud computing.

Les principaux concepts à retenir sont :

- les régions hébergent les ressources Azure ;
- les Resource Groups permettent d'organiser les ressources ;
- Azure Virtual Machines fournit des serveurs virtuels ;
- Azure App Service héberge les applications web ;
- Azure Blob Storage stocke des fichiers ;
- Azure SQL Database fournit une base de données relationnelle ;
- Azure Kubernetes Service exécute des clusters Kubernetes ;
- Azure Functions permet le Serverless ;
- Azure AI Search fournit des fonctionnalités de recherche documentaire ;
- Azure Monitor supervise les ressources ;
- Azure Key Vault protège les informations sensibles.