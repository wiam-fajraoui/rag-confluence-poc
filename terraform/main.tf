# -----------------------------
# Groupe de ressources
# -----------------------------

resource "azurerm_resource_group" "this" {
  name     = var.resource_group_name
  location = var.location
}

# -----------------------------
# Azure AI Search
# -----------------------------

resource "azurerm_search_service" "this" {
  name                = var.search_service_name
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  sku                 = var.search_sku
}

# -----------------------------
# Azure OpenAI
# -----------------------------

resource "azurerm_cognitive_account" "openai" {
  name                = var.openai_account_name
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  kind                = "OpenAI"
  sku_name            = var.openai_sku
}

resource "azurerm_cognitive_deployment" "chat_model" {
  name                 = var.openai_model_name
  cognitive_account_id = azurerm_cognitive_account.openai.id

  model {
    format  = "OpenAI"
    name    = var.openai_model_name
    version = var.openai_model_version
  }

  scale {
    type     = var.openai_deployment_sku_name
    capacity = var.openai_deployment_capacity
  }
}
