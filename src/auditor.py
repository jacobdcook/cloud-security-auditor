from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient
import os

def audit_azure():
    """
    Audits live Azure resources for misconfigurations.
    """
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    if not subscription_id:
        print("Error: AZURE_SUBSCRIPTION_ID not set.")
        return []

    credential = DefaultAzureCredential()
    findings = []

    # Example: Audit Storage Accounts for Public Access
    storage_client = StorageManagementClient(credential, subscription_id)
    print("Auditing Storage Accounts...")
    for account in storage_client.storage_accounts.list():
        if account.allow_blob_public_access:
            findings.append({
                "resource": account.name,
                "type": "Storage Account",
                "issue": "Public Blob Access is allowed",
                "severity": "High"
            })

    # Example: Audit NSGs for insecure ports
    network_client = NetworkManagementClient(credential, subscription_id)
    print("Auditing Network Security Groups...")
    for nsg in network_client.network_security_groups.list_all():
        for rule in nsg.security_rules:
            if rule.access == "Allow" and rule.destination_port_range in ["22", "3389"] and rule.source_address_prefix == "*":
                findings.append({
                    "resource": nsg.name,
                    "type": "NSG Rule",
                    "issue": f"Insecure port {rule.destination_port_range} open to the internet",
                    "severity": "Critical"
                })

    return findings
