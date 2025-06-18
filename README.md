# Coral-Bot

A modular, blockchain-integrated Discord economy bot powered by the Orbit Blockchain ledger.

---

## 🚀 Features

- 💰 **Economy System**
  - `!balance` — Check your on-chain Orbit balance
  - `!work` — Earn random Orbit with a cooldown
  - `!deposit` / `!withdraw` — Move funds in/out of your bank (separate balance)
  - `!pay @user amount` — Send Orbit to others

- 🕒 **Cooldowns**
  - Per-user, per-command cooldowns
  - Cooldowns persist across restarts (`cooldowns.json`)

- 🧠 **Blockchain Integration**
  - Uses `orbit-chain.json` as the transaction ledger
  - Fully stateless balance calculation by ledger scanning
  - Transactions include metadata (notes, timestamps)

- 📆 **Scheduled Tasks**
  - Daily interest payouts on bank balances (2% default)

- 🧩 **Modular Design**
  - Drop-in cog system via `src/cogs/`
  - Expandable with staking, leaderboards, VIP roles, etc.


