import json

import boto3
import humanize
from terminaltables import AsciiTable

from glacier.printer import success


def handler(args):
    client = boto3.client('glacier')
    if args['<vault_name>']:
        vault_name = args['<vault_name>']
        list_archives_in_vault(client, vault_name)
    else:
        pages = list_vaults(client)
        display_vaults_information(pages)


def list_archives_in_vault(client, vault_name):
    inventory_job = get_latest_inventory_job(client, vault_name)
    if inventory_job is None:
        client.initiate_job(vaultName=vault_name, jobParameters={"Type": "inventory-retrieval"})
        success(
            "An inventory retrieval request for this vault has been sent. "
            "It typically takes about 4 hours for AWS to process the request. "
            "Please check back again later.")
    else:
        job_id = inventory_job['JobId']
        archive_list = get_archive_list(client, vault_name, job_id)
        display_archive_list(archive_list)


def display_archive_list(archive_list):
    table = [
        ['Archive Id', 'Description', 'Creation date', 'Size']
    ]
    for archive in archive_list:
        row = [
            archive['ArchiveId'],
            archive['ArchiveDescription'],
            archive['CreationDate'],
            humanize.naturalsize(archive['Size'], binary=True, gnu=True)

        ]
        table.append(row)
    print(AsciiTable(table).table)
    success(f"Total: {len(table) - 1} archive(s)")


def get_archive_list(client, vault_name, job_id):
    job_output = client.get_job_output(vaultName=vault_name, jobId=job_id)
    job_body = json.loads(job_output['body'].read().decode("utf-8"))
    return job_body['ArchiveList']


def get_latest_inventory_job(client, vault_name):
    jobs = client.list_jobs(vaultName=vault_name)['JobList']
    inventory_jobs = [job for job in jobs if job.get('Action') == 'InventoryRetrieval' and job.get('Completed') is True]
    return max(inventory_jobs, key=lambda job: job.get('CompletionDate'), default=None)


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
