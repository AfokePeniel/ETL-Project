import boto3
import psycopg2
import config

s3 = boto3.client("s3", region_name=config.AWS_REGION)  # connect to S3
print("S3 OK:", s3.list_objects_v2(Bucket=config.BUCKET)["KeyCount"], "objects")  # list bucket contents

conn = psycopg2.connect(host=config.DB_HOST, dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD)  # connect to RDS
print("RDS OK:", conn.server_version)  # show PostgreSQL version
conn.close()  # close connection
