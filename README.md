# aws-glacier-uploader
A command-line tool that performs multipart upload to AWS Glacier, a feature that is not natively supported by AWS official CLI.

This tool simplifies the multipart upload process, which would otherwise be a series of tedious  steps such as split files, upload parts, calculate checksums, ...

## Commands

```bash
Usage:
    glacier create [options] <vault_name>
    glacier list [options]
    glacier help
Options:
    --region <aws_region>       Your AWS region
    --account-id <account_id>   Your AWS account ID [default: -]


```
