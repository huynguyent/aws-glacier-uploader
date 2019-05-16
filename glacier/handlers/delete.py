import boto3

from glacier.printer import success


def handler(args):
    client = boto3.client('glacier')
    vault_name, archive_id = parse_args(args)
    if archive_id is None:
        client.delete_vault(vaultName=vault_name)
        success(f"Vault {vault_name} has been deleted")
    else:
        client.delete_archive(vaultName=vault_name, archiveId=archive_id)
        success(f"Archive {archive_id} has been deleted from {vault_name}")


def parse_args(args):
    vault_name = args['<vault_name>']
    archive_id = args['<archive_id>']
    return vault_name, archive_id
