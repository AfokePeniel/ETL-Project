import io
from datetime import datetime, timezone
import boto3
import pandas as pd
import config

# ==================== ENV VARIABLE SETTINGS ====================
FILE = "transactions_2026-09-15.csv"  # file to transform
FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%b %d %Y"]  # date formats found during inspection
s3 = boto3.client("s3", region_name=config.AWS_REGION)  # connect to S3

# ==================== READ RAW FILE FROM S3 ====================
raw = s3.get_object(Bucket=config.BUCKET, Key=f"raw/{FILE}")["Body"].read()  # download the raw file
df = pd.read_csv(io.BytesIO(raw))  # read it into a table
print("Rows read:", len(df))  # expect 54

# ==================== STANDARDIZE VALUES ====================
df["account_type"] = df["account_type"].str.strip().str.lower()  # fix mixed case
dates = pd.Series(pd.NaT, index=df.index)  # empty date column to fill
for fmt in FORMATS:
    dates = dates.fillna(pd.to_datetime(df["transaction_date"], format=fmt, errors="coerce"))  # fill matches for each format
if dates.isna().any():
    raise ValueError(f"Unknown date format: {df.loc[dates.isna(), 'transaction_date'].tolist()}")  # stop on anything unexpected
df["transaction_date"] = dates.dt.date  # keep the date only

# ==================== REMOVE BAD ROWS ====================
rows = len(df)  # count before cleanup
df = df.drop_duplicates(subset="transaction_id")  # keep the first copy of each ID
dupes = rows - len(df)  # duplicates removed
df = df.dropna(subset=["amount"])  # remove rows with no amount
print(f"Removed {dupes} duplicates and {rows - dupes - len(df)} missing amounts, {len(df)} rows left")  # expect 4, 3, 47

# ==================== ADD AUDIT COLUMN AND SAVE TO S3 ====================
df["processed_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")  # when the data was cleaned (UTC)
s3.put_object(Bucket=config.BUCKET, Key=f"processed/{FILE}", Body=df.to_csv(index=False, float_format="%.2f"))  # upload clean file
print(f"Saved to s3://{config.BUCKET}/processed/{FILE}")  # confirm destination
