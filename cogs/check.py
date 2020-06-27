import numpy as np
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

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(711374787892740148)
        self.dev = self.guild.get_member(602668987112751125)
        self.nsfw = self.guild.get_channel(713050662774112306)
        self.system = self.bot.get_guild(682218950268157982)
        self.log1 = self.system.get_channel(726329141540159568)
        self.log2 = self.system.get_channel(726329157948145696)
        await self.load_json()
        await self.load_csv()

    @commands.Cog.listener()
    async def on_message(self, message):
        member = message.author
        if member.bot:
            return
        elif message.content.startswith("ab!"):
            return
        moji = message.content
        kekka = self.t.tokenize(moji, wakati=True)
        for word in kekka:
            if word in self.scan:
                if message.channel == self.nsfw:
                    return
                kensyutu = kekka.index(word)
                normal = message.guild.get_role(
                    711375295172706313)  # ノーマルメンバー役職
                tyuui = message.guild.get_role(715809531829157938)  # 「注意」役職
                keikoku = message.guild.get_role(715809422148108298)  # 「警告」役職
                seigen = message.guild.get_role(714733639505543222)  # 「制限」役職
                await message.delete()
                embed = discord.Embed(
                    title="Message deleted",
                    description=f"NGワードが含まれていたため、削除しました。",
                    color=0xff0000)
                kensyutu = discord.Embed(
                    title="NGワードを検出",
                    description=f"送信者: {str(message.author)}\n内容:{message.content}",
                    color=0xff0000)
                await message.guild.get_channel(715142539535056907).send(embed=kensyutu)
                if tyuui in member.roles:  # 注意がある場合は警告に変更
                    await member.add_roles(keikoku)
                    await member.remove_roles(tyuui)
                elif keikoku in member.roles:  # 警告がある場合は制限付きに
                    await member.remove_roles(normal)
                    await member.add_roles(seigen)
                    await member.remove_roles(keikoku)
                else:  # 何も持っていなければ注意を
                    await member.add_roles(tyuui)
                await message.channel.send(
                    embed=embed)
                return

    async def write_json(self):
        strage = self.log1
        kekka = {'henkoulist': self.scan}
        async with aiofiles.open('allbot.json', 'w') as ng:  # 追加後のリストに内容を置き換え
            await ng.write(json.dumps(kekka, indent=4))
        file = discord.File("allbot.json")
        await strage.send(file=file)

    async def load_json(self):
        strage = self.log1
        id = strage.last_message_id
        msg = await strage.fetch_message(id)
        await msg.attachments[0].save("allbot.json")
        async with aiofiles.open('allbot.json', 'r') as ng:  # jsonファイルから暴言リストを読み込み
            data = await ng.read()
        scanlist = json.loads(data)
        self.scan = scanlist['henkoulist']

    async def load_csv(self):
        strage = self.log2
        id = strage.last_message_id
        msg = await strage.fetch_message(id)
        await msg.attachments[0].save("dictionary.csv")
        self.df = pd.read_csv("dictionary.csv", header=None)

    async def write_csv(self):
        strage = self.log2
        self.df.to_csv('dictionary.csv', header=False, index=False)
        file = discord.File("dictionary.csv")
        await strage.send(file=file)

    async def reload_csv(self):
        self.t = Tokenizer(
            "dictionary.csv", udic_type="simpledic", udic_enc="utf8")

    @commands.group()
    @commands.has_role(713321552271376444)
    async def ng(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('このコマンドにはサブコマンドが必要です。')
            return

    @ng.command(name='add')
    async def _add(self, ctx, content):
        self.scan.append(content)
        embed = discord.Embed(
            title="Done.",
            description=(
                f"暴言リストに要素を追加しました。\nAdd complete."),
            color=0x4169e1)
        await ctx.send(embed=embed)
        await self.write_json()
        await ctx.message.delete()

    @ng.command(name='remove')
    async def _remove(self, ctx, content: str):
        try:
            self.scan.remove(content)
        except ValueError:
            raise commands.BadArgument
        embed = discord.Embed(
            title="Done.",
            description=(
                f"暴言リストから要素を削除しました。\nRemove complete."),
            color=0x4169e1)
        await ctx.send(embed=embed)
        await self.write_json()
        await ctx.message.delete()

    @ng.command(name='print')
    async def _print(self, ctx):
        kekka = []
        num = 1
        for word in self.scan:
            kekka.append(f"{str(num)}：{word}")
            num += 1
        msg = "\n".join(kekka)
        embed = discord.Embed(
            title="現在のNGワードリスト",
            description=f"{msg}"
        )
        await ctx.send(embed=embed, delete_after=60)
        await ctx.message.delete()

    @commands.command(aliases=['ks'])
    @commands.has_role(713321552271376444)
    async def kaiseki(self, ctx, naiyou):
        t = Tokenizer(
            "dictionary.csv", udic_type="simpledic",
            udic_enc="utf8")
        moji = naiyou
        kekka = t.tokenize(moji, wakati=True)
        await ctx.channel.send(kekka)

    @commands.group()
    @commands.is_owner()
    async def dict(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('このコマンドにはサブコマンドが必要です。')
            return

    @dict.command(name="add")
    async def _add(self, ctx, *args):
        content = list(args)
        if len(content) == 2:
            content.append("名詞")
        elif len(content) >= 4:
            raise commands.BadArgument
        self.df = self.df.append(
            {
                0: content[0],
                1: content[2],
                2: content[1]
            }, ignore_index=True)
        self.df = self.df.reset_index(drop=True)
        await self.write_csv()
        embed = discord.Embed(
            title="Done.",
            description=(
                f"ユーザー辞書に要素を追加しました。\n現在のユーザー辞書は ab!dictprint で確認できます。\nAdd complete."),
            color=0x4169e1)
        await ctx.message.delete()
        await self.reload_csv()
        await ctx.channel.send(embed=embed, delete_after=10)

    @dict.command(name='remove')
    async def _remove(self, ctx, kazu: int):
        self.df = self.df.drop(index=self.df.index[kazu])
        self.df = self.df.reset_index(drop=True)
        await self.write_csv()
        embed = discord.Embed(
            title="Done.",
            description=(
                f"ユーザー辞書から要素を削除しました。\n現在のユーザー辞書は ab!dict print で確認できます。\nDelete complete."),
            color=0x4169e1)
        await ctx.channel.send(embed=embed, delete_after=10)
        await self.reload_csv()
        await ctx.message.delete()

    @dict.command(name="print")
    async def _print(self, ctx):
        df = self.df.rename(
            columns={0: "名前", 1: "品詞", 2: "ふりがな"}
        )
        embed = discord.Embed(
            title="現在のユーザー辞書",
            description=f"{df}")
        await ctx.channel.send(embed=embed, delete_after=20)
        await self.reload_csv()
        await ctx.message.delete()

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
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="Error",
                description=(
                    f"不正な引数です！\nInvalid argument passed."),
                color=0xff0000)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed, delete_after=10)
            return
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title="Error",
                description=(
                    f"このコマンドは開発者のみ実行できます。\nCan only be executed by the creator."),
                color=0xff0000)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed, delete_after=10)
            return
        elif isinstance(error, commands.TooManyArguments):
            embed = discord.Embed(
                title="Error",
                description=(
                    f"引数の数が不正です！\nCan only be executed by the creator."),
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
            await ctx.channel.send(embed=embed)
            return


def setup(bot):
    bot.add_cog(Check(bot))
