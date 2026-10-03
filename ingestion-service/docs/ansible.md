# Ansible

## Présentation

Ansible est un outil d'automatisation open source développé par Red Hat.

Il permet d'automatiser la configuration des serveurs, le déploiement des applications et les tâches d'administration système.

Ansible fonctionne sans agent. Il communique directement avec les machines à l'aide du protocole SSH.

Il est largement utilisé dans les environnements Linux, Cloud et DevOps.

---

## Automatisation

L'objectif principal d'Ansible est d'automatiser des tâches répétitives.

Par exemple :

- installer un logiciel ;
- créer un utilisateur ;
- modifier un fichier de configuration ;
- redémarrer un service ;
- déployer une application.

L'automatisation réduit les erreurs humaines et fait gagner du temps.

---

## Architecture

Ansible repose sur une architecture simple.

Une machine de contrôle exécute les commandes Ansible.

Les machines administrées sont appelées Managed Nodes.

La communication s'effectue généralement via SSH.

Aucun logiciel supplémentaire n'est nécessaire sur les machines administrées.

---

## Inventaire

L'inventaire contient la liste des serveurs à administrer.

Les serveurs peuvent être regroupés selon leur rôle.

Exemple :

- serveurs web
- serveurs de bases de données
- serveurs de développement
- serveurs de production

Les inventaires peuvent être statiques ou dynamiques.

---

## Les Playbooks

Les Playbooks décrivent les tâches à exécuter.

Ils sont écrits au format YAML.

Chaque Playbook contient une ou plusieurs tâches.

Les Playbooks permettent d'automatiser complètement la configuration d'un serveur.

---

## Les tâches

Une tâche représente une action réalisée par Ansible.

Quelques exemples :

- installer un paquet ;
- copier un fichier ;
- créer un dossier ;
- démarrer un service ;
- supprimer un utilisateur.

Les tâches sont exécutées dans l'ordre où elles apparaissent.

---

## Les modules

Ansible possède plusieurs centaines de modules.

Chaque module réalise une opération spécifique.

Quelques modules courants :

- apt
- yum
- copy
- file
- service
- user
- git
- docker_container

Les modules permettent d'éviter l'écriture de scripts complexes.

---

## Les variables

Les variables rendent les Playbooks réutilisables.

Elles permettent de modifier facilement :

- un nom d'utilisateur ;
- un chemin ;
- un port ;
- une version d'application ;
- un environnement.

Les variables peuvent être définies dans plusieurs fichiers.

---

## Les rôles

Les rôles permettent d'organiser les Playbooks.

Un rôle regroupe :

- les tâches ;
- les variables ;
- les modèles ;
- les fichiers ;
- les gestionnaires.

Les rôles facilitent la réutilisation du code.

---

## Les handlers

Les handlers sont des tâches particulières.

Ils sont exécutés uniquement lorsqu'une modification est détectée.

Par exemple, un service peut être redémarré uniquement si son fichier de configuration a changé.

Cette approche évite les redémarrages inutiles.

---

## Exécution d'un Playbook

Un Playbook est exécuté avec la commande :

ansible-playbook site.yml

Ansible affiche ensuite les tâches exécutées ainsi que leur résultat.

---

## Idempotence

L'idempotence est un principe fondamental d'Ansible.

Si une tâche est déjà appliquée, Ansible ne la répète pas.

Ainsi, un Playbook peut être exécuté plusieurs fois sans modifier inutilement le système.

Ce comportement améliore la stabilité des déploiements.

---

## Ansible et Docker

Ansible peut installer Docker sur un serveur.

Il peut également démarrer ou arrêter des conteneurs.

Les modules Docker facilitent l'automatisation des applications conteneurisées.

---

## Ansible et Kubernetes

Ansible peut déployer des applications sur un cluster Kubernetes.

Il peut également automatiser certaines tâches d'administration du cluster.

---

## Ansible et Azure

Ansible permet d'automatiser la gestion des ressources Azure.

Il peut créer des machines virtuelles, configurer les réseaux et déployer des applications.

Il est souvent utilisé avec Terraform.

Terraform crée les ressources.

Ansible configure ensuite les serveurs.

---

## Avantages

Ansible présente plusieurs avantages :

- simplicité d'utilisation ;
- absence d'agent ;
- syntaxe YAML facile à lire ;
- nombreuses intégrations ;
- automatisation fiable des tâches répétitives.

---

## Limites

Ansible n'est pas conçu pour créer une infrastructure complète.

Son objectif principal est la configuration des systèmes existants.

Pour la création d'infrastructure, Terraform est généralement plus adapté.

---

## Bonnes pratiques

Il est recommandé de :

- organiser les Playbooks en rôles ;
- utiliser des variables plutôt que des valeurs fixes ;
- conserver les Playbooks dans un dépôt Git ;
- documenter les rôles ;
- tester les Playbooks avant leur utilisation en production ;
- privilégier des Playbooks courts et réutilisables.

---

## Résumé

Ansible est un outil d'automatisation et de gestion de configuration.

Les principaux concepts à retenir sont :

- les Playbooks décrivent les tâches ;
- les modules réalisent des actions spécifiques ;
- les rôles organisent les projets ;
- les handlers exécutent des actions conditionnelles ;
- l'idempotence garantit des déploiements fiables ;
- Ansible fonctionne sans agent grâce à SSH ;
- Terraform crée l'infrastructure tandis qu'Ansible configure les serveurs.