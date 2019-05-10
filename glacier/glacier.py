"""Glacier: An easy tool to work with AWS Glacier.

Usage:
    glacier create [options] <vault_name>
    glacier list [options]
    glacier help
Options:
    --region aws_region
    --account-id <account_id>   Your AWS account ID [default: -]
"""

import sys
import pkg_resources
from docpie import docpie
from glacier.handlers.create_vault import create_vault
from glacier.handlers.list_vaults import list_vaults


def main(argv=sys.argv):
    version = pkg_resources.require("aws-glacier-tool")[0].version
    args = docpie(__doc__, argv=argv, version=version)
    account_id = args['--account-id']

    if args["create"]:
        vault_name = args['<vault_name>']
        create_vault(account_id, vault_name)
    elif args["list"]:
        list_vaults(account_id)
    else:
        exit(__doc__)
