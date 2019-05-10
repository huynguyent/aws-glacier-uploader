import boto3
from glacier.printer import success, info


def upload(vault_name, file_name, description, concurrency):
    client = boto3.client('glacier')
    file = open(file_name, 'rb')
    data = file.read()
    file.close()
    info(f"Uploading file to vault {vault_name}")
    response = client.upload_archive(
        vaultName=vault_name,
        archiveDescription=description,
        body=data
    )
    success(f"File have been uploaded to Glacier at {response['location']}")
