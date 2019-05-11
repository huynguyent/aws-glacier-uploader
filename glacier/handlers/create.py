import boto3
from glacier.printer import success


def handler(args):
    vault_name = args['<vault_name>']
    account_id = '-'
    client = boto3.client('glacier')

    response = create_vault(client, vault_name, account_id)
    success(f"A new vault has been created at: {response['location']}")


def create_vault(client, vault_name, account_id):
    response = client.create_vault(
        accountId=account_id,
        vaultName=vault_name,
    )
    return response
