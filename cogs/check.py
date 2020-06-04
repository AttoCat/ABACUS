import discord
from discord.ext import commands
from janome.tokenizer import Tokenizer
t = Tokenizer()


class Check(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        member = message.author
        if member.bot:
            return
        out_list = [
            "死ね", "氏ね", "ﾀﾋね", "シネ", "クズ", "消えろ", "カス", "キチガイ", "基地外",
            "きちがい", "ふぁっきゅ", "fack you", "Fack you",
            "ファッキュ", "ふぁっくゆー", "ファックユー", "f**k"]
        moji = message.content
        kekka = t.tokenize(moji, wakati=True)
        print(kekka)
        for word in kekka:
            if word in out_list:
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


def setup(bot):
    bot.add_cog(Check(bot))
