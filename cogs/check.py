from janome.tokenizer import Tokenizer
from discord.ext import commands
import discord
import json
import csv
import pandas as pd
import aiofiles


class Check(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def gentei(self, ch, ctx):
        embed = discord.Embed(
            title="Error",
            description=(
                f"このコマンドは開発者のみ実行できます。\nCan only be executed by the creator."),
            color=0xff0000)
        await ch.send(embed=embed, delete_after=10)
        await ctx.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(711374787892740148)
        self.dev = self.guild.get_member(602668987112751125)

    @commands.Cog.listener()
    async def on_message(self, message):
        t = Tokenizer("dictionary.csv", udic_type="simpledic", udic_enc="utf8")
        async with aiofiles.open('allbot.json', 'r') as bougen:
            data = await bougen.read()
        loadbougen = json.loads(data)
        bougenlist = loadbougen['henkoulist']
        member = message.author
        if member.bot:
            return
        elif message.content.startswith("ab!"):
            return
        moji = message.content
        kekka = t.tokenize(moji, wakati=True)
        for word in kekka:
            if word in bougenlist:
                kensyutu = kekka.index(word)
                normal = message.guild.get_role(
                    711375295172706313)  # ノーマルメンバー役職
                tyuui = message.guild.get_role(715809531829157938)  # 「注意」役職
                keikoku = message.guild.get_role(715809422148108298)  # 「警告」役職
                seigen = message.guild.get_role(714733639505543222)  # 「制限」役職
                await message.delete()
                embed = discord.Embed(
                    title="Message deleted",
                    description=f"暴言が含まれていたため、削除しました。",
                    color=0xff0000)
                kensyutu = discord.Embed(
                    title="Manegement_001",
                    description=f"送信者: {str(message.author)}\n内容:{message.content}",
                    color=0xff0000)
                await message.guild.get_channel(715154878166466671).send(embed=kensyutu)
                if tyuui in member.roles:
                    await member.add_roles(keikoku)
                    await member.remove_roles(tyuui)
                elif keikoku in member.roles:
                    await member.remove_roles(normal)
                    await member.add_roles(seigen)
                    await member.remove_roles(keikoku)
                else:
                    await member.add_roles(tyuui)
                await message.channel.send(
                    embed=embed)
                return

    @commands.command(aliases=['ba'])
    @commands.has_role(713321552271376444)
    async def bougenadd(self, ctx, naiyou):
        if not self.dev == ctx.author:
            await self.gentei(ctx.channel, ctx.message)
            return
        async with aiofiles.open('allbot.json', 'r') as bougen:
            data = await bougen.read()
        loadbougen = json.loads(data)
        bougenlist = loadbougen['henkoulist']
        bougenlist.append(naiyou)
        kekka = {'henkoulist': bougenlist}
        async with aiofiles.open('allbot.json', 'w') as bougen:
            await bougen.write(json.dumps(kekka, indent=4))
        embed = discord.Embed(
            title="Done.",
            description=(
                f"暴言リストに要素を追加しました。\nAdd complete."),
            color=0x4169e1)
        await ctx.channel.send(embed=embed, delete_after=10)
        return await ctx.message.delete()

    @commands.command(aliases=['br'])
    @commands.has_role(713321552271376444)
    async def bougenremove(self, ctx, naiyou):
        if not self.dev == ctx.author:
            await self.gentei(ctx.channel, ctx.message)
            return
        async with aiofiles.open('allbot.json', 'r') as bougen:
            data = await bougen.read()
        loadbougen = json.loads(data)
        bougenlist = loadbougen['henkoulist']
        try:
            bougenlist.remove(naiyou)
        except ValueError:
            embed = discord.Embed(
                title="Error",
                description=(
                    f"不正な引数です！\nInvalid argument passed."),
                color=0xff0000)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed, delete_after=10)
            return
        kekka = {'henkoulist': bougenlist}
        async with aiofiles.open('allbot.json', 'w') as bougen:
            await bougen.write(json.dumps(kekka, indent=4))
        embed = discord.Embed(
            title="Done.",
            description=(
                f"暴言リストから要素を削除しました。\nDelete complete."),
            color=0x4169e1)
        await ctx.channel.send(embed=embed, delete_after=10)
        return await ctx.message.delete()

    @commands.command(aliases=['ks'])
    async def kaiseki(self, ctx, naiyou):
        t = Tokenizer("dictionary.csv", udic_type="simpledic", udic_enc="utf8")
        moji = naiyou
        kekka = t.tokenize(moji, wakati=True)
        await ctx.channel.send(kekka)

    @commands.command(aliases=['da'])
    @commands.has_role(713321552271376444)
    async def dictadd(self, ctx, naiyou, yomi, hinsi):
        if not self.dev == ctx.author:
            await self.gentei(ctx.channel, ctx.message)
            return
        with open('dictionary.csv', 'a', encoding='utf8') as f:
            csv_writer = csv.writer(f, lineterminator='\n')
            csv_writer.writerow([naiyou, hinsi, yomi])
        embed = discord.Embed(
            title="Done.",
            description=(
                f"ユーザー辞書に要素を追加しました。\n現在のユーザー辞書は ab!dictprint で確認できます。\nAdd complete."),
            color=0x4169e1)
        await ctx.channel.send(embed=embed, delete_after=10)
        return await ctx.message.delete()

    @commands.command(aliases=['dr'])
    @commands.has_role(713321552271376444)
    async def dictremove(self, ctx, kazu: int):
        if not self.dev == ctx.author:
            await self.gentei(ctx.channel, ctx.message)
            return
        df = pd.read_csv("dictionary.csv", header=None)
        df = df.drop(index=df.index[kazu])
        df.to_csv('dictionary.csv', header=False, index=False)
        embed = discord.Embed(
            title="Done.",
            description=(
                f"ユーザー辞書から要素を削除しました。\n現在のユーザー辞書は ab!dictprint で確認できます。\nDelete complete."),
            color=0x4169e1)
        await ctx.channel.send(embed=embed, delete_after=10)
        return await ctx.message.delete()

    @commands.command(aliases=['dp'])
    async def dictprint(self, ctx):
        num = 0
        jisyo = []
        with open("dictionary.csv", 'r', encoding="utf8") as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                naiyou = row[0]
                hinsi = row[1]
                yomi = row[2]
                jisyo.append(
                    f"{num}" + f" {naiyou}" +
                    f" {hinsi}" + f" {yomi}")
                num += 1
        msg = "\n".join(jisyo)
        embed = discord.Embed(
            title="現在のユーザー辞書",
            description=f"行  名前  品詞  読み\n{msg}")
        await ctx.channel.send(embed=embed, delete_after=10)
        return await ctx.message.delete()

    @commands.command(aliases=['bp'])
    async def bougenprint(self, ctx):
        async with aiofiles.open('allbot.json', 'r') as bougen:
            data = await bougen.read()
        loadbougen = json.loads(data)
        bougenlist = loadbougen['henkoulist']
        return await ctx.channel.send(bougenlist)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            embed = discord.Embed(
                title="Error",
                description=(
                    f"あなたにこのコマンドを実行する権限がありません！\nYou don't have permission."),
                color=0xff0000)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed, delete_after=10)
            return
        elif isinstance(error, commands.MissingRequiredArgument):
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
                    f"不明なエラーが発生しました。\nエラー内容:{error}"),
                color=0xff0000)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed, delete_after=10)
            return


def setup(bot):
    bot.add_cog(Check(bot))
