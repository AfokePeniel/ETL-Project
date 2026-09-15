import io
import boto3
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import config

# ==================== ENV VARIABLE SETTINGS ====================
FILE = "transactions_2026-09-15.csv"  # clean file to load
COLUMNS = ["transaction_id", "account_number", "account_type", "transaction_type", "amount", "transaction_date", "processed_at"]  # table columns in order
s3 = boto3.client("s3", region_name=config.AWS_REGION)  # connect to S3

# ==================== READ CLEAN FILE FROM S3 ====================
clean = s3.get_object(Bucket=config.BUCKET, Key=f"processed/{FILE}")["Body"].read()  # download the clean file
df = pd.read_csv(io.BytesIO(clean), dtype=str)  # read every value as text to keep amounts exact
print("Rows read:", len(df))  # expect 47

# ==================== UPSERT SQL ====================
SQL = """
INSERT INTO transactions (transaction_id, account_number, account_type, transaction_type, amount, transaction_date, processed_at)
VALUES %s
ON CONFLICT (transaction_id) DO UPDATE SET
    account_number   = EXCLUDED.account_number,
    account_type     = EXCLUDED.account_type,
    transaction_type = EXCLUDED.transaction_type,
    amount           = EXCLUDED.amount,
    transaction_date = EXCLUDED.transaction_date,
    processed_at     = EXCLUDED.processed_at;
"""

# ==================== LOAD INTO RDS ====================
conn = psycopg2.connect(host=config.DB_HOST, dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD)  # connect to RDS
with conn, conn.cursor() as cur:  # commit if everything succeeds, undo if anything fails
    execute_values(cur, SQL, df[COLUMNS].itertuples(index=False, name=None))  # send all rows in one batch
    cur.execute("SELECT COUNT(*) FROM transactions")  # count rows now in the table
    print("Rows in table:", cur.fetchone()[0])  # expect 47
conn.close()  # close connection
