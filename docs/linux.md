# Linux

## Présentation

Linux est un système d'exploitation open source largement utilisé dans les environnements professionnels.

Il est reconnu pour sa stabilité, sa sécurité et ses performances.

La majorité des serveurs, des plateformes cloud et des conteneurs utilisent Linux.

De nombreuses distributions existent, comme Ubuntu, Debian, Rocky Linux, Fedora et Red Hat Enterprise Linux.

---

## Le terminal

Le terminal est l'interface en ligne de commande de Linux.

Il permet d'exécuter des commandes pour administrer le système.

Le terminal offre un contrôle précis sur le système d'exploitation et permet d'automatiser de nombreuses tâches.

---

## Le système de fichiers

Sous Linux, tous les fichiers sont organisés dans une arborescence unique.

Le répertoire racine est représenté par le caractère :

/

Quelques répertoires importants :

- /home contient les dossiers des utilisateurs.
- /etc contient les fichiers de configuration.
- /var contient les journaux et les données des services.
- /tmp contient les fichiers temporaires.
- /usr contient les applications installées.
- /bin contient des commandes essentielles.

---

## Navigation dans les répertoires

Afficher le répertoire courant :

pwd

Lister les fichiers :

ls

Lister les fichiers avec leurs détails :

ls -l

Afficher les fichiers cachés :

ls -la

Changer de répertoire :

cd Documents

Revenir au dossier précédent :

cd ..

Revenir au dossier personnel :

cd ~

---

## Gestion des fichiers

Créer un fichier :

touch fichier.txt

Créer un dossier :

mkdir projet

Supprimer un fichier :

rm fichier.txt

Supprimer un dossier vide :

rmdir dossier

Supprimer un dossier et son contenu :

rm -r dossier

Copier un fichier :

cp fichier.txt sauvegarde.txt

Déplacer ou renommer un fichier :

mv ancien.txt nouveau.txt

---

## Consulter un fichier

Afficher le contenu d'un fichier :

cat fichier.txt

Lire un fichier page par page :

less fichier.txt

Afficher les premières lignes :

head fichier.txt

Afficher les dernières lignes :

tail fichier.txt

Suivre un fichier de logs :

tail -f application.log

---

## Rechercher des fichiers

Rechercher un fichier :

find . -name "config.yml"

Rechercher un texte dans plusieurs fichiers :

grep "docker" *.txt

La commande grep est très utilisée pour rechercher une information dans des fichiers de configuration ou des journaux.

---

## Les permissions

Chaque fichier possède des droits d'accès.

Les permissions concernent :

- le propriétaire ;
- le groupe ;
- les autres utilisateurs.

Afficher les permissions :

ls -l

Modifier les permissions :

chmod 755 script.sh

Modifier le propriétaire :

chown utilisateur fichier.txt

---

## Les utilisateurs

Créer un utilisateur :

sudo adduser alice

Supprimer un utilisateur :

sudo deluser alice

Changer de mot de passe :

passwd

Afficher l'utilisateur connecté :

whoami

---

## Les processus

Afficher les processus actifs :

ps

Afficher les processus en temps réel :

top

Une version plus moderne est :

htop

Arrêter un processus :

kill PID

---

## Les services

Les services sont gérés avec systemd.

Démarrer un service :

sudo systemctl start nginx

Arrêter un service :

sudo systemctl stop nginx

Redémarrer un service :

sudo systemctl restart nginx

Afficher l'état d'un service :

sudo systemctl status nginx

---

## Les journaux

Les journaux permettent d'analyser le fonctionnement du système.

Ils sont principalement stockés dans :

/var/log

Afficher les journaux système :

journalctl

Afficher les derniers événements :

journalctl -n 50

---

## Gestion des paquets

Sous Ubuntu et Debian :

Mettre à jour les dépôts :

sudo apt update

Installer un logiciel :

sudo apt install git

Mettre à jour les logiciels :

sudo apt upgrade

Supprimer un logiciel :

sudo apt remove git

---

## Les variables d'environnement

Les variables d'environnement permettent de stocker des informations accessibles par les applications.

Afficher toutes les variables :

env

Afficher une variable :

echo $HOME

Créer une variable temporaire :

export ENV=production

---

## Les scripts Bash

Bash est l'interpréteur de commandes par défaut de nombreuses distributions Linux.

Les scripts Bash permettent d'automatiser des tâches répétitives.

Un script commence généralement par :

#!/bin/bash

Pour exécuter un script :

bash script.sh

Ou :

chmod +x script.sh

./script.sh

---

## Les connexions distantes

SSH permet de se connecter à un serveur distant de manière sécurisée.

Connexion :

ssh utilisateur@serveur

Copie de fichiers :

scp fichier.txt utilisateur@serveur:/home/utilisateur

SSH est très utilisé pour administrer les serveurs Linux.

---

## Bonnes pratiques

Il est recommandé de :

- utiliser le terminal régulièrement ;
- limiter l'utilisation du compte root ;
- mettre à jour le système fréquemment ;
- attribuer les permissions minimales nécessaires ;
- sauvegarder régulièrement les données importantes ;
- consulter les journaux en cas d'erreur.

---

## Résumé

Linux est un système d'exploitation largement utilisé dans les environnements serveurs et cloud.

Les principaux concepts à retenir sont :

- le terminal permet d'administrer le système ;
- les fichiers sont organisés dans une arborescence ;
- les permissions protègent les ressources ;
- les processus représentent les programmes en cours d'exécution ;
- les services sont gérés avec systemd ;
- les journaux facilitent le diagnostic des problèmes ;
- les scripts Bash automatisent les tâches ;
- SSH permet l'administration à distance des serveurs.