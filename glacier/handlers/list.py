import boto3
from glacier.printer import success
from terminaltables import AsciiTable
import humanize


def handler(args):
    client = boto3.client('glacier')
    if args['<vault_name>']:
        pass
    else:
        pages = list_vaults(client)
        display_vaults_information(pages)


def list_vaults(client):
    paginator = client.get_paginator('list_vaults')
    page_iterator = paginator.paginate()
    return list(page_iterator)


def display_vaults_information(pages):
    table = [
        ['Vault ARN', 'Vault name', 'Creation date', 'Archives', 'Size']
    ]
    for page in pages:
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
