# aws-glacier-uploader
A command-line tool that performs multipart upload to AWS Glacier, a feature that is not natively supported by AWS official CLI.

This tool simplifies the multipart upload process, which would otherwise be a series of tedious  steps such as split files, upload parts, calculate checksums, ... The upload process also utilizes multithreading to maximize upload speed.  


## Getting started
### Prerequisite
Make sure you have installed the following:
* `python3`
* `pip3`
* `aws-cli` - to configure your credentials

### Installation
#### Install with pip
```bash
python3 -m pip install git+ssh://git@github.com:huynguyent/aws-glacier-uploader.git
```

#### Manual installation (for development)
```bash
git clone https://github.com/huynguyent/aws-glacier-uploader.git
cd aws-glacier-uploader
python3 setup.py develop
```

#### Uninstall
```bash
pip3 uninstall aws-glacier-uploader
```


## Commands

```bash
Usage:
    glacier upload [options] <vault_name> <file_name>
    glacier list
    glacier list <vault_name>
    glacier create <vault_name>
    glacier delete <vault_name> [<archive_id>]

Options:
    -d --description <description>                      The archive description that you are uploading
    -c --concurrency <concurrency>                      The number of upload jobs to run in parallel [default: 10]
```
