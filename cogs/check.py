from janome.tokenizer import Tokenizer
from discord.ext import commands
import discord
import json
import csv
import pandas as pd
import aiofiles
t = Tokenizer("dictionary.csv", udic_type="simpledic", udic_enc="utf8")


class Check(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(711374787892740148)
        self.dev = self.guild.get_member(602668987112751125)

    @commands.Cog.listener()
    async def on_message(self, message):
        async with aiofiles.open('allbot.json', 'r') as bougen:
            data = await bougen.read()
        loadbougen = json.loads(data)
        bougenlist = loadbougen['henkoulist']
        member = message.author
        if member.bot:
            return
        elif message.content.startswith("ab!"):
            return
        not_list = ["削り", "消し"]
        moji = message.content
        kekka = t.tokenize(moji, wakati=True)
        for word in kekka:
            if word in bougenlist:
                kensyutu = kekka.index(word)
                if kekka[kensyutu-1] in not_list:
                    embed = discord.Embed(
                        title="Exception handling",
                        description=f"暴言を検出しましたが、例外処理に含まれていたためreturnしました。",
                        color=0x4db56a)
                    embed.add_field(
                        name="Details", value=f"送信者: {str(message.author)}\n内容: {message.content}")
                    await message.guild.get_channel(715154878166466671).send(embed=embed)
                    return
                seigen = message.guild.get_role(714733639505543222)
                normal = message.guild.get_role(711375295172706313)
                tyuui = message.guild.get_role(715809531829157938)
                keikoku = message.guild.get_role(715809422148108298)
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

    @commands.command()
    @commands.has_role(713321552271376444)
    async def bougenadd(self, ctx, naiyou):
        if not self.dev == ctx.author:
            embed = discord.Embed(
                title="Error",
                description=(
                    f"このコマンドは開発者のみ実行できます。\nCan only be executed by the creator."),
                color=0xff0000)
            await ctx.channel.send(embed=embed, delete_after=10)
            await ctx.message.delete()
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
        await ctx.message.delete()
        return

    @commands.command()
    @commands.has_role(713321552271376444)
    async def bougenremove(self, ctx, naiyou):
        if not self.dev == ctx.author:
            embed = discord.Embed(
                title="Error",
                description=(
                    f"このコマンドは開発者のみ実行できます。\nCan only be executed by the creator."),
                color=0xff0000)
            await ctx.channel.send(embed=embed, delete_after=10)
            await ctx.message.delete()
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
        await ctx.message.delete()
        return

    @commands.command()
    async def kaiseki(self, ctx, naiyou):
        moji = naiyou
        kekka = t.tokenize(moji, wakati=True)
        await ctx.channel.send(kekka)

    @commands.command()
    async def dictadd(self, ctx, naiyou, yomi, hinsi):
        with open('dictionary.csv', 'a', encoding='utf8') as f:
            csv_writer = csv.writer(f, lineterminator='\n')
            csv_writer.writerow([naiyou, hinsi, yomi])
        print("Done")

    @commands.command()
    async def dictprint(self, ctx):
        num = 0
        jisyo = []
        with open("dictionary.csv", 'r', encoding="utf8") as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                jisyo.append(str(num), row)
                num += 1
                print(row)
            embed = discord.Embed(
                title="現在のユーザー辞書",
                description=f"{jisyo}")
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def bougenprint(self, ctx):
        async with aiofiles.open('allbot.json', 'r') as bougen:
            data = await bougen.read()
        loadbougen = json.loads(data)
        bougenlist = loadbougen['henkoulist']
        await ctx.channel.send(bougenlist)

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


def setup(bot):
    bot.add_cog(Check(bot))
