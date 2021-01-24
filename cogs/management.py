import asyncio

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

    @commands.Cog.listener()
    async def on_message(self, message):  # メンションユーザー操作機能
        if message.author.bot:
            return
        if message.channel.name != "user-management":
            return
        try:  # discord.Messageからdiscord.Contextに変換しcontentをコンバート
            member = await commands.MemberConverter().convert(await self.bot.get_context(message), message.content)
        except commands.errors.BadArgument:  # コンバートできない=メンションやIDじゃない→削除
            await message.delete()
            return

        # memberが運営、自身、ABACUSの場合はエラー
        if self.unei in member.roles:
            await message.delete()
            await message.channel.send(
                (
                    "運営またはABACUSに対して変更を加えることは出来ません！\n"
                    "You can't make changes to managers and ABACUS."), delete_after=5)
            return
        elif member == message.author:
            await message.delete()
            await message.channel.send(
                (
                    "自身に対して変更を加えることは出来ません！\n"
                    "You can't make changes to yourself."), delete_after=5)
            return

        await message.delete()  # 元のメンションやIDは削除しておく
        panel_embed = discord.Embed(
            title="Operation Panel",
            description=f"{str(member)}に変更を加えます。\nMake changes to {str(member)}.\n(Within 60sec)",
            color=0x03b50f
        )
        timeout_embed = discord.Embed(
            title="Timeout",
            description=(
                "時間切れです。\nPanel will be deleted automatically."),
            color=0xff8800)
        emojis = []
        datum = {
            "Kick": "をキック", "BAN": "をBAN",
            "To Limit": "を制限付きに", "To Caution": "に注意役職を付与",
            "To Warning": "に警告役職を付与", "Lift Admonitions": "の注意系役職を全解除"
        }
        panel = await message.channel.send(embed=panel_embed)
        for num, data in enumerate(datum):
            emoji = chr(0x0001f1e6 + num)
            panel_embed.add_field(
                name=f"{emoji}:{data}",
                value=f"ユーザー{datum[data]}します。", inline=False
            )
            await panel.add_reaction(emoji)
            emojis.append(emoji)
        await panel.add_reaction("❌")
        emojis.append("❌")
        await panel.edit(embed=panel_embed)

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) in emojis
        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add",
                timeout=60.0,
                check=check)
        except asyncio.TimeoutError:
            await panel.clear_reactions()
            await panel.edit(embed=timeout_embed)
            await asyncio.sleep(5)
            await panel.delete()
            return
        else:
            number = emojis.index(str(reaction.emoji))  # 何個目のリアクションなのか記録

        cancel_embed = discord.Embed(
            title="Canceled",
            description=(
                "操作をキャンセルしました。パネルは自動で削除されます。\n"
                "Panel will be deleted automatically."),
            color=0xff8800
        )
    # 押されたリアクションが最後のもの(=❌)ならキャンセル
        if number == len(emojis) - 1:
            await panel.clear_reactions()
            await panel.edit(embed=cancel_embed)
            await asyncio.sleep(5)
            await panel.delete()
            return

    # 実際に操作を実行する関数。evalよりnumberの数字で条件分岐するほうがいいのか？
        async def execute(number):
            exec_list = [
                "guild.kick(member)", "guild.ban(member)", "member.add_roles(seigen)",
                "member.add_roles(tyuui)", "member.add_roles(keikoku)", "member.add_roles(seigen)"]
            attributes = {
                "guild": message.guild, "member": member,
                "seigen": self.seigen, "tyuui": self.tyuui,
                "keikoku": self.keikoku}
            if number < len(exec_list):
                await eval(exec_list[number], attributes)
                return

        check_embed = discord.Embed(
            title="Final confirmation",
            description=(
                f"**User**={member}\n"
                f"**Content**={list(datum.keys())[number]}\n\n"
                "実行する場合はOK,キャンセルする場合はNoと発言して下さい。\n"
                "Say OK or No.\n(Within 20sec)"),
            color=0xff0000)
        await panel.edit(embed=check_embed)
        await panel.clear_reactions()
        try:
            ok_no = await self.bot.wait_for(
                'message', timeout=20.0,
                check=lambda m: m.author == message.author and m.content.lower() in ["ok", "no"])
        except asyncio.TimeoutError:
            await panel.edit(embed=timeout_embed)
            await asyncio.sleep(5)
            await panel.delete()
            return

        if ok_no.content.lower() == "ok":
            await execute(number)  # ここで実行
            done_embed = discord.Embed(
                title="Execution complete",
                description=(
                    "実行が完了しました。パネルは自動で削除されます。\n"
                    "Panel will be deleted automatically."
                ),
                color=0x4169e1)
            await panel.edit(embed=done_embed)
            await asyncio.sleep(5)
            await panel.delete()
            return
        else:  # Noと言われればキャンセル
            await panel.edit(embed=cancel_embed)
            await asyncio.sleep(5)
            await panel.delete()
            return


def setup(bot):
    bot.add_cog(Management(bot))
