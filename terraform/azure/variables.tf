variable "application_name" {
  type        = string
  description = "Name of the application to be deployed"
}
variable "primary_location" {
  type        = string
  description = "Azure region where resources will be deployed"
}
variable "environment_name" {
  type        = string
  description = "Name of the environment (e.g., dev, staging, prod)"
}
variable "primary_region" {
  type        = string
  description = "Primary Azure region for the resources"
}
variable "component_name" {
  type        = string
  description = "Name of the component being deployed"
}
variable "instance" {
  type        = string
  description = "First instance number for the resource group"
}
variable "node_vm_size" {
  type = string
}
variable "system_node_count" {
  type = number
}
variable "app_node_min" {
  type = number
}
variable "app_node_max" {
  type = number
}
