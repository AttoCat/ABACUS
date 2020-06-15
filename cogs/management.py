import asyncio
import typing
import discord
from discord.ext import commands


class Management(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(711374787892740148)
        self.seigen = self.guild.get_role(714733639505543222)
        self.normal = self.guild.get_role(711375295172706313)
        self.unei = self.guild.get_role(713321552271376444)
        self.keikoku = self.guild.get_role(715809422148108298)
        self.tyuui = self.guild.get_role(715809531829157938)
        self.userch = self.guild.get_channel(720493286888046644)
        self.dev = self.guild.get_member(602668987112751125)

    @commands.command()
    @commands.has_role(713321552271376444)
    async def protect(self, ctx, member: discord.Member):
        await member.remove_roles(self.normal)
        await member.add_roles(self.seigen)
        await ctx.message.delete()

    @commands.command()
    @commands.has_role(713321552271376444)
    async def fix(self, ctx, member: discord.Member):
        if self.tyuui in member.roles:
            await member.remove_roles(self.tyuui)
        elif self.keikoku in member.roles:
            await member.remove_roles(self.keikoku)
        else:
            await member.remove_roles(self.seigen)
            await member.add_roles(self.normal)
        await ctx.message.delete()

    @commands.command(aliases=['md'])
    @commands.has_role(713321552271376444)
    async def mesdelete(self, ctx, message: discord.Message):
        await message.delete()
        embed = discord.Embed(
            title="Done.",
            description=(
                f"削除成功。\nDeletion successful."),
            color=0x4169e1)
        await ctx.message.delete()
        await ctx.channel.send(embed=embed, delete_after=3)

    @commands.Cog.listener()  # メンションユーザー操作機能
    async def on_message(self, message):
        if message.author.bot:
            return
        members = message.guild.members
        if message.channel != self.userch:
            return
        getlist = []
        try:
            get = self.guild.get_member(int(message.content))
            getlist.append(get)
        except ValueError:
            getlist = message.mentions
        if len(getlist) >= 2:
            await message.channel.send("複数のメンションは使用できません！")
            await message.delete()
            asyncio.sleep(10)
            await message.channel.purge(limit=None)
            return
        elif len(getlist) == 0:
            await message.delete()
            return
        elif getlist[0] == message.author:
            await message.channel.send("自身に対して変更を加えることは出来ません！")
            await message.delete()
            asyncio.sleep(10)
            await message.channel.purge(limit=None)
            return
        elif self.unei in getlist[0].roles:
            await message.channel.send("運営またはABACUSに対して変更を加えることは出来ません！")
            await message.delete()
            asyncio.sleep(10)
            await message.channel.purge(limit=None)
            return
        for member in members:
            if member in getlist:
                bangou = []
                emoji = [
                    ":regional_indicator_a:",
                    ":regional_indicator_b:",
                    ":regional_indicator_c:",
                    ":regional_indicator_d:",
                    ":regional_indicator_e:",
                    ":regional_indicator_f:"]
                embed = discord.Embed(
                    title="ユーザー操作",
                    description=(
                        f"{member}に対して変更を加えます。"),
                    color=0xff0000)
                embed.add_field(name=f"{emoji[0]}:キック",
                                value="ユーザーをキックします。", inline=False)
                embed.add_field(name=f"{emoji[1]}:BAN",
                                value="ユーザーをBANします。", inline=False)
                embed.add_field(name=f"{emoji[2]}:制限付き",
                                value="ユーザーを制限付きにします。", inline=False)
                embed.add_field(name=f"{emoji[3]}:注意",
                                value="ユーザーに注意役職を付与します。", inline=False)
                embed.add_field(name=f"{emoji[4]}:警告",
                                value="ユーザーに警告役職を付与します。", inline=False)
                embed.add_field(name=f"{emoji[5]}:解除",
                                value="ユーザーの注意等を全て解除します。", inline=False)
                msg = await message.channel.send(embed=embed, delete_after=100)
                for num in range(6):
                    tuika = chr((0x0001f1e6 + num))
                    await msg.add_reaction(tuika)
                    bangou.append(str(tuika))
                await msg.add_reaction("❌")
                bangou.append(str("❌"))

                async def sousa(sousa):
                    if sousa == 0:
                        await self.guild.kick(member)
                        return
                    elif sousa == 1:
                        await self.guild.ban(member)
                        return
                    elif sousa == 2:
                        await member.add_roles(self.seigen)
                        return
                    elif sousa == 3:
                        await member.add_roles(self.tyuui)
                        return
                    elif sousa == 4:
                        await member.add_roles(self.keikoku)
                        return
                    elif sousa == 5:
                        if self.tyuui in member.roles:
                            await member.remove_roles(self.tyuui)
                        elif self.keikoku in member.roles:
                            await member.remove_roles(self.keikoku)
                        else:
                            await member.remove_roles(self.seigen)
                            await member.add_roles(self.normal)

                def check(reaction, user):
                    msg = str(reaction.emoji)
                    return user == message.author and msg in bangou

                while True:
                    content = [
                        "キック", "BAN", "制限付きに",
                        "注意役職を付与", "警告役職を付与", "注意系役職全解除"
                    ]
                    try:
                        reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        embed = discord.Embed(
                            title="Timeout",
                            description=(
                                f"時間切れです。ログは10秒後に自動で削除されます。"),
                            color=0xff0000)
                        await message.channel.send(embed=embed)
                        asyncio.sleep(10)
                        await message.channel.purge(limit=None)
                        break
                    else:
                        if str(reaction.emoji) == chr(0x0001f1e6):
                            number = 0
                        elif str(reaction.emoji) == chr(0x0001f1e7):
                            number = 1
                        elif str(reaction.emoji) == chr(0x0001f1e8):
                            number = 2
                        elif str(reaction.emoji) == chr(0x0001f1e9):
                            number = 3
                        elif str(reaction.emoji) == chr(0x0001f1ea):
                            number = 4
                        elif str(reaction.emoji) == chr(0x0001f1eb):
                            number = 5
                        elif str(reaction.emoji) == "❌":
                            embed = discord.Embed(
                                title="Cancel",
                                description=(
                                    f"操作をキャンセルしました。ログは10秒後に自動で削除されます。"),
                                color=0xff0000)
                            await message.channel.send(embed=embed)
                            asyncio.sleep(10)
                            await message.channel.purge(limit=None)
                            return
                        embed = discord.Embed(
                            title="最終確認",
                            description=(
                                f"{member}に対して{content[number]} を行います。よろしいですか？\n実行する場合はOK、キャンセルする場合はNOと発言してください！"),
                            color=0xff0000)
                        await message.channel.send(embed=embed, delete_after=50)
                        try:
                            ok_no = await self.bot.wait_for(
                                'message', timeout=20.0,
                                check=lambda m: m.author == message.author and m.content.lower() in ["ok", "no"])
                        except asyncio.TimeoutError:
                            await message.channel.send("時間切れです")
                            break
                        if ok_no.content.lower() == "ok":
                            await sousa(sousa=number)
                            embed = discord.Embed(
                                title="Done.",
                                description=(
                                    f"実行が完了しました。ログは10秒後に自動で削除されます。\nExecution complete."),
                                color=0x4169e1)
                            await message.channel.send(embed=embed, delete_after=20)
                            await asyncio.sleep(10)
                            await message.channel.purge(limit=None)
                            return
                        else:
                            embed = discord.Embed(
                                title="Cancel",
                                description=(
                                    f"操作をキャンセルしました。ログは10秒後に自動で削除されます。"),
                                color=0xff0000)
                            await message.channel.send(embed=embed)
                            asyncio.sleep(10)
                            await message.channel.purge(limit=None)
                        break
                    break

    @commands.command()
    @commands.has_role(713321552271376444)
    async def give(self, ctx, user: typing.Union[discord.Member, str], roles: int):
        if isinstance(user, str):
            try:
                member = discord.utils.get(
                    self.guild.members, discriminator=user)
                user = self.guild.get_member(member.id)
                if user == None:
                    raise commands.BadArgument()
            except ValueError:
                raise commands.BadArgument()
        role = self.guild.get_role(roles)
        await user.add_roles(role)
        embed = discord.Embed(
            title="Done.",
            description=(
                f"{user}に{role}を付与しました。\nGrant complete."),
            color=0x4169e1)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    @commands.has_role(713321552271376444)
    async def remove(self, ctx, user: typing.Union[discord.Member, str], roles: int):
        if isinstance(user, str):
            try:
                member = discord.utils.get(
                    self.guild.members, discriminator=user)
                user = self.guild.get_member(member.id)
                if user == None:
                    raise commands.BadArgument()
            except ValueError:
                raise commands.BadArgument()
        role = self.guild.get_role(roles)
        await user.remove_roles(role)
        embed = discord.Embed(
            title="Done.",
            description=(
                f"{user}から{role}を剥奪しました。\nDeprivation complete."),
            color=0x4169e1)
        await ctx.send(embed=embed)
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
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="Error",
                description=(
                    f"不正な引数です！\nInvalid argument passed."),
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
    bot.add_cog(Management(bot))
