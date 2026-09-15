import pandas as pd

FILE = "data/transactions_2026-09-15.csv"  # raw file to inspect

df = pd.read_csv(FILE)  # read the file into a table

print("Rows:", len(df))  # total rows, excluding header
print("\nDuplicate transaction IDs:")
print(df[df["transaction_id"].duplicated()]["transaction_id"].to_string(index=False))  # IDs that repeat
print("\nRows with missing amounts:")
print(df[df["amount"].isna()].to_string(index=False))  # blank amounts
print("\nAccount type spellings:")
print(df["account_type"].value_counts().to_string())  # count each spelling
print("\nDate formats:")
print(df["transaction_date"].value_counts().to_string())  # count each date value
