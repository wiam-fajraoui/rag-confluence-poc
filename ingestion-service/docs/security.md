# Sécurité informatique

## Présentation

La sécurité informatique regroupe l'ensemble des pratiques permettant de protéger les systèmes, les applications et les données contre les accès non autorisés, les attaques et les pertes de données.

La sécurité est un élément essentiel de toute infrastructure moderne, qu'elle soit hébergée sur site ou dans le Cloud.

Elle concerne aussi bien les utilisateurs que les serveurs, les réseaux et les applications.

---

## Les objectifs de la sécurité

La sécurité repose sur trois principes fondamentaux appelés triade CIA :

- Confidentialité
- Intégrité
- Disponibilité

La confidentialité garantit que seules les personnes autorisées peuvent accéder aux données.

L'intégrité assure que les données ne sont pas modifiées de manière non autorisée.

La disponibilité garantit que les services restent accessibles lorsque les utilisateurs en ont besoin.

---

## Authentification

L'authentification permet de vérifier l'identité d'un utilisateur ou d'une application.

Les méthodes les plus courantes sont :

- nom d'utilisateur et mot de passe ;
- certificat ;
- clé SSH ;
- authentification multifacteur.

Une authentification forte améliore considérablement la sécurité.

---

## Autorisation

Après l'authentification, le système détermine les actions autorisées.

L'autorisation définit les ressources auxquelles un utilisateur peut accéder ainsi que les opérations qu'il peut effectuer.

---

## RBAC

Le contrôle d'accès basé sur les rôles, ou Role-Based Access Control (RBAC), consiste à attribuer des permissions selon le rôle d'un utilisateur.

Par exemple :

- administrateur ;
- développeur ;
- opérateur ;
- lecteur.

Cette approche simplifie la gestion des permissions.

---

## Le principe du moindre privilège

Le principe du moindre privilège consiste à accorder uniquement les permissions nécessaires.

Un utilisateur ou une application ne doit jamais disposer de droits inutiles.

Cette pratique limite les conséquences d'une erreur ou d'une compromission.

---

## HTTPS

HTTPS protège les communications entre un client et un serveur.

Les données sont chiffrées grâce au protocole TLS.

HTTPS empêche l'interception des informations échangées.

Aujourd'hui, la majorité des applications web utilisent HTTPS.

---

## TLS

Transport Layer Security est le protocole utilisé pour sécuriser les communications réseau.

TLS garantit :

- le chiffrement des données ;
- l'authentification du serveur ;
- l'intégrité des échanges.

TLS remplace l'ancien protocole SSL.

---

## Les certificats

Les certificats numériques permettent de prouver l'identité d'un serveur.

Ils sont délivrés par une autorité de certification.

Le navigateur vérifie le certificat avant d'établir une connexion sécurisée.

---

## Le chiffrement

Le chiffrement transforme des données lisibles en données incompréhensibles sans clé de déchiffrement.

Il protège les informations stockées ainsi que les communications.

Le chiffrement est utilisé pour :

- les disques ;
- les bases de données ;
- les sauvegardes ;
- les échanges réseau.

---

## Les hachages

Une fonction de hachage produit une empreinte unique à partir d'une donnée.

Les hachages sont utilisés pour :

- vérifier l'intégrité ;
- stocker les mots de passe ;
- comparer des fichiers.

Contrairement au chiffrement, un hachage ne peut pas être inversé.

---

## Les mots de passe

Les mots de passe doivent être :

- longs ;
- complexes ;
- uniques.

Ils ne doivent jamais être enregistrés en clair dans une base de données.

Les mots de passe sont généralement stockés sous forme de hachage.

---

## L'authentification multifacteur

L'authentification multifacteur ajoute une seconde preuve d'identité.

Elle peut utiliser :

- un code temporaire ;
- une application mobile ;
- une clé physique ;
- une donnée biométrique.

Cette méthode réduit fortement les risques de compromission.

---

## OAuth 2.0

OAuth 2.0 est un protocole d'autorisation.

Il permet à une application d'accéder à des ressources sans connaître directement le mot de passe de l'utilisateur.

De nombreux services Cloud utilisent OAuth 2.0.

---

## OpenID Connect

OpenID Connect complète OAuth 2.0.

Il ajoute une couche d'authentification permettant de vérifier l'identité d'un utilisateur.

Il est largement utilisé pour le Single Sign-On.

---

## JWT

JSON Web Token est un format permettant de transmettre des informations de manière sécurisée.

Un JWT contient généralement :

- l'identité de l'utilisateur ;
- ses permissions ;
- une date d'expiration.

Les API modernes utilisent fréquemment les JWT.

---

## Les Secrets

Les informations sensibles ne doivent jamais être stockées dans le code source.

Les Secrets peuvent contenir :

- mots de passe ;
- clés API ;
- jetons d'accès ;
- chaînes de connexion.

Des outils spécialisés permettent de gérer ces informations de manière sécurisée.

---

## Azure Key Vault

Azure Key Vault est un service permettant de stocker les Secrets, les certificats et les clés de chiffrement.

Les applications peuvent récupérer ces informations sans les enregistrer directement dans le code.

---

## Sécurité de Docker

Les conteneurs doivent être exécutés avec le minimum de privilèges.

Les images doivent provenir de sources fiables.

Les Secrets ne doivent jamais être intégrés directement dans les images Docker.

Les images doivent être régulièrement mises à jour afin de corriger les vulnérabilités.

---

## Sécurité de Kubernetes

Kubernetes utilise le RBAC pour contrôler les accès au cluster.

Les Secrets Kubernetes permettent de stocker les informations sensibles.

Les politiques réseau limitent les communications entre les Pods.

Les images des conteneurs doivent être analysées avant leur déploiement.

---

## Sécurité dans Azure

Microsoft Azure fournit de nombreux services de sécurité.

Parmi les principaux :

- Microsoft Entra ID ;
- Azure Key Vault ;
- Microsoft Defender for Cloud ;
- Network Security Groups.

Ces services permettent de protéger les ressources Cloud.

---

## Journalisation

Les événements de sécurité doivent être enregistrés dans des journaux.

Ces journaux permettent :

- de détecter les attaques ;
- d'enquêter après un incident ;
- de respecter certaines exigences réglementaires.

---

## Bonnes pratiques

Il est recommandé de :

- utiliser HTTPS partout ;
- activer l'authentification multifacteur ;
- appliquer le principe du moindre privilège ;
- mettre régulièrement les logiciels à jour ;
- utiliser des Secrets plutôt que des mots de passe dans le code ;
- surveiller les journaux de sécurité ;
- effectuer des sauvegardes régulières.

---

## Résumé

La sécurité informatique protège les systèmes, les applications et les données.

Les principaux concepts à retenir sont :

- la triade CIA définit les objectifs de la sécurité ;
- l'authentification vérifie l'identité ;
- l'autorisation détermine les permissions ;
- RBAC facilite la gestion des accès ;
- TLS sécurise les communications ;
- OAuth 2.0 et OpenID Connect sont utilisés pour l'authentification moderne ;
- les JWT sont couramment utilisés dans les API ;
- Azure Key Vault protège les informations sensibles ;
- la sécurité doit être intégrée dès la conception des applications.