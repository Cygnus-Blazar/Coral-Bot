from discord.ext import commands
import random
import ledger, cooldownutil, config

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def balance(self, ctx):
        user_id = str(ctx.author.id)
        ledger.ensure_user(user_id)
        bal = ledger.get_balance(user_id)
        await ctx.send(f"💰 {ctx.author.display_name}, you have {bal} Orbit.")

    @commands.command()
    async def work(self, ctx):
        user_id = str(ctx.author.id)
        on_cd, wait = cooldownutil.is_on_cooldown(user_id, "work", config.COOLDOWNS["work"])
        if on_cd:
            await ctx.send(f"⏳ Wait {wait}s before working again.")
            return
        earned = random.randint(10, 25)
        ledger.ensure_user(user_id)
        ledger.record_transaction("system", user_id, earned, "work_reward")
        cooldownutil.set_cooldown(user_id, "work")
        await ctx.send(f"🛠️ {ctx.author.display_name}, you worked and earned {earned} Orbit!")

    @commands.command()
    async def deposit(self, ctx, amount: int):
        user_id = str(ctx.author.id)
        balance = ledger.get_balance(user_id)
        if amount <= 0 or amount > balance:
            await ctx.send("❌ Invalid deposit amount.")
            return
        ledger.record_transaction(user_id, f"{user_id}_bank", amount, "deposit")
        await ctx.send(f"🏦 Deposited {amount} Orbit into your bank.")

    @commands.command()
    async def withdraw(self, ctx, amount: int):
        user_id = str(ctx.author.id)
        bank_id = f"{user_id}_bank"
        balance = ledger.get_balance(bank_id)
        if amount <= 0 or amount > balance:
            await ctx.send("❌ Invalid withdrawal amount.")
            return
        ledger.record_transaction(bank_id, user_id, amount, "withdraw")
        await ctx.send(f"💸 Withdrew {amount} Orbit from your bank.")

    @commands.command()
    async def pay(self, ctx, member: discord.Member, amount: int):
        sender = str(ctx.author.id)
        receiver = str(member.id)
        if sender == receiver:
            await ctx.send("❌ You can't pay yourself.")
            return
        balance = ledger.get_balance(sender)
        if amount <= 0 or amount > balance:
            await ctx.send("❌ Invalid payment amount.")
            return
        ledger.record_transaction(sender, receiver, amount, "user_payment")
        await ctx.send(f"✅ Sent {amount} Orbit to {member.display_name}.")

async def setup(bot):
    await bot.add_cog(Economy(bot))
