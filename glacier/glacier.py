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
import botocore.exceptions
from glacier.printer import fatal


def main(argv=sys.argv):
    version = pkg_resources.require("aws-glacier-tool")[0].version
    args = docpie(__doc__, argv=argv, version=version)

    try:
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
    except botocore.exceptions.NoRegionError:
        fatal('You must specify a region. You can also configure your region by running "aws configure".')
    except botocore.exceptions.NoCredentialsError:
        fatal('Unable to locate credentials. You can configure credentials by running "aws configure".')
    except Exception as ex:
        fatal(str(ex))
