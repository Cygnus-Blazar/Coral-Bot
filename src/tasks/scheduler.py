from discord.ext import tasks
import ledger, config

@tasks.loop(hours=24)
async def pay_interest():
    chain = ledger.load_ledger()
    all_ids = set()
    for block in chain:
        for tx in block["transactions"]:
            all_ids.add(tx.get("receiver"))
            all_ids.add(tx.get("sender"))
    for uid in list(all_ids):
        if uid.endswith("_bank"):
            bal = ledger.get_balance(uid)
            if bal > 0:
                interest = round(bal * config.INTEREST_RATE)
                ledger.record_transaction("system", uid, interest, "daily_interest")
