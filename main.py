import asyncio
import asyncpg
import discord
from discord.ext import commands
import dotenv
import os
import signal
import ssl
import traceback

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX")
DATABASE_URL = os.getenv("DATABASE_URL")
EXTENSIONS = [
    "cogs.scan", "cogs.management",
    "cogs.play", "cogs.event", "cogs.special", "cogs.database"]


def handler(signum, frame):
    print("シグナルをスルー")  # test
    return


signal.signal(signal.SIGTERM, handler)


class Hiikun(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)

        for cog in EXTENSIONS:
            try:
                self.load_extension(cog)
                print(f"Loaded Extension {cog}.py.")
            except Exception:
                traceback.print_exc()

    async def setup(self):
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            bot.conn = await asyncpg.connect(DATABASE_URL, ssl=context)
        except Exception as e:
            print(e)
            print(e.__class__)
            return

    async def on_ready(self):
        print(f"Bot is ready! \nlibrary version:{discord.__version__}")
        await self.setup()

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            content = "あなたにこのコマンドを実行する権限がありません！\nYou don't have permission."
        elif isinstance(error, commands.BadArgument):
            content = "不正な引数です！\nInvalid argument passed."
        elif isinstance(error, commands.MissingRequiredArgument):
            content = "想定しない引数が渡されました！\nInvalid input."
        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, discord.NotFound):
                content = "メッセージが見つかりませんでした！\nMessage not found."
            else:
                content = f"不明なエラーが発生しました。\nエラー内容：\n{error}"
        elif isinstance(error, commands.TooManyArguments):
            content = "引数の数が不正です！\nInvalid input."
        else:
            content = f"不明なエラーが発生しました。\nエラー内容:\n{error}"
        embed = discord.Embed(
            title="Error", description=content, color=0xff0000)
        await ctx.message.delete()
        await ctx.send(embed=embed)


if __name__ == '__main__':
    bot = Hiikun(command_prefix=PREFIX)
    bot.run(TOKEN)
