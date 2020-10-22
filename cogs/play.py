import random
import psutil
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
import discord
from discord.ext import commands
import asyncpg


class Play(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong!\nlatency={round(self.bot.latency,2)*1000}ms")

    @commands.command(aliases=["mr"])
    @commands.is_owner()
    async def member_random(self, ctx):
        members = [
            member.discriminator for member in ctx.guild.members if not member.bot]
        content = random.choice(members)
        embed = discord.Embed(
            title=("抽選結果"),
            description=f"今回選ばれたのは||{content}||番のユーザーです！",
            color=0x3aee67)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command(aliases=["dis"])
    @commands.is_owner()
    async def discriminator(self, ctx, dis: str):
        guild = self.bot.get_guild(711374787892740148)
        member = discord.utils.get(guild.members, discriminator=dis)
        if member is None:
            raise commands.BadArgument()
        await ctx.message.delete()
        await ctx.send(str(member))

    @commands.command()
    async def slot(self, ctx, chance: int = 343):
        slotlist = [":alien:", ":robot:", ":smiley_cat:", ":desktop:",
                    ":full_moon_with_face:", ":crossed_swords:", ":seven:"]
        if chance > 10000 or chance <= 0:
            raise commands.BadArgument()
        choice_number = random.randint(0, chance)
        if choice_number == 0:
            content = [random.choice(slotlist)] * 3
            if content[0] == ":seven:":
                result = "大あたり！"
            else:
                result = "あたり！"
        else:
            result = "はずれ！"
            while len(set(content)) != 1:
                content = random.choices(slotlist, k=3)
        embed = discord.Embed(
            title="スロット結果",
            description=(
                f"{'|'.join(content)}\n"
                f"{result}\n当選確率 = {1/chance:.4%}\n"
                f"大当たり率 = {1/chance/7: .4 %}"),
            color=0x3aee67)
        await ctx.send(embed=embed)

    @commands.command(aliases=["touhyou"])
    async def poll(self, ctx, title, *choices):
        if len(choices) >= 21:
            raise commands.TooManyArguments()
        emoji = 0x0001f1e6  # 絵文字定数（A）
        num = 0
        emojis = []
        content = ""
        if len(choices) == 0:
            choices = ["そう思う", "そう思わない"]
        for num, choice in enumerate(choices):
            reaction = chr(emoji + num)
            content += f"{reaction}：{choice}\n"
            emojis.append(reaction)
        embed = discord.Embed(
            title=title,
            description=content,
            color=0x3aee67)
        msg = await ctx.send(embed=embed)
        await ctx.message.delete()
        [await msg.add_reaction(e) for e in emojis]

    @commands.command()
    async def choice(self, ctx, *choices):
        content = random.choice(choices)
        await ctx.send(content)

    @commands.command()
    async def used(self, ctx):
        total = psutil.virtual_memory().total / 1000000000
        use = psutil.virtual_memory().used / 1000000000
        memory = round(use / total * 100, 0)
        cpu = psutil.cpu_percent(interval=1)
        memory_meter = ("#" * int(memory / 5)).ljust(20, ".")
        cpu_meter = ("#" * int(cpu / 5)).ljust(20, ".")
        embed = discord.Embed(
            title="使用状況",
            description=(
                f"Memory...{round(use, 1)}GB/{round(total, 1)}GB {memory}%\n"
                f"`|{memory_meter}|`\n\n"
                f"CPU...{cpu}%\n"
                f"`|{cpu_meter}|`"),
            color=0)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Play(bot))
