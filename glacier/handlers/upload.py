import boto3
from glacier.printer import success, info


def handler(args):
    vault_name = args['<vault_name>']
    file_name = args['<file_name>']
    description = args['--description'] if args['--description'] else ''
    concurrency = args['--concurrency']
    client = boto3.client('glacier')

    response = upload_archive(client, vault_name, file_name, description, concurrency)
    success(f"File have been uploaded to Glacier at {response['location']}")


def upload_archive(client, vault_name, file_name, description, concurrency):
    file = open(file_name, 'rb')
    data = file.read()
    file.close()
    info(f"Uploading file to vault {vault_name}")
    response = client.upload_archive(
        vaultName=vault_name,
        archiveDescription=description,
        body=data
    )
    return response
