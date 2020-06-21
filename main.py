import os
import dotenv
import discord
from discord.ext import commands
import traceback

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX")
EXTENSIONS = [
    "cogs.check", "cogs.management",
    "cogs.event", "cogs.play", "cogs.special"]


# class Help(commands.DefaultHelpCommand):
#     def __init__(self):
#         super().__init__()
#         self.no_category = "カテゴリ未設定"
#         self.command_attrs["description"] = "コマンドリストを表示します。"

#     async def send_bot_help(self, mapping):
#         content = ""
#         for cog in mapping:
#             # 各コグのコマンド一覧を content に追加していく
#             command_list = await self.filter_commands(mapping[cog])
#             if not command_list:
#                 # 表示できるコマンドがないので、他のコグの処理に移る
#                 continue
#             if cog is None:
#                 # コグが未設定のコマンドなので、no_category属性を参照する
#                 content += f"```\n{self.no_category}```"
#             else:
#                 content += f"```\n{cog.qualified_name} / {cog.description}\n```"
#             for command in command_list:
#                 content += f"`{command.name}` / {command.description}\n"
#             content += "\n"
#         embed = discord.Embed(
#             title="コマンドリスト",
#             description=content, color=0x00ff00)
#         embed.set_footer(text=f"コマンドのヘルプ {self.context.prefix}help コマンド名")
#         await self.get_destination().send(embed=embed)


class Hiikun(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)

        for cog in EXTENSIONS:
            try:
                self.load_extension(cog)
                print(f"Loaded Extension {cog}.py.")
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print(f"Bot is ready! \nlibrary version:{discord.__version__}")


if __name__ == '__main__':
    bot = Hiikun(command_prefix=PREFIX)
    bot.run(TOKEN)
