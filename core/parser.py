# core/parser.py

import pandas as pd
from uuid import uuid4
from datetime import datetime
import os

EXPECTED_COLUMNS = [
    "Date", "Time", "Transaction Details", "Your Account",
    "Amount", "UPI Ref No.", "Order ID", "Remarks", "Tags", "Comment"
]

def parse_transaction_file(file_path):
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".csv":
            df = pd.read_csv(file_path)
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(file_path, sheet_name="Passbook Payment History", engine="openpyxl")
        else:
            raise ValueError("Unsupported file type.")

        if not all(col in df.columns for col in EXPECTED_COLUMNS):
            raise ValueError("Invalid file format. Missing expected columns.")

        transactions = []
        for _, row in df.iterrows():
            try:
                combined_datetime = datetime.strptime(
                    f"{row['Date']} {row['Time']}",
                    "%d/%m/%Y %H:%M:%S"
                )

                transactions.append({
                    "id": str(uuid4()),
                    "datetime": combined_datetime.isoformat(),
                    "account": str(row["Your Account"]),
                    "amount": float(str(row["Amount"]).replace(",", "").strip()),
                    "description": str(row["Transaction Details"]),
                    "upi_ref": str(row["UPI Ref No."]),
                    "order_id": str(row.get("Order ID", "")),
                    "remarks": str(row.get("Remarks", "")),
                    "category": str(row.get("Tags", "Uncategorized")),
                    "comment": str(row.get("Comment", ""))
                })
            except Exception as e:
                print(f"[WARN] Skipping row: {e}")

        return transactions

    except Exception as e:
        print(f"[ERROR] Could not parse file: {e}")
        return []
