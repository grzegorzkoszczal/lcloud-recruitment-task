# LCloud recruitment task

## TODO list:

### 1. Write a python CLI that can do the following things, work from top to bottom of the list getting each one done before moving to the next (120min):

- List all files in an S3 Bucket
- Upload a local file to a defined location in the bucket
- List an AWS buckets files that match a "filter" regex 
- Delete all files matching a regex from a bucket

Please use following credentials:
    access key id: HIDDEN IN .env
    access key: HIDDEN IN .env

You have access to S3 bucket named “developer-task”, but limited to contents of “a-wing” prefix (directory)
!! Please push your final work to GitHub repo and also use this repository to save your progress of work min 2-3 times !!

### 2*. Please use the ENV variables for configuring the sdk, you can check AWS documents (120min):

    Python SDK: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html 

If you don't have practices with AWS, you have additional 120min for reading AWS documentation.

### 3*. If you have more free time and feel that you can improve your code, you can work more and push code to the same repo with your improvement. (60min)

## How to use Python CLI

### Upload file command syntax

    python3 main.py upload-file --upload-file /home/username/path/file.ext --s3-key file.ext

### List all files command syntax

    python3 main.py list-all-files --list-all

### List files by provided regex

    python3 main.py list-files-by-regex --regex <provided_regex>

### Delete files by provided regex

    python3 main.py delete-files-by-regex --regex <provided_regex>