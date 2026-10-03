# Git

## Présentation

Git est un système de gestion de versions distribué.

Il permet de suivre les modifications apportées au code source d'un projet.

Git facilite la collaboration entre plusieurs développeurs et conserve l'historique complet des changements.

Chaque développeur possède une copie complète du dépôt sur sa machine.

---

## Les dépôts Git

Un dépôt, appelé repository, contient l'ensemble des fichiers du projet ainsi que l'historique des modifications.

Un dépôt peut être local ou distant.

Le dépôt local est stocké sur l'ordinateur du développeur.

Le dépôt distant est généralement hébergé sur une plateforme comme GitHub, GitLab ou Azure DevOps.

---

## Initialiser un dépôt

Un nouveau dépôt Git peut être créé avec la commande :

git init

Cette commande crée un dossier caché nommé .git contenant toutes les informations du dépôt.

---

## Cloner un dépôt

Pour récupérer un dépôt existant, on utilise la commande :

git clone <url_du_depot>

Cette commande télécharge le projet ainsi que tout son historique.

---

## Le suivi des fichiers

Git distingue plusieurs états pour les fichiers :

- Non suivis
- Modifiés
- Indexés
- Validés

Les fichiers doivent être ajoutés à l'index avant d'être enregistrés dans l'historique.

---

## Ajouter des fichiers

Pour ajouter un fichier à l'index :

git add fichier.py

Pour ajouter tous les fichiers modifiés :

git add .

---

## Les commits

Un commit représente un enregistrement des modifications.

Chaque commit possède un identifiant unique.

Les commits permettent de retrouver facilement une version précédente du projet.

Créer un commit :

git commit -m "Ajout du système d'authentification"

Il est recommandé d'utiliser des messages de commit clairs et explicites.

---

## Consulter l'historique

L'historique des commits peut être affiché avec :

git log

Une version simplifiée est disponible avec :

git log --oneline

---

## Les branches

Une branche permet de développer une fonctionnalité indépendamment de la branche principale.

La branche principale est généralement appelée main.

Créer une branche :

git branch nouvelle-fonction

Se placer sur cette branche :

git checkout nouvelle-fonction

Ou en une seule commande :

git checkout -b nouvelle-fonction

---

## Fusionner des branches

Lorsque le développement est terminé, la branche peut être fusionnée avec la branche principale.

Commande :

git merge nouvelle-fonction

Git tente automatiquement de fusionner les modifications.

---

## Les conflits

Un conflit apparaît lorsque deux personnes modifient les mêmes lignes d'un fichier.

Git demande alors au développeur de choisir quelles modifications conserver.

Les conflits doivent être résolus avant de terminer la fusion.

---

## Les dépôts distants

Git permet de synchroniser un dépôt local avec un dépôt distant.

Afficher les dépôts distants :

git remote -v

Ajouter un dépôt distant :

git remote add origin <url>

---

## Envoyer les modifications

Pour envoyer les commits vers le dépôt distant :

git push origin main

Cette commande met à jour le dépôt distant.

---

## Récupérer les modifications

Pour récupérer les dernières modifications :

git pull

Cette commande télécharge les nouveaux commits et les fusionne avec le dépôt local.

Il est également possible de récupérer les modifications sans les fusionner avec :

git fetch

---

## Annuler des modifications

Annuler les modifications d'un fichier :

git restore fichier.py

Annuler le dernier commit sans supprimer les fichiers :

git reset --soft HEAD~1

Annuler complètement le dernier commit :

git reset --hard HEAD~1

Ces commandes doivent être utilisées avec précaution.

---

## Le fichier .gitignore

Le fichier .gitignore permet d'indiquer les fichiers qui ne doivent pas être suivis par Git.

On y retrouve souvent :

- les fichiers temporaires ;
- les environnements virtuels Python ;
- les fichiers de configuration locaux ;
- les fichiers compilés.

Exemple :

__pycache__/

.venv/

.env

---

## Les tags

Les tags permettent de marquer une version importante du projet.

Ils sont souvent utilisés pour identifier une version de production.

Créer un tag :

git tag v1.0.0

Lister les tags :

git tag

---

## Bonnes pratiques

Pour utiliser Git efficacement, il est recommandé de :

- réaliser des commits fréquents ;
- écrire des messages de commit explicites ;
- utiliser une branche par fonctionnalité ;
- mettre régulièrement à jour sa branche ;
- éviter les commits contenant plusieurs modifications sans lien ;
- utiliser un fichier .gitignore adapté au projet.

---

## Résumé

Git est un système de gestion de versions distribué.

Les principaux concepts à retenir sont :

- un dépôt contient le projet et son historique ;
- un commit enregistre les modifications ;
- une branche permet de développer une fonctionnalité indépendamment ;
- un merge fusionne plusieurs branches ;
- un dépôt distant facilite la collaboration ;
- git push envoie les modifications ;
- git pull récupère les dernières versions ;
- le fichier .gitignore exclut certains fichiers du suivi.