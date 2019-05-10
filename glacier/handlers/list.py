import boto3
from glacier.printer import success
from terminaltables import AsciiTable
import humanize


def list_vaults():
    client = boto3.client('glacier')
    table = [
        ['Vault ARN', 'Vault name', 'Creation date', 'Archives', 'Size']
    ]
    paginator = client.get_paginator('list_vaults')
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
    print(AsciiTable(table).table)
    success(f"Total: {len(table) - 1} vault(s)")

