import os
import boto3
from botocore.utils import calculate_tree_hash
from glacier.printer import success, info
from glacier.models.archive_part import ArchivePart

PART_COUNT_LIMIT = 10000


def handler(args):
    vault_name, file_name, description, concurrency = parse_args(args)
    client = boto3.client('glacier')
    response = upload_archive(client, vault_name, file_name, description, concurrency)
    success(f"{file_name} have been uploaded to Glacier at {response['location']}")


def upload_archive(client, vault_name, file_name, description, concurrency):
    file_size = os.stat(file_name).st_size
    part_size = calculate_part_size(file_size)
    parts = generate_archive_parts(file_size, part_size)

    info('Initiating multipart upload')
    upload_id = client.initiate_multipart_upload(vaultName=vault_name, partSize=str(part_size),
                                                 archiveDescription=description)['uploadId']

    for archive_part in parts:
        info(f'Uploading part {archive_part.order + 1} (of {len(parts)})')
        data = read_bytes(file_name, archive_part.start_byte, archive_part.part_size)
        client.upload_multipart_part(vaultName=vault_name, uploadId=upload_id, range=archive_part.range, body=data)
        info(f'Finished uploading part {archive_part.order + 1} (of {len(parts)})')

    info('Verifying checksum')
    checksum = calculate_tree_hash(open(file_name, 'rb'))
    return client.complete_multipart_upload(vaultName=vault_name, uploadId=upload_id, archiveSize=str(file_size),
                                            checksum=checksum)


def generate_archive_parts(file_size, part_size):
    parts = []
    order = 0
    start_byte = 0

    while start_byte + part_size < file_size:
        range = f"bytes {start_byte}-{start_byte + part_size - 1}/*"
        archive_part = ArchivePart(order, start_byte, part_size, range)
        order += 1
        start_byte = start_byte + part_size
        parts.append(archive_part)

    final_part_size = file_size - start_byte
    range = f"bytes {start_byte}-{start_byte + final_part_size - 1}/*"
    archive_part = ArchivePart(order, start_byte, final_part_size, range)
    parts.append(archive_part)

    return parts


def calculate_part_size(file_size):
    part_size = 1024 ** 2   # 1 MB
    while (file_size / part_size) > PART_COUNT_LIMIT:
        part_size *= 2
    return part_size


def read_bytes(file_name, start_byte, size):
    file = open(file_name, 'rb')
    file.seek(start_byte)
    data = file.read(size)
    file.close()
    return data


def parse_args(args):
    vault_name = args['<vault_name>']
    file_name = args['<file_name>']
    description = args['--description'] if args['--description'] else ''
    concurrency = args['--concurrency']
    return vault_name, file_name, description, concurrency
