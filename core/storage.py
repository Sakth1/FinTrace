# core/storage.py

from tinydb import TinyDB, Query
from pathlib import Path

DB_PATH = Path("data/db.json")
db = TinyDB(DB_PATH)

def save_transactions(transactions):
    tx_store = db.table("transactions")
    for tx in transactions:
        if not tx_store.contains(Query().upi_ref == tx["upi_ref"]):
            tx_store.insert(tx)

def get_all_transactions():
    return db.table("transactions").all()
