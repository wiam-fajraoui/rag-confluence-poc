# Monitoring

## Présentation

Le monitoring consiste à surveiller le fonctionnement d'une infrastructure, d'une application ou d'un service.

Son objectif est de détecter rapidement les problèmes, d'analyser les performances et d'assurer la disponibilité des systèmes.

Le monitoring est une pratique essentielle dans les environnements DevOps et Cloud.

---

## Les objectifs

Le monitoring permet notamment de :

- surveiller la disponibilité des services ;
- mesurer les performances ;
- détecter les anomalies ;
- envoyer des alertes ;
- faciliter le diagnostic des incidents.

Une bonne stratégie de monitoring réduit le temps nécessaire pour résoudre les problèmes.

---

## Les métriques

Les métriques représentent des valeurs numériques mesurées dans le temps.

Quelques exemples :

- utilisation du processeur ;
- consommation de mémoire ;
- espace disque disponible ;
- trafic réseau ;
- nombre de requêtes ;
- temps de réponse.

Les métriques permettent d'observer l'évolution d'un système.

---

## Les logs

Les logs enregistrent les événements produits par une application ou un système.

Ils permettent de comprendre ce qui s'est passé lorsqu'une erreur survient.

Les logs peuvent contenir :

- des informations ;
- des avertissements ;
- des erreurs ;
- des événements de sécurité.

Une bonne gestion des logs facilite le dépannage.

---

## Les traces

Les traces permettent de suivre une requête lorsqu'elle traverse plusieurs services.

Elles sont particulièrement utiles dans les architectures distribuées et les microservices.

Les traces facilitent l'identification des ralentissements.

---

## Les tableaux de bord

Les tableaux de bord présentent les métriques sous forme graphique.

Ils permettent de visualiser rapidement l'état d'une infrastructure.

Les équipes peuvent suivre en temps réel les principaux indicateurs.

---

## Les alertes

Les alertes sont déclenchées lorsqu'une condition est remplie.

Par exemple :

- processeur supérieur à 90 % ;
- mémoire insuffisante ;
- service indisponible ;
- temps de réponse trop élevé.

Les alertes permettent d'intervenir avant qu'un incident ne devienne critique.

---

## Prometheus

Prometheus est un système open source de collecte de métriques.

Il interroge régulièrement les applications afin de récupérer leurs indicateurs.

Les données sont stockées dans une base de données spécialisée.

Prometheus est largement utilisé avec Kubernetes.

---

## Grafana

Grafana est une plateforme de visualisation.

Elle permet de créer des tableaux de bord interactifs à partir de nombreuses sources de données.

Grafana est souvent utilisé avec Prometheus.

Les tableaux de bord facilitent le suivi des performances.

---

## Alertmanager

Alertmanager complète Prometheus.

Il reçoit les alertes générées par Prometheus.

Il peut ensuite envoyer des notifications par :

- courrier électronique ;
- Slack ;
- Microsoft Teams ;
- Webhook.

Les alertes peuvent être regroupées afin d'éviter les notifications répétitives.

---

## ELK Stack

La pile ELK est une solution de gestion des logs.

Elle est composée de :

- Elasticsearch ;
- Logstash ;
- Kibana.

Logstash collecte les données.

Elasticsearch les indexe.

Kibana permet de les visualiser.

---

## OpenTelemetry

OpenTelemetry est un standard permettant de collecter :

- des métriques ;
- des logs ;
- des traces.

Il facilite l'observabilité des applications modernes.

De nombreux outils sont compatibles avec OpenTelemetry.

---

## Monitoring des applications

Les applications peuvent exposer leurs propres métriques.

Par exemple :

- nombre d'utilisateurs connectés ;
- temps moyen d'une requête ;
- nombre d'erreurs ;
- nombre de transactions.

Ces informations complètent les métriques système.

---

## Monitoring des serveurs

Les serveurs sont surveillés afin de vérifier :

- le processeur ;
- la mémoire ;
- le disque ;
- le réseau ;
- les processus.

Cette surveillance permet d'anticiper les problèmes matériels ou logiciels.

---

## Monitoring de Docker

Les conteneurs Docker peuvent être surveillés individuellement.

Les métriques les plus courantes concernent :

- l'utilisation CPU ;
- la mémoire ;
- le trafic réseau ;
- le stockage.

Ces informations permettent d'identifier les conteneurs consommant le plus de ressources.

---

## Monitoring de Kubernetes

Kubernetes fournit de nombreuses métriques sur les Pods, les Nodes et les Services.

Les administrateurs peuvent surveiller :

- les Pods en erreur ;
- les redémarrages ;
- les ressources consommées ;
- les déploiements.

Prometheus est souvent utilisé pour collecter ces informations.

---

## Monitoring d'Azure

Microsoft Azure propose Azure Monitor.

Azure Monitor collecte les métriques, les logs et les événements provenant des ressources Azure.

Il peut également envoyer des alertes et afficher des tableaux de bord.

Azure Log Analytics permet d'analyser les journaux de manière avancée.

---

## Les indicateurs clés

Quelques indicateurs fréquemment surveillés :

- disponibilité ;
- temps de réponse ;
- taux d'erreur ;
- charge CPU ;
- mémoire utilisée ;
- espace disque ;
- trafic réseau.

Ces indicateurs donnent une vision globale de la santé d'un système.

---

## Observabilité

L'observabilité est la capacité à comprendre l'état interne d'un système à partir des informations qu'il produit.

Elle repose généralement sur trois éléments :

- les métriques ;
- les logs ;
- les traces.

Une bonne observabilité facilite la résolution des incidents.

---

## Avantages

Le monitoring présente plusieurs avantages :

- détection rapide des incidents ;
- amélioration des performances ;
- meilleure disponibilité ;
- réduction du temps de résolution ;
- meilleure compréhension du comportement des applications.

---

## Bonnes pratiques

Il est recommandé de :

- surveiller les services critiques ;
- définir des seuils d'alerte adaptés ;
- centraliser les logs ;
- créer des tableaux de bord simples ;
- tester régulièrement les alertes ;
- conserver un historique des métriques ;
- surveiller également les applications, pas uniquement les serveurs.

---

## Résumé

Le monitoring permet de surveiller une infrastructure et ses applications.

Les principaux concepts à retenir sont :

- les métriques mesurent les performances ;
- les logs enregistrent les événements ;
- les traces suivent les requêtes ;
- Prometheus collecte les métriques ;
- Grafana affiche les tableaux de bord ;
- Alertmanager gère les notifications ;
- ELK centralise les journaux ;
- Azure Monitor surveille les ressources Azure ;
- l'observabilité repose sur les métriques, les logs et les traces.