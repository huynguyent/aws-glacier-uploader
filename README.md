# aws-glacier-uploader
A command-line tool that performs multipart upload to AWS Glacier, a feature that is not natively supported by AWS official CLI.

This tool simplifies the multipart upload process, which would otherwise be a series of tedious  steps such as split files, upload parts, calculate checksums, ...

## Commands

```bash
Usage:
    glacier upload [options] <vault_name> <file_name>
    glacier create [options] <vault_name>
    glacier list [options]
    glacier help

Options:
    -r --region <aws_region>                    Your AWS region
    -a --account-id <account_id>                Your AWS account ID [default: -]
    -d --desciption <description>               The archive description that you are uploading
    -c --concurrency <concurrency>              The number of upload jobs to run in parallel [default: 10]
```
