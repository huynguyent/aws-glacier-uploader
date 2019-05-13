import os
from multiprocessing.dummy import Pool

import boto3
from botocore.utils import calculate_tree_hash
from tqdm import tqdm

from glacier.models.archive_part import ArchivePart
from glacier.printer import success, info

PART_COUNT_LIMIT = 10000


def handler(args):
    vault_name, file_name, description, concurrency = parse_args(args)
    client = boto3.client('glacier')
    response = upload_archive(client, vault_name, file_name, description, concurrency)
    success(f"{file_name} have been uploaded to Glacier at {response['location']}")


def upload_archive(client, vault_name, file_name, description, concurrency):
    file_size = os.stat(file_name).st_size
    part_size = calculate_part_size(file_size)

    info('Initiating multipart upload')
    upload_id = client.initiate_multipart_upload(vaultName=vault_name, partSize=str(part_size),
                                                 archiveDescription=description)['uploadId']

    parts = generate_archive_parts(vault_name, file_name, upload_id, file_size, part_size)
    base_name = os.path.basename(file_name)
    info(f'Uploading {base_name} in {len(parts)} parts')
    with Pool(concurrency) as pool:
        pbar = tqdm(total=file_size, unit="", unit_scale=True, dynamic_ncols=True,
                    bar_format='{percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} ({rate_fmt})')
        for uploaded_size in pool.imap_unordered(upload_archive_part, parts):
            pbar.update(uploaded_size)
        pbar.close()

    info('Verifying checksum')
    checksum = calculate_tree_hash(open(file_name, 'rb'))
    return client.complete_multipart_upload(vaultName=vault_name, uploadId=upload_id, archiveSize=str(file_size),
                                            checksum=checksum)


def upload_archive_part(archive_part):
    client = boto3.client('glacier')
    data = read_bytes(archive_part.file_name, archive_part.start_byte, archive_part.part_size)
    client.upload_multipart_part(vaultName=archive_part.vault_name, uploadId=archive_part.upload_id,
                                 range=archive_part.range,
                                 body=data)
    return archive_part.part_size


def generate_archive_parts(vault_name, file_name, upload_id, file_size, part_size):
    parts = []
    order = 0
    start_byte = 0

    while start_byte + part_size < file_size:
        range = f"bytes {start_byte}-{start_byte + part_size - 1}/*"
        archive_part = ArchivePart(order, vault_name, file_name, upload_id, start_byte, part_size, range)
        order += 1
        start_byte = start_byte + part_size
        parts.append(archive_part)

    final_part_size = file_size - start_byte
    range = f"bytes {start_byte}-{start_byte + final_part_size - 1}/*"
    archive_part = ArchivePart(order, vault_name, file_name, upload_id, start_byte, final_part_size, range)
    parts.append(archive_part)

    return parts


def calculate_part_size(file_size):
    part_size = 1 * (1024 ** 2)  # 1 MB
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
    concurrency = int(args['--concurrency'])
    return vault_name, file_name, description, concurrency
