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

def get_budget_for_month(month_key):
    db_table = db.table("budgets")
    result = db_table.get(Query().month == month_key)
    if isinstance(result, dict):
        return result.get("limit", 0)
    elif isinstance(result, list) and result:
        return result[0].get("limit", 0)
    else:
        return 0

def save_budget_for_month(month, category, limit):
    db_table = db.table("budgets")
    Budget = Query()
    existing = db_table.get((Budget.month == month) & (Budget.category == category))
    if existing:
        # Handle both single document and list of documents
        if isinstance(existing, list):
            doc_ids = [doc.doc_id for doc in existing]
        else:
            doc_ids = [existing.doc_id]
        db_table.update({"limit": limit}, doc_ids=doc_ids)
    else:
        db_table.insert({"month": month, "category": category, "limit": limit})

def get_all_budgets():
    return db.table("budgets").all()

def load_settings():
    return db.table("settings").get(doc_id=1) or {}

def save_settings(config: dict):
    settings_table = db.table("settings")
    Settings = Query()
    settings_table.upsert(config, Settings.doc_id == 1)
