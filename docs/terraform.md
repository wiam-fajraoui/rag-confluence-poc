# Terraform

## Présentation

Terraform est un outil d'Infrastructure as Code, souvent abrégé IaC.

Il permet de créer, modifier et supprimer une infrastructure informatique à l'aide de fichiers de configuration.

Terraform est développé par HashiCorp.

Grâce à Terraform, l'infrastructure est décrite sous forme de code, ce qui facilite son automatisation et son suivi dans un système de gestion de versions comme Git.

---

## Infrastructure as Code

L'Infrastructure as Code consiste à décrire une infrastructure dans des fichiers texte.

Au lieu de créer manuellement des serveurs ou des bases de données, les ressources sont définies dans des fichiers de configuration.

Cette approche améliore la reproductibilité, la maintenance et la collaboration entre les équipes.

---

## Les fournisseurs

Terraform fonctionne grâce à des fournisseurs appelés Providers.

Chaque Provider permet de communiquer avec une plateforme.

Quelques Providers courants :

- Microsoft Azure
- Amazon Web Services
- Google Cloud Platform
- Kubernetes
- Docker
- GitHub

Le Provider Azure est nommé azurerm.

---

## Les fichiers Terraform

Les configurations Terraform sont généralement écrites dans des fichiers portant l'extension .tf.

Ces fichiers contiennent la description des ressources à créer.

Terraform lit automatiquement tous les fichiers .tf présents dans un même dossier.

---

## Les ressources

Une ressource représente un élément de l'infrastructure.

Une ressource peut être :

- une machine virtuelle ;
- un réseau ;
- une base de données ;
- un compte de stockage ;
- un cluster Kubernetes.

Chaque ressource possède un type et un nom.

---

## Les variables

Les variables permettent de rendre les configurations réutilisables.

Elles évitent de modifier directement les fichiers Terraform.

Une variable peut représenter :

- une région Azure ;
- un nom de ressource ;
- une taille de machine virtuelle ;
- un environnement.

---

## Les sorties

Les outputs permettent d'afficher des informations après le déploiement.

Par exemple :

- une adresse IP ;
- un nom de domaine ;
- l'identifiant d'une ressource.

Les outputs facilitent la communication entre plusieurs modules Terraform.

---

## Les modules

Un module est un ensemble de fichiers Terraform réutilisables.

Les modules permettent d'éviter la duplication du code.

Une entreprise peut créer un module pour déployer automatiquement une machine virtuelle ou un réseau.

Les modules facilitent la maintenance des infrastructures.

---

## L'état Terraform

Terraform conserve l'état de l'infrastructure dans un fichier appelé terraform.tfstate.

Ce fichier contient la liste des ressources créées.

Terraform compare cet état avec la configuration afin de déterminer les modifications nécessaires.

Le fichier d'état est essentiel au bon fonctionnement de Terraform.

---

## Initialisation

Avant d'utiliser Terraform, il faut initialiser le projet.

Commande :

terraform init

Cette commande télécharge les Providers nécessaires.

---

## Validation

Terraform peut vérifier la validité de la configuration.

Commande :

terraform validate

Cette étape permet de détecter les erreurs avant le déploiement.

---

## Planification

Terraform peut afficher les modifications qui seront réalisées.

Commande :

terraform plan

Cette commande ne modifie pas l'infrastructure.

Elle affiche simplement les ressources qui seront créées, modifiées ou supprimées.

---

## Déploiement

Pour appliquer la configuration :

terraform apply

Terraform demande généralement une confirmation avant de créer les ressources.

Une fois validée, l'infrastructure est créée automatiquement.

---

## Suppression

Terraform permet également de supprimer toutes les ressources créées.

Commande :

terraform destroy

Cette commande doit être utilisée avec prudence.

---

## Terraform et Azure

Terraform est largement utilisé avec Microsoft Azure.

Il permet notamment de créer :

- des Resource Groups ;
- des Machines Virtuelles ;
- des Virtual Networks ;
- des comptes de stockage ;
- des clusters Azure Kubernetes Service ;
- des bases de données Azure SQL.

Les ressources Azure sont gérées grâce au Provider azurerm.

---

## Terraform et Kubernetes

Terraform peut également créer des clusters Kubernetes.

Une fois le cluster créé, d'autres outils comme kubectl ou Helm permettent de déployer les applications.

Terraform est principalement utilisé pour créer l'infrastructure.

---

## Avantages

Terraform présente plusieurs avantages.

Il permet :

- d'automatiser les déploiements ;
- de versionner l'infrastructure avec Git ;
- de reproduire facilement un environnement ;
- de réduire les erreurs humaines ;
- de documenter l'infrastructure sous forme de code.

---

## Limites

Terraform n'est pas destiné à configurer les serveurs.

Son rôle est principalement de créer les ressources.

La configuration des machines est généralement réalisée avec Ansible ou d'autres outils spécialisés.

---

## Bonnes pratiques

Il est recommandé de :

- stocker le fichier d'état dans un emplacement sécurisé ;
- utiliser des modules réutilisables ;
- exécuter terraform plan avant terraform apply ;
- utiliser des variables plutôt que des valeurs codées en dur ;
- conserver les configurations dans un dépôt Git ;
- documenter les modules.

---

## Résumé

Terraform est un outil d'Infrastructure as Code.

Les principaux concepts à retenir sont :

- les Providers permettent de communiquer avec les plateformes cloud ;
- les ressources représentent les éléments de l'infrastructure ;
- les variables rendent les configurations réutilisables ;
- les modules facilitent la réutilisation du code ;
- terraform init initialise le projet ;
- terraform plan affiche les modifications prévues ;
- terraform apply déploie l'infrastructure ;
- terraform destroy supprime les ressources ;
- Terraform est largement utilisé pour automatiser les déploiements sur Azure.