import os
import ssl
import traceback

import asyncpg
import discord
import dotenv
from discord.ext import commands
from discord.ext.commands.bot import when_mentioned_or

dotenv.load_dotenv()


TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX")
DATABASE_URL = os.getenv("DATABASE_URL")
EXTENSIONS = [
    "cogs.scan", "cogs.management",
    "cogs.play", "cogs.event", "cogs.special", "cogs.database"]


class Abacus(commands.Bot):
    def __init__(self, command_prefix):
        Intents = discord.Intents.all()
        Intents.typing = False
        super().__init__(command_prefix, intents=Intents)

        for cog in EXTENSIONS:
            try:
                self.load_extension(cog)
                print(f"Loaded Extension {cog}.py.")
            except Exception:
                traceback.print_exc()

    async def setup(self):
        try:
            ctx = ssl.create_default_context(cafile='')
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            bot.conn = await asyncpg.connect(DATABASE_URL, ssl=ctx)
        except Exception:
            raise

    async def on_ready(self):
        print(f"Bot is ready! \nlibrary version:{discord.__version__}")
        await self.setup()
        channel = bot.get_channel(706779308211044352)
        await channel.send(f"{self.user}: 起動完了")

    async def on_command_error(self, ctx, error):
        content = None
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.NotOwner):
            content = "あなたにこのコマンドを実行する権限がありません！\nYou don't have permission."
        elif isinstance(error, commands.BadArgument):
            content = "不正な引数です！\nInvalid argument passed."
        elif isinstance(error, commands.MissingRequiredArgument):
            content = "想定しない引数が渡されました！\nInvalid input."
        elif isinstance(error, commands.TooManyArguments):
            content = "引数の数が不正です！\nInvalid input."
        elif isinstance(error, commands.CommandNotFound):
            content = "存在しないコマンドです。\nThe command is not available."
        elif isinstance(error, discord.HTTPException):
            if error.code == 10008:
                content = "メッセージが見つかりませんでした。"
            elif error.code == 10014:
                content = "絵文字が見つかりませんでした。"
        if content is None:
            content = f"不明なエラーが発生しました。\nエラー内容:\n{error}"
        embed = discord.Embed(
            title="Error", description=content, color=0xff0000)
        await ctx.message.delete()
        await ctx.send(embed=embed)


if __name__ == '__main__':
    bot = Abacus(command_prefix=when_mentioned_or([PREFIX, "ab.", "a!", "a."]))
    bot.run(TOKEN)
