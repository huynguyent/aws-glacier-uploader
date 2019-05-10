from glacier import aws
from glacier.printer import success, fatal
import botocore.exceptions


def upload(vault_name, file_name, description, concurrency):
    client = aws.create_glacier_client()
    try:
        file = open(file_name, 'rb')
        data = file.read()
        response = client.upload_archive(
            vaultName=vault_name,
            archiveDescription=description,
            body=data
        )
        print(response)
    except botocore.exceptions.NoCredentialsError:
        fatal('Unable to locate credentials. You can configure credentials by running "aws configure".')
    except Exception as ex:
        fatal(str(ex))

