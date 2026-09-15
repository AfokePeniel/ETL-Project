import os

AWS_REGION = os.environ.get("AWS_REGION", "ca-central-1")  # AWS region
BUCKET = os.environ["BUCKET"]  # S3 bucket name
DB_HOST = os.environ["DB_HOST"]  # RDS endpoint
DB_NAME = "bankingdb"  # database name
DB_USER = "etladmin"  # database user
DB_PASSWORD = os.environ["DB_PASSWORD"]  # read from environment, never hardcoded
