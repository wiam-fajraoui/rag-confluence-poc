# Python

## Présentation

Python est un langage de programmation interprété, polyvalent et open source.

Il est reconnu pour sa syntaxe simple et sa grande lisibilité.

Python est utilisé dans de nombreux domaines comme le développement web, l'intelligence artificielle, la science des données, l'automatisation, la cybersécurité et le DevOps.

Grâce à son important écosystème de bibliothèques, Python est aujourd'hui l'un des langages les plus populaires.

---

## Installation

Python peut être installé depuis le site officiel ou à l'aide d'un gestionnaire de paquets.

La version installée peut être vérifiée avec la commande :

python --version

Ou :

python3 --version

---

## Exécution d'un programme

Un programme Python est enregistré dans un fichier portant l'extension .py.

Pour exécuter un programme :

python main.py

Sous certaines distributions Linux :

python3 main.py

---

## Variables

Les variables permettent de stocker des informations.

Python détermine automatiquement le type d'une variable.

Exemple :

nom = "Alice"

age = 25

est_connecte = True

---

## Les types de données

Les principaux types sont :

- int
- float
- str
- bool
- list
- tuple
- dict
- set

Chaque type possède ses propres méthodes et caractéristiques.

---

## Les conditions

Les conditions permettent d'exécuter du code selon une expression logique.

Python utilise principalement :

if

elif

else

Exemple :

if age >= 18:
    print("Majeur")
else:
    print("Mineur")

---

## Les boucles

Python propose deux principales boucles.

La boucle for permet de parcourir une collection.

La boucle while répète une action tant qu'une condition est vraie.

Exemple :

for i in range(5):
    print(i)

---

## Les fonctions

Une fonction permet de regrouper plusieurs instructions.

Elle facilite la réutilisation du code.

Exemple :

def addition(a, b):
    return a + b

Les fonctions peuvent recevoir des paramètres et retourner une valeur.

---

## Les listes

Une liste est une collection ordonnée et modifiable.

Exemple :

fruits = ["Pomme", "Banane", "Orange"]

Quelques méthodes utiles :

append()

remove()

sort()

pop()

---

## Les dictionnaires

Un dictionnaire stocke des données sous forme de clé-valeur.

Exemple :

utilisateur = {
    "nom": "Alice",
    "age": 25
}

Les dictionnaires sont très utilisés pour représenter des objets.

---

## Les classes

Python prend en charge la programmation orientée objet.

Une classe décrit un modèle permettant de créer plusieurs objets.

Exemple :

class Utilisateur:

    def __init__(self, nom):
        self.nom = nom

Les objets sont créés à partir des classes.

---

## Les modules

Les modules permettent de réutiliser du code.

Importer un module :

import math

Ou :

from pathlib import Path

Python possède une bibliothèque standard très riche.

---

## Les environnements virtuels

Un environnement virtuel permet d'isoler les dépendances d'un projet.

Créer un environnement virtuel :

python -m venv .venv

Activer l'environnement sous Windows :

.venv\Scripts\activate

Sous Linux :

source .venv/bin/activate

---

## Les dépendances

Les bibliothèques Python sont généralement installées avec pip.

Installer une bibliothèque :

pip install requests

Lister les dépendances :

pip list

Exporter les dépendances :

pip freeze > requirements.txt

Installer les dépendances d'un projet :

pip install -r requirements.txt

---

## Gestion des exceptions

Les exceptions permettent de gérer les erreurs.

Exemple :

try:
    resultat = 10 / 0
except ZeroDivisionError:
    print("Division impossible")

La gestion des exceptions améliore la robustesse des applications.

---

## Les fichiers

Python permet de lire et d'écrire des fichiers.

Exemple :

with open("notes.txt", "r") as fichier:
    contenu = fichier.read()

L'instruction with ferme automatiquement le fichier.

---

## Les bibliothèques populaires

Quelques bibliothèques couramment utilisées :

- requests
- numpy
- pandas
- matplotlib
- flask
- fastapi
- django
- scikit-learn
- transformers
- sentence-transformers

---

## Python et l'intelligence artificielle

Python est le langage le plus utilisé dans le domaine de l'intelligence artificielle.

Il permet de développer des modèles de Machine Learning, de Deep Learning et des applications basées sur les modèles de langage.

De nombreuses bibliothèques facilitent le développement d'applications RAG.

---

## Python et le DevOps

Python est largement utilisé pour automatiser des tâches d'administration système.

Il permet de créer des scripts de déploiement, d'automatiser des tests et d'interagir avec les API des plateformes cloud.

Python est également utilisé avec Docker, Kubernetes et Azure.

---

## Bonnes pratiques

Il est recommandé de :

- respecter la convention PEP 8 ;
- choisir des noms explicites pour les variables ;
- écrire des fonctions courtes ;
- documenter le code important ;
- utiliser un environnement virtuel pour chaque projet ;
- gérer les erreurs avec des exceptions ;
- écrire des tests unitaires lorsque cela est possible.

---

## Résumé

Python est un langage de programmation simple, puissant et polyvalent.

Les principaux concepts à retenir sont :

- les variables stockent les données ;
- les fonctions permettent de réutiliser du code ;
- les classes facilitent la programmation orientée objet ;
- les modules organisent les applications ;
- les environnements virtuels isolent les dépendances ;
- pip permet d'installer les bibliothèques ;
- Python est largement utilisé dans le cloud, le DevOps et l'intelligence artificielle.