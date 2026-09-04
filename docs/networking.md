# Réseau informatique

## Présentation

Le réseau informatique permet à plusieurs machines de communiquer entre elles.

Grâce au réseau, les ordinateurs peuvent échanger des données, accéder à des services et communiquer avec Internet.

Les applications modernes reposent largement sur les réseaux pour fonctionner.

---

## Adresse IP

Une adresse IP identifie de manière unique un appareil sur un réseau.

Il existe deux versions principales :

- IPv4
- IPv6

Une adresse IPv4 est composée de quatre nombres séparés par des points.

Exemple :

192.168.1.10

Les adresses IPv6 sont plus longues et permettent de gérer un nombre beaucoup plus important d'équipements.

---

## Adresse publique et adresse privée

Une adresse IP privée est utilisée à l'intérieur d'un réseau local.

Elle n'est pas accessible directement depuis Internet.

Les plages privées les plus courantes sont :

- 10.0.0.0/8
- 172.16.0.0/12
- 192.168.0.0/16

Une adresse publique est accessible depuis Internet.

---

## Le masque de sous-réseau

Le masque de sous-réseau permet de déterminer quelles machines appartiennent au même réseau.

Il est souvent représenté avec la notation CIDR.

Exemples :

192.168.1.0/24

10.0.0.0/16

---

## Les ports

Un port permet d'identifier un service sur une machine.

Plusieurs applications peuvent fonctionner sur la même adresse IP grâce aux ports.

Quelques ports courants :

- 22 : SSH
- 53 : DNS
- 80 : HTTP
- 443 : HTTPS
- 3306 : MySQL
- 5432 : PostgreSQL
- 6379 : Redis

---

## Les protocoles

Les protocoles définissent les règles de communication entre les machines.

Les principaux protocoles sont :

- TCP
- UDP
- HTTP
- HTTPS
- FTP
- SSH
- DNS

Chaque protocole répond à un besoin spécifique.

---

## TCP

TCP est un protocole fiable.

Il garantit que les données arrivent dans le bon ordre et sans perte.

Il est utilisé par la majorité des applications web.

---

## UDP

UDP est un protocole plus rapide que TCP.

Il ne garantit pas la réception des données.

Il est principalement utilisé pour :

- la vidéo
- la voix sur IP
- les jeux en ligne

---

## HTTP

HTTP est le protocole utilisé pour les sites web.

Il fonctionne généralement sur le port 80.

HTTP transmet les données en clair.

---

## HTTPS

HTTPS est une version sécurisée de HTTP.

Les échanges sont chiffrés grâce au protocole TLS.

HTTPS fonctionne généralement sur le port 443.

Aujourd'hui, la majorité des sites utilisent HTTPS.

---

## DNS

Le DNS permet de traduire un nom de domaine en adresse IP.

Par exemple :

www.microsoft.com

est converti en une adresse IP compréhensible par les ordinateurs.

Sans DNS, il faudrait mémoriser les adresses IP de tous les sites Internet.

---

## Le routage

Le routage permet de faire circuler les paquets entre différents réseaux.

Les routeurs choisissent le meilleur chemin jusqu'à la destination.

---

## Les pare-feu

Un pare-feu contrôle le trafic réseau.

Il autorise ou bloque certaines connexions selon des règles définies.

Les pare-feu améliorent la sécurité des infrastructures.

---

## Les réseaux dans Docker

Docker crée automatiquement un réseau virtuel pour les conteneurs.

Les conteneurs d'un même réseau peuvent communiquer entre eux.

Il est possible de créer plusieurs réseaux pour isoler différentes applications.

Commande :

docker network create backend

---

## Les réseaux dans Kubernetes

Dans Kubernetes, chaque Pod possède une adresse IP.

Les Pods communiquent grâce au réseau du cluster.

Les Services permettent d'exposer les applications sans dépendre directement des adresses IP des Pods.

---

## Les réseaux dans Azure

Azure fournit plusieurs services réseau.

Parmi les plus utilisés :

- Virtual Network
- Network Security Groups
- Load Balancer
- Application Gateway

Ces services permettent de connecter et protéger les ressources Azure.

---

## Outils de diagnostic

Afficher la configuration réseau :

ip addr

Afficher les connexions réseau :

ss -tuln

Tester une connexion :

ping google.com

Afficher le chemin d'un paquet :

traceroute google.com

Résoudre un nom de domaine :

nslookup google.com

Télécharger une page web :

curl https://www.microsoft.com

---

## Bonnes pratiques

Il est recommandé de :

- utiliser HTTPS plutôt que HTTP ;
- limiter les ports ouverts ;
- protéger les serveurs avec un pare-feu ;
- segmenter les réseaux ;
- surveiller le trafic réseau ;
- documenter les règles de sécurité.

---

## Résumé

Le réseau permet aux machines de communiquer.

Les principaux concepts à retenir sont :

- une adresse IP identifie une machine ;
- un port identifie un service ;
- TCP garantit la fiabilité des échanges ;
- UDP privilégie la rapidité ;
- DNS traduit les noms de domaine en adresses IP ;
- HTTPS sécurise les communications ;
- les pare-feu protègent les réseaux ;
- Docker, Kubernetes et Azure disposent de leurs propres mécanismes réseau.