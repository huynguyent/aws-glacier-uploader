import boto3

from glacier.printer import success


def handler(args):
    client = boto3.client('glacier')
    vault_name = args['<vault_name>']

    response = client.create_vault(vaultName=vault_name)
    success(f"A new vault has been created at: {response['location']}")
