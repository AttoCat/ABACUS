import json

import aiofiles
import discord
import pandas as pd
from discord.ext import commands
from janome.tokenizer import Tokenizer


class Scan(commands.Cog):

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
        self.cat_log = self.system.get_channel(741916689993826345)
        await self.load_json()
        await self.load_csv()
        await self.reload_csv()

    async def role_change(self, author):
        normal = author.guild.get_role(
            711375295172706313)  # ノーマルメンバー役職
        tyuui = author.guild.get_role(715809531829157938)  # 「注意」役職
        keikoku = author.guild.get_role(715809422148108298)  # 「警告」役職
        seigen = author.guild.get_role(714733639505543222)  # 「制限」役職
        if tyuui in author.roles:  # 注意がある場合は警告に変更
            await author.add_roles(keikoku)
            await author.remove_roles(tyuui)
        elif keikoku in author.roles:  # 警告がある場合は制限付きに
            await author.remove_roles(normal)
            await author.add_roles(seigen)
            await author.remove_roles(keikoku)
        else:  # 何も持っていなければ注意を
            await author.add_roles(tyuui)

    @commands.Cog.listener()
    async def on_message(self, message):
        member = message.author
        if (member.bot
            or message.content.startswith("ab!")
                or message.channel.is_nsfw()):
            return
        result = self.t.tokenize(message.content, wakati=True)
        if not any((word in self.scan) for word in result):
            return
        embed = discord.Embed(
            title="Message deleted",
            description="NGワードが含まれていたため、削除しました。",
            color=0xff0000)
        await message.channel.send(embed=embed)
        if message.guild != self.guild:
            is_ab = False
        else:
            channel = member.guild.get_channel(715142539535056907)
            is_ab = True
            await self.role_change(member)
        description = (
            "**Type**: NGword\n"
            "**Author**: {0.author}\n"
            "**Author ID**: {0.author.id}\n"
            "**Content**: {0.content}\n"
            "**Place**: {0.guild.name}  >>  {0.channel.name}\n"
            "**Place ID**: {0.guild.id}  >>  {0.channel.id} \n").format(
            message)
        embed = discord.Embed(
            title="Automatic Management",
            description=description,
            color=0xff0000)
        await self.cat_log.send(embed=embed)
        if is_ab:
            await channel.send(embed=embed)
        await message.delete()
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
        # jsonファイルから暴言リストを読み込み
        async with aiofiles.open('allbot.json', 'r') as ng:
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
    @commands.is_owner()
    async def ng(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('このコマンドにはサブコマンドが必要です。')
            return

    @ng.command(name='add')
    async def ng_add(self, ctx, content):
        self.scan.append(content)
        embed = discord.Embed(
            title="Done.",
            description=(
                "暴言リストに要素を追加しました。\nAdd complete."),
            color=0x4169e1)
        await ctx.send(embed=embed)
        await self.write_json()
        await ctx.message.delete()

    @ng.command(name='remove')
    async def ng_remove(self, ctx, content: str):
        try:
            self.scan.remove(content)
        except ValueError:
            raise commands.BadArgument()
        embed = discord.Embed(
            title="Done.",
            description=(
                "暴言リストから要素を削除しました。\nRemove complete."),
            color=0x4169e1)
        await ctx.send(embed=embed)
        await self.write_json()
        await ctx.message.delete()

    @ng.command(name='print')
    async def ng_print(self, ctx):
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
    @commands.is_owner()
    async def analyze(self, ctx, content):
        result = list(self.t.tokenize(content, wakati=True))
        await ctx.channel.send(",".join(result))

    @commands.group()
    @commands.is_owner()
    async def dict(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('このコマンドにはサブコマンドが必要です。')
            return

    @dict.command(name="add")
    async def dict_add(self, ctx, *args):
        content = list(args)
        if len(content) == 2:
            content.append("名詞")
        elif len(content) >= 4:
            raise commands.BadArgument()
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
                "ユーザー辞書に要素を追加しました。\n"
                "n現在のユーザー辞書は ab!dictprint で確認できます。\n"
                "Add complete."),
            color=0x4169e1)
        await ctx.message.delete()
        await self.reload_csv()
        await ctx.channel.send(embed=embed, delete_after=10)

    @dict.command(name='remove')
    async def dict_remove(self, ctx, kazu: int):
        self.df = self.df.drop(index=self.df.index[kazu])
        self.df = self.df.reset_index(drop=True)
        await self.write_csv()
        embed = discord.Embed(
            title="Done.",
            description=(
                "ユーザー辞書から要素を削除しました。\n"
                "現在のユーザー辞書は ab!dict print で確認できます。\n"
                "Delete complete."),
            color=0x4169e1)
        await ctx.channel.send(embed=embed, delete_after=10)
        await self.reload_csv()
        await ctx.message.delete()

    @dict.command(name="print")
    async def dict_print(self, ctx):
        df = self.df.rename(
            columns={0: "名前", 1: "品詞", 2: "ふりがな"}
        )
        embed = discord.Embed(
            title="現在のユーザー辞書",
            description=f"{df}")
        await ctx.channel.send(embed=embed, delete_after=20)
        await self.reload_csv()
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Scan(bot))
