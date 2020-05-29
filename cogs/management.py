import discord
from discord.ext import commands


class management(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(711374787892740148)
        self.seigen = self.guild.get_role(714733639505543222)
        self.normal = self.guild.get_role(711375295172706313)
        self.unei = self.guild.get_role(713321552271376444)

    @commands.command()
    @commands.has_role(713321552271376444)
    async def protect(self, ctx, member: discord.Member):
        await member.remove_roles(self.normal)
        await member.add_roles(self.seigen)
        await ctx.message.delete()

    @commands.command()
    @commands.has_role(713321552271376444)
    async def fix(self, ctx, member: discord.Member):
        await member.remove_roles(self.seigen)
        await member.add_roles(self.normal)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(management(bot))
