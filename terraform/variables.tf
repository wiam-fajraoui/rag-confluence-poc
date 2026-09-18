# -----------------------------
# Groupe de ressources
# -----------------------------

variable "resource_group_name" {
  description = "Nom du groupe de ressources Azure"
  type        = string
  default     = "rg-rag-poc-tf"
}

variable "location" {
  description = "Region Azure. Germany West Central confirmee compatible avec Azure AI Search (tier Free) et Azure OpenAI sur un abonnement Azure for Students -- a revalider si le tenant Bacab utilise une autre region."
  type        = string
  default     = "germanywestcentral"
}

# -----------------------------
# Azure AI Search
# -----------------------------

variable "search_service_name" {
  description = "Nom du service Azure AI Search (doit etre unique globalement)"
  type        = string
  default     = "rag-poc-wiam-tf"
}

variable "search_sku" {
  description = "Niveau tarifaire Azure AI Search. 'free' = 50 Mo, 3 index max, un seul service gratuit par abonnement."
  type        = string
  default     = "free"
}

# -----------------------------
# Azure OpenAI
# -----------------------------

variable "openai_account_name" {
  description = "Nom de la ressource Azure OpenAI (doit etre unique globalement)"
  type        = string
  default     = "rag-poc-wiam-openai-tf"
}

variable "openai_sku" {
  description = "Niveau tarifaire Azure OpenAI. Pas de niveau gratuit dedie -- facturation a l'usage (S0)."
  type        = string
  default     = "S0"
}

variable "openai_model_name" {
  description = "Nom du modele de chat a deployer"
  type        = string
  default     = "gpt-4o-mini"
}

variable "openai_model_version" {
  description = "Version du modele"
  type        = string
  default     = "2024-07-18"
}

variable "openai_deployment_sku_name" {
  description = <<-EOT
    Type de deploiement Azure OpenAI (utilise comme "type" dans le
    bloc scale de azurerm_cognitive_deployment -- le nom de cette
    variable garde "sku" par habitude du vocabulaire Azure, mais le
    provider terraform installe, v3.117.1, utilise le terme "scale").
    Determine empiriquement lors de la mise en place manuelle :
    "GlobalStandard" et "Standard" ont tous deux echoue par manque de
    quota disponible sur l'abonnement Azure for Students (message :
    "Aucun quota disponible dans la
    region selectionnee"), quelle que soit la region testee.
    "DataZoneStandard" a fonctionne. Cette contrainte est propre a
    l'abonnement / au moment du test -- a revalider sur le tenant
    Bacab, qui peut avoir des quotas differents.
  EOT
  type        = string
  default     = "DataZoneStandard"
}

variable "openai_deployment_capacity" {
  description = "Limite de debit en milliers de tokens par minute (K TPM)"
  type        = number
  default     = 30
}
