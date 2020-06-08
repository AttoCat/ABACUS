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
            return
        elif self.keikoku in member.roles:
            await member.remove_roles(self.keikoku)
            return
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


def setup(bot):
    bot.add_cog(Management(bot))
