resource "azurerm_resource_group" "main" {
  name     = "rg-${var.application_name}-${var.component_name}-${var.environment_name}-${var.primary_region}-${var.instance}"
  location = var.primary_location
}

resource "random_string" "suffix" {
  length  = 6
  upper   = false
  special = false
}

resource "azurerm_container_registry" "main" {
  name                = "cr${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Basic"
  admin_enabled       = false
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = "aks-${var.application_name}-${var.environment_name}-${var.primary_region}-${var.instance}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "${var.application_name}aks${var.instance}"
  #  kubernetes_version  = var.kubernetes_version

  # -----------System Node Pool----------------
  # Runs kube-system pods only (CoreDNS, metrics-server, etc) - no user workloads
  default_node_pool {
    name                         = "system"
    vm_size                      = var.node_vm_size
    node_count                   = var.system_node_count
    only_critical_addons_enabled = true

    upgrade_settings {
      max_surge = "33%"
    }
  }

  #----Mananged Identity-----------
  # Azure manages identity - no service principle needed
  # Equivalent to an IAM role on EKS
  identity {
    type = "SystemAssigned"
  }

  #------------Networking-----------------
  #azure CNI = pods get real VNet Ips (needed for Network Policy)
  #calico = enables Kubernetes Network Policy enforcement
  network_profile {
    network_plugin = "azure"
    network_policy = "calico"
  }

  #----------Workload Identity-----------------
  # Allows pods to authenticate to Azure services without secrets
  # Equivalent to IRSA on EKS
  oidc_issuer_enabled       = true
  workload_identity_enabled = true

  #-------------------Auto Upgrade-----------------------
  automatic_upgrade_channel = "patch" #auto apply patch versions only

  tags = {
    Environment = "${var.environment_name}"
  }
}

# ------App node pool-----------------------
# Separate from system pool --aplication workloads run here
# Autoscaling enabled between min and max node count
resource "azurerm_kubernetes_cluster_node_pool" "apps" {
  name                  = "app${var.instance}"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id
  vm_size               = var.node_vm_size
  auto_scaling_enabled  = true
  min_count             = var.app_node_min
  max_count             = var.app_node_max
  mode                  = "User"

  tags = {
    Environment = "${var.environment_name}"
  }
}

resource "azurerm_role_assignment" "aks_acr_pull" {
  principal_id                     = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.main.id
  skip_service_principal_aad_check = true
}
