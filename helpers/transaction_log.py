# context_provider/helpers/transaction_log.py

import os
import yaml
from typing import List, Dict
from datetime import datetime

TRANSACTION_DIR = "transactions"


def ensure_transaction_dir_exists(base_path: str):
    os.makedirs(os.path.join(base_path, TRANSACTION_DIR), exist_ok=True)


def get_transaction_file_path(base_path: str, topic: str) -> str:
    filename = f"{topic}.pending.yaml"
    return os.path.join(base_path, TRANSACTION_DIR, filename)


def append_transaction(
    base_path: str, topic: str, action: str, fact: str, timestamp: str = None
) -> None:
    """Append a new transaction (insert/edit/delete) for a topic."""
    ensure_transaction_dir_exists(base_path)

    path = get_transaction_file_path(base_path, topic)

    if not timestamp:
        timestamp = datetime.utcnow().isoformat()

    transaction = {
        "type": action,
        "fact": fact.strip(),
        "timestamp": timestamp,
    }

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {"pending_changes": []}
    else:
        data = {"pending_changes": []}

    data["pending_changes"].append(transaction)

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)


def load_transactions(base_path: str, topic: str) -> List[Dict]:
    """Load pending transactions for a topic."""
    path = get_transaction_file_path(base_path, topic)

    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    return data.get("pending_changes", [])


def clear_transactions(base_path: str, topic: str) -> None:
    """Clear the pending transaction file for a topic."""
    path = get_transaction_file_path(base_path, topic)

    if os.path.exists(path):
        os.remove(path)


def count_transactions(base_path: str, topic: str) -> int:
    """Return the number of pending transactions for a topic."""
    transactions = load_transactions(base_path, topic)
    return len(transactions)
