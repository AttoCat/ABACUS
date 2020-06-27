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
            title=(f"抽選結果"),
            description=f"今回選ばれたのは||{content}||番のユーザーです！",
            color=0x3aee67)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command(aliases=["gd"])
    @commands.is_owner()
    async def userdiscriminator(self, ctx, dis: str):
        guild = self.bot.get_guild(711374787892740148)
        member = discord.utils.get(guild.members, discriminator=dis)
        if member == None:
            raise commands.BadArgument()
        else:
            await ctx.message.delete()
            await ctx.send(str(member))

    @commands.command()
    async def slot(self, ctx, kakuritu: int = 0):
        slotlist = [":alien:", ":robot:", ":smiley_cat:", ":desktop:",
                    ":full_moon_with_face:", ":crossed_swords:", ":seven:"]
        number = []
        if kakuritu == 0:
            content1 = random.choice(slotlist)
            content2 = random.choice(slotlist)
            content3 = random.choice(slotlist)
            tousen = "0.29%"
            ooatari = "0.041%"
        elif kakuritu > 10000:
            embed = discord.Embed(
                title="Error",
                description=(
                    f"引数が大きすぎます！最大数は10000です！\nArgument is too large."),
                color=0xff0000)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed, delete_after=10)
            return
        else:
            for num in range(kakuritu):
                number.append(num)
            k = random.choice(number)
            if k == 0:
                content1 = random.choice(slotlist)
                content2 = content1
                content3 = content2
            else:
                content1 = random.choice(slotlist)
                content2 = random.choice(slotlist)
                content3 = random.choice(slotlist)
            tousen = str(round(1/kakuritu*100, 1))
            ooatari = str(round(float(tousen)/7, 1))
            if float(tousen) == 0.0:
                tousen = "限りなく低い"
                ooatari = "限りなく低い"
            else:
                tousen = tousen + "%"
                ooatari = ooatari + "%"
        if content1 == content2 == content3:
            kekka = "あたり！"
            if content1 == ":seven:":
                kekka = "大当たり！"
        else:
            kekka = "はずれ！"
        embed = discord.Embed(
            title="スロット結果",
            description=(
                f"{content1}|{content2}|{content3}\n{kekka}\n当選確率 = {tousen}\n大当たり率 = {ooatari}"),
            color=0x3aee67)
        embed.set_footer(text=f"実行者：{ctx.author}")
        await ctx.send(embed=embed)

    @commands.command()
    async def touhyou(self, ctx, title, *args):
        if len(args) >= 21:
            raise commands.TooManyArguments()
        emoji = 0x0001f1e6  # 絵文字定数（A）
        num = 0
        naiyou = []
        if len(args) == 0:
            naiyou.append(chr(emoji) + "：そう思う")
            naiyou.append(chr(emoji + 1) + "：そう思わない")
        else:
            for content in args:
                tuika = chr(emoji + num) + "：" + str(content)
                num += 1
                naiyou.append(tuika)
        msg = "\n".join(naiyou)
        embed = discord.Embed(
            title="投票",
            description=(
                f"タイトル：{title}\n{msg}"),
            color=0x3aee67)
        msg = await ctx.send(embed=embed)
        await ctx.message.delete()
        for num in range(len(naiyou)):
            tuika = chr((emoji + num))
            await msg.add_reaction(tuika)

    @commands.command()
    async def abacus(self, ctx):
        total = psutil.virtual_memory().total/1000/1000/1000
        use = psutil.virtual_memory().used/1000/1000/1000
        kekka = round(use/total*100, 0)
        content = int(kekka/5)
        cpu = psutil.cpu_percent(interval=1)
        content2 = int(cpu/5)
        memorymeter = ("|" * content) + (" " * (20-content))
        cpumeter = ("|" * content2) + (" " * (20-content2))
        embed = discord.Embed(
            title="使用状況",
            description=(
                f"Memory...{round(use, 1)}GB/{round(total, 1)}GB {kekka}%\n"
                f"`[{memorymeter}]`\n"
                f"CPU...{cpu}%\n"
                f"`[{cpumeter}]`"),
            color=0xff0000)
        await ctx.send(embed=embed)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title="Error",
                description=(
                    f"あなたにこのコマンドを実行する権限がありません！\nYou don't have permission."),
                color=0xff0000)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed, delete_after=10)
            return
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="Error",
                description=(
                    f"不正な引数です！\nInvalid argument passed."),
                color=0xff0000)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed, delete_after=10)
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Error",
                description=f"想定しない引数が渡されました！\nInvalid input.",
                color=0xff0000)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed, delete_after=10)
            return
        elif isinstance(error, commands.TooManyArguments):
            embed = discord.Embed(
                title="Error",
                description=f"引数の数が不正です！\nInvalid input.",
                color=0xff0000)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed, delete_after=10)
            return
        else:
            embed = discord.Embed(
                title="Error",
                description=(
                    f"不明なエラーが発生しました。\nエラー内容:\n{error}"),
                color=0xff0000)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed)
            return


def setup(bot):
    bot.add_cog(Play(bot))
