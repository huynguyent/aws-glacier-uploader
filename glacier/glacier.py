"""aws-glacier-uploader: A command-line tool that performs multipart upload to AWS Glacier.

Usage:
    glacier upload [options] <vault_name> <file_name>
    glacier create <vault_name>
    glacier list

Options:
    -d --description <description>              The archive description that you are uploading
    -c --concurrency <concurrency>              The number of upload jobs to run in parallel [default: 10]
"""

import sys
import pkg_resources
from docpie import docpie


def main(argv=sys.argv):
    version = pkg_resources.require("aws-glacier-tool")[0].version
    args = docpie(__doc__, argv=argv, version=version)

    if args['create']:
        from glacier.handlers.create import create_vault
        vault_name = args['<vault_name>']
        create_vault(vault_name)
    elif args['list']:
        from glacier.handlers.list import list_vaults
        list_vaults()
    elif args['upload']:
        from glacier.handlers.upload import upload
        vault_name = args['<vault_name>']
        file_name = args['<file_name>']
        description = args['--description'] if args['--description'] else ''
        concurrency = args['--concurrency']
        upload(vault_name, file_name, description, concurrency)
    else:
        print(__doc__)
