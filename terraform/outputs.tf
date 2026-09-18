output "resource_group_name" {
  description = "Nom du groupe de ressources cree"
  value       = azurerm_resource_group.this.name
}

output "search_service_endpoint" {
  description = "A utiliser comme AZURE_SEARCH_ENDPOINT dans .env"
  value       = "https://${azurerm_search_service.this.name}.search.windows.net"
}

output "search_service_primary_key" {
  description = "A utiliser comme AZURE_SEARCH_API_KEY dans .env"
  value       = azurerm_search_service.this.primary_key
  sensitive   = true
}

output "openai_endpoint" {
  description = "A utiliser comme AZURE_OPENAI_ENDPOINT dans .env"
  value       = azurerm_cognitive_account.openai.endpoint
}

output "openai_primary_key" {
  description = "A utiliser comme AZURE_OPENAI_API_KEY dans .env"
  value       = azurerm_cognitive_account.openai.primary_access_key
  sensitive   = true
}

output "openai_deployment_name" {
  description = "A utiliser comme AZURE_OPENAI_DEPLOYMENT_NAME dans .env"
  value       = azurerm_cognitive_deployment.chat_model.name
}
