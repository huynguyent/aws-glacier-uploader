"""Glacier: An easy tool to work with AWS Glacier.

Usage:
    glacier create-vault [options] --vault-name <vault_name>
    glacier help

Options:
    --region aws_region
    --account-id <account_id>   Your AWS account ID [default: -]
"""

import sys
import pkg_resources
from docpie import docpie
from glacier.create_vault import create_vault


def main(argv=sys.argv):
    version = pkg_resources.require("aws-glacier-tool")[0].version
    args = docpie(__doc__, argv=argv, version=version)
    if args["create-vault"]:
        account_id = args['--account-id']
        vault_name = args['<vault_name>']
        create_vault(account_id, vault_name)
    else:
        exit(__doc__)
