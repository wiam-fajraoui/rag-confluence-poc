# Kubernetes Deployment

## Fonctionnement d'un Deployment

Un Deployment est une ressource Kubernetes utilisée pour gérer le déploiement d'une application. Son objectif est de maintenir un nombre défini de réplicas en fonctionnement tout en permettant des mises à jour progressives et des retours en arrière si nécessaire.

Lorsqu'un Deployment est créé, Kubernetes génère automatiquement un ReplicaSet. Ce ReplicaSet est responsable de la création des Pods correspondant à la configuration demandée. Si un Pod est supprimé ou tombe en panne, le ReplicaSet crée automatiquement un nouveau Pod afin de conserver le nombre de réplicas souhaité.

Le Deployment permet également de réaliser des mises à jour progressives, appelées Rolling Updates. Lorsqu'une nouvelle version de l'application est déployée, Kubernetes remplace progressivement les anciens Pods par de nouveaux. Cette approche permet de limiter les interruptions de service et de garantir que l'application reste disponible pendant le déploiement.

Si une erreur est détectée après une mise à jour, Kubernetes permet d'effectuer un Rollback. Le Deployment conserve l'historique des versions précédentes et peut revenir automatiquement à une version stable. Cette fonctionnalité est particulièrement utile lors des déploiements en production où la disponibilité des services est critique.

Le Deployment surveille en permanence l'état souhaité de l'application. Si un administrateur modifie manuellement le nombre de Pods ou supprime certains Pods, Kubernetes compare l'état réel à l'état désiré puis recrée automatiquement les ressources manquantes. Cette capacité d'auto-réparation constitue l'un des principes fondamentaux de Kubernetes.

Les stratégies de déploiement peuvent également être personnalisées. Il est possible de définir le nombre maximal de Pods indisponibles pendant une mise à jour, le nombre maximal de nouveaux Pods créés simultanément ainsi que le délai d'attente avant qu'un Pod soit considéré comme prêt. Ces paramètres permettent d'adapter le comportement du Deployment aux contraintes de disponibilité de chaque application.

## Exemple YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3

  selector:
    matchLabels:
      app: web

  template:
    metadata:
      labels:
        app: web

    spec:
      containers:
      - name: nginx
        image: nginx:latest
```

## Résumé

Le Deployment automatise le déploiement, la mise à jour, le rollback et la haute disponibilité des applications Kubernetes.