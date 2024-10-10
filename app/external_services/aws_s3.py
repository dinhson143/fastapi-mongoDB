import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


BUCKET_NAME = "book-store-logs"
s3_client = None


def get_s3_client():
    global s3_client
    if s3_client is None:
        try:
            s3_client = boto3.client('s3')
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Error with AWS credentials: {e}")
    return s3_client


def upload_log_to_s3(log_file: str, s3_key: str):
    s3 = get_s3_client()
    try:
        s3.upload_file(log_file, BUCKET_NAME, s3_key)
        print(f"Successfully uploaded {log_file} to s3://{BUCKET_NAME}/{s3_key}")
    except Exception as e:
        print(f"Failed to upload log to S3 service: {e}")
