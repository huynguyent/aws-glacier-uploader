"""aws-glacier-uploader: A command-line tool that performs multipart upload to AWS Glacier.

Usage:
    glacier upload [options] <vault_name> <file_name>
    glacier list
    glacier list <vault_name>
    glacier create <vault_name>
    glacier delete <vault_name> [<archive_id>]

Options:
    -d --description <description>                      The archive description that you are uploading
    -c --concurrency <concurrency>                      The number of upload jobs to run in parallel [default: 10]
"""

import sys

import botocore.exceptions
import pkg_resources
from docpie import docpie

from glacier.handlers import create, list, upload, delete
from glacier.printer import fatal


def main(argv=sys.argv):
    version = pkg_resources.require("aws-glacier-tool")[0].version
    args = docpie(__doc__, argv=argv, version=version)

    try:
        if args['create']:
            create.handler(args)
        elif args['list']:
            list.handler(args)
        elif args['upload']:
            upload.handler(args)
        elif args['delete']:
            delete.handler(args)
        else:
            print(__doc__)
    except botocore.exceptions.NoRegionError:
        fatal('You must specify a region. You can also configure your region by running "aws configure".')
    except botocore.exceptions.NoCredentialsError:
        fatal('Unable to locate credentials. You can configure credentials by running "aws configure".')
    except Exception as ex:
        fatal(str(ex))
