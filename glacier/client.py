import boto3
import botocore.exceptions
from glacier.printer import fatal


def create_glacier_client():
    try:
        glacier = boto3.client('glacier')
        return glacier
    except botocore.exceptions.NoRegionError:
        fatal('You must specify a region. You can also configure your region by running "aws configure".')

    except Exception as ex:
        fatal(str(ex))
