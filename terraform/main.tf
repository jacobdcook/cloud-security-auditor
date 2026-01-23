provider "azurerm" {
  features {}
}

resource "azurerm_storage_account" "insecure_storage" {
  name                     = "insecurestorageacct"
  resource_group_name      = "security-lab-rg"
  location                 = "West US"
  account_tier             = "Standard"
  account_replication_type = "LRS"

  # MISCONFIGURATION: Public access allowed
  allow_blob_public_access = true
}

resource "azurerm_network_security_group" "insecure_nsg" {
  name                = "insecure-nsg"
  location            = "West US"
  resource_group_name = "security-lab-rg"

  security_rule {
    name                       = "allow-ssh-all"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}
