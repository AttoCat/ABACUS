import discord
from discord.ext import commands


class Event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(711374787892740148)
        self.dev = self.guild.get_member(602668987112751125)
        self.rank = self.guild.get_channel(713389883569340436)
        self.hiibot = self.guild.get_member(727164114513690688)
        self.log = self.guild.get_channel(715154878166466671)
        self.kakutyousi = (".jpg", ".jpeg", ".png")

    @commands.command()
    async def devdm(self, ctx, *, naiyou):
        embed = discord.Embed(
            title="メッセージが届きました！",
            description=(
                f"{naiyou}\n送信者:{ctx.author}"),
            color=0x4169e1)
        await self.dev.send(embed=embed)
        embed = discord.Embed(
            title="Done.",
            description=(
                f"正常に送信しました。\nMessage sent successfully. "),
            color=0x4169e1)
        await ctx.channel.send(embed=embed, delete_after=10)
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel == self.rank:
            mee6 = self.guild.get_member(159985870458322944)
            if message.author == mee6:
                return
            elif not message.content.startswith("!rank"):
                await message.delete()
                return
        if message.channel.is_nsfw():
            if not message.attachments:
                return
            for attachment in message.attachments:
                if not attachment.url.endswith(self.kakutyousi):
                    return
                if "SPOILER_" in attachment.url:
                    return print("tessssssssssst")
                else:
                    print("goooooooooood")
                    print(attachment.url)
                    print(message.content)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.hiibot.status == discord.Status.online:
            return
        ch = self.guild.get_channel(711375652107976847)
        rule = self.guild.get_channel(711379195992997949)
        yaku = self.guild.get_channel(712410294496002090)
        naiyou = (
            f"{member.mention}さんようこそBOTのすべてへ！\n"
            f"まずは{rule.mention}でルールを確認し、同意する場合は{yaku.mention}でその他の役職をもらいましょう！")
        embed = discord.Embed(
            title=(f"{member.display_name}さんが参加しました！"),
            description=naiyou,
            color=0x3aee67)
        await ch.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.hiibot.status == discord.Status.online:
            return
        ch = self.guild.get_channel(711375652107976847)
        naiyou = (
            f"{member.display_name}さん、BOTのすべてのご利用ありがとうございました。またのお越しをお待ちしております。")
        embed = discord.Embed(
            title=(f"{member.display_name}さんが退出しました。\n"),
            description=naiyou,
            color=0xff0000)
        await ch.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def say(self, ctx, *, naiyou: str):
        await ctx.message.delete()
        await ctx.send(naiyou)

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


def setup(bot):
    bot.add_cog(Event(bot))
