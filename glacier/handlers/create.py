import boto3
from glacier.printer import success


def create_vault(vault_name):
    account_id = '-'
    client = boto3.client('glacier')
    response = client.create_vault(
        accountId=account_id,
        vaultName=vault_name,
    )
    success(f"A new vault has been created at: {response['location']}")
