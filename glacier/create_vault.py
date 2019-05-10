from glacier import client
from glacier.printer import success, fatal
import botocore.exceptions


def create_vault(account_id, vault_name):
    glacier_client = client.create_glacier_client()
    try:
        response = glacier_client.create_vault(
            accountId=account_id,
            vaultName=vault_name,
        )
        success(f"A new vault has been created at: {response['location']}")
    except botocore.exceptions.NoCredentialsError:
        fatal('Unable to locate credentials. You can configure credentials by running "aws configure".')
    except Exception as ex:
        fatal(str(ex))
