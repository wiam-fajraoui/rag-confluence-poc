# Fondations Terraform — RAG Confluence

Ce dossier decrit, sous forme de code (Infrastructure as Code), les
briques Azure de base du projet : un groupe de ressources, une
instance Azure AI Search, et une ressource Azure OpenAI avec un
modele de chat deploye.

## Portee (volontairement limitee a ce stade)

Conforme au livrable "fondations Terraform" de la Phase 2 de la
roadmap du stage : le groupe de ressources et les briques de base.
Ne couvre PAS encore : le reseau, les pipelines CI/CD, le calcul
(Docker Compose / AKS) -- prevus en Phase 6.

## Prealable

- Terraform installe (>= 1.5)
- Azure CLI installe et connectee : `az login`
- Un abonnement Azure actif (teste avec Azure for Students)

⚠️ Ce code n'a pas pu etre execute ni valide dans l'environnement de
redaction (pas d'acces reseau ni d'identifiants Azure). Il est ecrit
a partir de la syntaxe standard du provider `azurerm` et des noms de
ressources reellement crees manuellement pendant le stage, mais une
premiere execution de validation (`terraform plan`) reste necessaire
avant de le considerer fiable.

## Utilisation

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

Les noms de ressources par defaut (`variables.tf`) utilisent un
suffixe `-tf`, different des ressources deja creees manuellement
(`rag-poc-wiam`, `rag-poc-wiam-openai`) -- pour eviter tout conflit
de nom et pouvoir valider ce code sans toucher a l'environnement de
travail actuel.

## Recuperer les identifiants pour .env

```bash
terraform output -raw search_service_endpoint
terraform output -raw search_service_primary_key
terraform output -raw openai_endpoint
terraform output -raw openai_primary_key
terraform output -raw openai_deployment_name
```

## Point d'attention specifique a ce projet : le quota Azure OpenAI

Lors de la mise en place manuelle, les types de deploiement
"GlobalStandard" et "Standard" ont tous deux echoue avec l'erreur
"Aucun quota disponible dans la region selectionnee", quelle que
soit la region testee (Germany West Central, East US 2, Sweden
Central). Seul "DataZoneStandard" a fonctionne. La variable
`openai_deployment_sku_name` est donc definie par defaut sur
"DataZoneStandard" -- **a revalider** si ce code est utilise sur un
autre abonnement (notamment le futur tenant Bacab Consulting), dont
les quotas peuvent etre differents.

## Etat par rapport aux ressources existantes

Les ressources actuellement utilisees par le projet
(`rag-poc-wiam`, `rag-poc-wiam-openai`) ont ete creees manuellement
via le portail Azure, pas par ce code. Ce dossier Terraform n'est
donc pas encore la source de verite de l'infrastructure reelle du
projet -- c'est une premiere version a valider, avant de decider
si les ressources existantes doivent etre importees
(`terraform import`) ou si ce code servira surtout de base pour la
migration vers le tenant Azure officiel de Bacab Consulting.