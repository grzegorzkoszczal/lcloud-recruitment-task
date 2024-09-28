import os
import re
import click
import boto3
from botocore.config import Config
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_DEFAULT_REGION')
)

BUCKET_NAME = os.getenv('BUCKET_NAME')
BUCKET_PREFIX = os.getenv('BUCKET_PREFIX')

# Upload a local file to the S3 bucket under the defined location in the prefix
@click.command()
@click.option('--upload-file', type=click.Path(exists=True), help="Upload a local file to the 'a-wing' directory in S3.")
@click.option('--s3-key', required=True, help="The destination key (path) in S3.")
def upload_file(upload_file, s3_key):
    s3_key = BUCKET_PREFIX + s3_key
    try:
        s3_client.upload_file(upload_file, BUCKET_NAME, s3_key)
        print(f"File uploaded to {s3_key}")
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Credentials error: {str(e)}")

@click.command()
@click.option('--list-all', is_flag=True, help="List all files in the 'a-wing' prefix of the bucket.")
def list_all_files(list_all):
    if list_all:
        try:
            response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=BUCKET_PREFIX)
            if 'Contents' in response:
                for item in response['Contents']:
                    print(item['Key'])
            else:
                print("No files found.")
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Credentials error: {str(e)}")

@click.command()
@click.option('--regex', required=True, help="Regex pattern to filter files in the S3 bucket.")
def list_files_by_regex(regex):
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=BUCKET_PREFIX)
        if 'Contents' in response:
            pattern = re.compile(regex)
            matched = False
            for item in response['Contents']:
                if pattern.search(item['Key']):
                    print(item['Key'])
                    matched = True
            if not matched:
                print("No file match the provided regex!")
        else:
            print("No files found.")
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Credentials error: {str(e)}")

@click.command()
@click.option('--regex', required=True, help="Regex pattern to filter and delete files in the S3 bucket.")
def delete_files_by_regex(regex):
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=BUCKET_PREFIX)
        if 'Contents' in response:
            pattern = re.compile(regex)
            keys_to_delete = [item['Key'] for item in response['Contents'] if pattern.search(item['Key'])]
            
            if keys_to_delete:
                delete_response = s3_client.delete_objects(
                    Bucket=BUCKET_NAME,
                    Delete={'Objects': [{'Key': key} for key in keys_to_delete]}
                )
                print(f"Deleted files: {keys_to_delete}")
            else:
                print("No matching files to delete.")
        else:
            print("No files found.")
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Credentials error: {str(e)}")

@click.group()
def cli():
    pass

cli.add_command(list_all_files)
cli.add_command(upload_file)
cli.add_command(list_files_by_regex)
cli.add_command(delete_files_by_regex)

if __name__ == '__main__':
    cli()
