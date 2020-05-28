import discord
from discord.ext import commands


class management(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def protect(self, ctx, member: discord.Member):
        self.guild = self.client.get_guild(711374787892740148)
        unei = self.guild.ger_role(713321552271376444)
        if ctx.author.roles not in unei:
            await ctx.channel.send("あなたにはその権限がありません。")
            return
        seigen: discord.Role = self.guild.get_role(714733639505543222)
        normal: discord.Role = self.guild.get_role(711375295172706313)
        await member.remove_roles(normal)
        await member.add_roles(seigen)


def setup(bot):
    bot.add_cog(management(bot))
