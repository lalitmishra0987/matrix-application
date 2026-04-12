output "application_name" {
  value = var.application_name
}
output "primary_region" {
  value = var.primary_region
}
output "primary_location" {
  value = var.primary_location
}
output "random_suffix" {
  value = random_string.suffix.result
}
output "resource_group_name" {
  value = azurerm_resource_group.main.name
}
output "container_registry_name" {
  value = azurerm_container_registry.main.name
}
output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}
