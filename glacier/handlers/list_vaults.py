from glacier import client
from glacier.printer import success, fatal
import botocore.exceptions
from terminaltables import AsciiTable
import humanize


def list_vaults(account_id):
    glacier_client = client.create_glacier_client()
    try:
        table = [
            ['Vault ARN', 'Vault name', 'Creation date', 'Archives', 'Size']
        ]
        paginator = glacier_client.get_paginator('list_vaults')
        page_iterator = paginator.paginate()
        for page in page_iterator:
            vaults = page['VaultList']
            for vault in vaults:
                row = [
                    vault['VaultARN'],
                    vault['VaultName'],
                    vault['CreationDate'],
                    vault['NumberOfArchives'],
                    humanize.naturalsize(vault['SizeInBytes'], binary=True, gnu=True)
                ]
                table.append(row)
        success(f"Total: {len(table) - 1} vault(s)")
        print(AsciiTable(table).table)
    except botocore.exceptions.NoCredentialsError:
        fatal('Unable to locate credentials. You can configure credentials by running "aws configure".')
    except Exception as ex:
        fatal(str(ex))
