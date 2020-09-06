import random
import psutil
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
import discord
from discord.ext import commands


class Play(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["mr"])
    @commands.is_owner()
    async def memberandom(self, ctx):
        checklist = []
        guild = self.bot.get_guild(711374787892740148)
        bots = guild.get_role(711377288272412723)
        member = guild.members
        for check in member:
            if bots in check.roles:
                continue
            checklist.append(check.discriminator)
        content = random.choice(checklist)
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
        else:
            await ctx.message.delete()
            await ctx.send(str(member))

    @commands.command()
    async def slot(self, ctx, chance: int = 343):
        slotlist = [":alien:", ":robot:", ":smiley_cat:", ":desktop:",
                    ":full_moon_with_face:", ":crossed_swords:", ":seven:"]
        if chance > 10000 or chance == 0:
            raise commands.BadArgument()
        tousenlist = list(range(chance))
        k = random.choice(tousenlist)
        if k == 0:
            content = [random.choice(slotlist)] * 3
            if content[0] == ":seven:":
                kekka = "大あたり！"
            else:
                kekka = "あたり！"
        else:
            while True:
                content = random.choices(slotlist, k=3)
                if not len(set(content)) == 1:
                    kekka = "はずれ！"
                    break
        tousen = str(round(1 / chance * 100, 3)) + "%"
        ooatari = str(round(float(tousen[:-1]) / 7, 3)) + "%"
        if tousen == "0.0%":
            tousen = "限りなく低い"
        if ooatari == "0.0%":
            ooatari = "限りなく低い"
        embed = discord.Embed(
            title="スロット結果",
            description=(
                "|".join(content)
                + f"\n{kekka}\n当選確率 = {tousen}\n大当たり率 = {ooatari}"),
            color=0x3aee67)
        embed.set_footer(text=f"実行者：{ctx.author}")
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
        memory_meter = ("#" * int(memory / 5)).ljust(20)
        cpu_meter = ("#" * int(cpu / 5)).ljust(20)
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
