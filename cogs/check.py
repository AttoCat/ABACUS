import discord
from discord.ext import commands


class check(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        out_list = [
            "死ね", "氏ね", "ﾀﾋね", "シネ", "クズ", "消えろ", "カス", "キチガイ", "基地外",
            "きちがい", "ふぁっきゅ", "fack you", "Fack you",
            "ファッキュ", "ふぁっくゆー", "ファックユー", "f**k"]
        if any((word in message.content) for word in out_list) or message.content.startswith("しね"):
            member = message.author
            seigen = message.guild.get_role(714733639505543222)
            normal = message.guild.get_role(711375295172706313)
            await message.delete()
            embed = discord.Embed(
                title="Message deleted",
                description=f"""暴言が含まれていたため、削除しました。
                {str(message.author)}:{message.content}""",
                color=0xff0000)
            await member.remove_roles(normal)
            await member.add_roles(seigen)
            await message.channel.send(
                embed=embed)


def setup(bot):
    bot.add_cog(check(bot))
