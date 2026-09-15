from pathlib import Path
import boto3
import config

LOCAL_FILE = Path("data/transactions_2026-09-15.csv")  # raw file to upload
S3_KEY = f"raw/{LOCAL_FILE.name}"  # destination path in the bucket

s3 = boto3.client("s3", region_name=config.AWS_REGION)  # connect to S3
s3.upload_file(str(LOCAL_FILE), config.BUCKET, S3_KEY)  # upload the file untouched
print(f"Uploaded {LOCAL_FILE} to s3://{config.BUCKET}/{S3_KEY}")  # confirm upload
