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
                "削除成功。\nDeletion successful."),
            color=0x4169e1)
        await ctx.message.delete()
        await ctx.channel.send(embed=embed, delete_after=3)

    @commands.command()
    @commands.has_role(713321552271376444)
    async def give(self, ctx, user: discord.Member, role: discord.Role):
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
    async def remove(self, ctx, user: discord.Member, role: discord.Role):
        await user.remove_roles(role)
        embed = discord.Embed(
            title="Done.",
            description=(
                f"{user}から{role}を剥奪しました。\nDeprivation complete."),
            color=0x4169e1)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.Cog.listener()  # メンションユーザー操作機能
    async def on_message(self, message):
        if message.author.bot:
            return
        try:
            member = await commands.MemberConverter().convert(await self.bot.get_context(message), message.content)
        except commands.errors.BadArgument:
            await message.delete()
            return
        embed = discord.Embed(
            title="Operation Panel",
            description=f"{str(member)}に変更を加えます。\nMake changes to {str(member)}.",
            color=0xff0000
        )
        emojis = []
        datum = {
            "Kick": "をキック", "BAN": "をBAN",
            "To Limit": "を制限付きに", "To Caution": "に注意役職を付与", "To Warning": "に警告役職を付与",
            "Lift Admonition": "の注意系役職を全解除"
        }
        panel = await message.channel.send(embed=embed)
        for num, data in enumerate(datum):
            emoji = chr(0x0001f1e6 + num)
            embed.add_field(
                name=f"{emoji}:{data}",
                value=f"ユーザー{datum[data]}します。", inline=False
            )
            await panel.add_reaction(emoji)
            emojis.append(emoji)
        await panel.add_reaction("❌")
        await panel.edit(embed=embed)

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) in emojis
        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add",
                timeout=60.0,
                check=check)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title="Timeout",
                description=(
                    "時間切れです。"),
                color=0xff0000)
            return
        else:
            number = emojis.index(str(reaction.emoji))
            print(number)

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

                def check(reaction, _user):
                    msg = str(reaction.emoji)
                    return _user == message.author and msg in bangou

                def check2(m):
                    lower = m.content.lower()
                    return m.author == message.author and lower in ["ok", "no"]

                while True:
                    content = [
                        "キック", "BAN", "制限付きに",
                        "注意役職を付与", "警告役職を付与", "注意系役職全解除"
                    ]
                    try:
                        reaction, _user = await self.bot.wait_for(
                            "reaction_add",
                            timeout=60.0,
                            check=check)
                    except asyncio.TimeoutError:
                        embed = discord.Embed(
                            title="Timeout",
                            description=(
                                "時間切れです。ログは10秒後に自動で削除されます。"),
                            color=0xff0000)
                        await message.channel.send(embed=embed)
                        await asyncio.sleep(10)
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
                                    "操作をキャンセルしました。ログは10秒後に自動で削除されます。"),
                                color=0xff0000)
                            await message.channel.send(embed=embed)
                            await asyncio.sleep(10)
                            await message.channel.purge(limit=None)
                            return
                        embed = discord.Embed(
                            title="最終確認",
                            description=(
                                f"{member}に対して{content[number]} を行います。"
                                "よろしいですか？\n"
                                "実行する場合はOK、キャンセルする場合はNOと発言してください！"),
                            color=0xff0000)
                        await message.channel.send(
                            embed=embed,
                            delete_after=50
                        )
                        try:
                            ok_no = await self.bot.wait_for(
                                'message',
                                timeout=20.0,
                                check=check2)
                        except asyncio.TimeoutError:
                            await message.channel.send("時間切れです")
                            break
                        if ok_no.content.lower() == "ok":
                            await sousa(sousa=number)
                            embed = discord.Embed(
                                title="Done.",
                                description=(
                                    "実行が完了しました。ログは10秒後に自動で削除されます。\n"
                                    "Execution complete."
                                ),
                                color=0x4169e1)
                            await message.channel.send(
                                embed=embed,
                                delete_after=20
                            )
                            await asyncio.sleep(10)
                            await message.channel.purge(limit=None)
                            return
                        else:
                            embed = discord.Embed(
                                title="Cancel",
                                description=(
                                    "操作をキャンセルしました。ログは10秒後に自動で削除されます。"),
                                color=0xff0000)
                            await message.channel.send(embed=embed)
                            await asyncio.sleep(10)
                            await message.channel.purge(limit=None)
                        break
                    break


def setup(bot):
    bot.add_cog(Management(bot))
