import discord
from discord.ext import commands


class management(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def protect(self, ctx, member: discord.Member):
        guild = self.bot.get_guild(711374787892740148)
        unei = guild.get_role(713321552271376444)
        if unei not in ctx.author.roles:
            await ctx.channel.send("あなたにはその権限がありません。")
            return
        seigen = guild.get_role(714733639505543222)
        normal = guild.get_role(711375295172706313)
        await member.remove_roles(normal)
        await member.add_roles(seigen)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(management(bot))
