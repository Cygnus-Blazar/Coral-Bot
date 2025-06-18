import json, os
from datetime import datetime

LEDGER_PATH = os.path.join("src", "data", "orbit-chain.json")

def load_ledger():
    with open(LEDGER_PATH, "r") as f:
        return json.load(f)

def save_ledger(ledger):
    with open(LEDGER_PATH, "w") as f:
        json.dump(ledger, f, indent=2)

def get_user_transactions(user_id):
    ledger = load_ledger()
    return [
        tx for block in ledger for tx in block.get("transactions", [])
        if tx.get("sender") == user_id or tx.get("receiver") == user_id
    ]

def get_balance(user_id):
    bal = 0
    for tx in get_user_transactions(user_id):
        if tx.get("receiver") == user_id:
            bal += tx.get("amount", 0)
        if tx.get("sender") == user_id:
            bal -= tx.get("amount", 0)
    return bal

def record_transaction(sender, receiver, amount, note="transfer"):
    ledger = load_ledger()
    block = {
        "block_id": len(ledger) + 1,
        "timestamp": datetime.utcnow().isoformat(),
        "transactions": [{
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "note": note
        }]
    }
    ledger.append(block)
    save_ledger(ledger)

def ensure_user(user_id):
    if get_user_transactions(user_id) == []:
        record_transaction("system", user_id, 0, "register")
