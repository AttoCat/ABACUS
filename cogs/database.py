import os

import dotenv
from discord.ext import commands

dotenv.load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def user_check(self, id):
        user = await self.bot.conn.fetchrow(
            """
            SELECT *
                FROM users
                WHERE id = $1;
            """,
            id,
        )
        return user

    @commands.command()
    async def register(self, ctx):
        if await self.user_check(ctx.author.id):
            await ctx.send("あなたは既にデータベースに登録されています！")
            return
        await self.bot.conn.execute(
            """
                INSERT INTO users VALUES ($1,DEFAULT);
                """,
            ctx.author.id,
        )
        await ctx.send("データベースに登録しました！")

    @commands.command()
    async def tag(self, ctx, *, text: str):
        user = await self.user_check(ctx.author.id)
        if not user:
            await ctx.send("あなたはデータベースに登録されていません！")
            return
        if not user["tag"]:
            content = "作成"
        else:
            content = "上書き"
        await self.bot.conn.execute(
            """
            UPDATE users
                SET tag=$1
            WHERE id = $2;
            """,
            text,
            ctx.author.id,
        )
        await ctx.send(f"タグを{content}しました！")

    @commands.command()
    async def me(self, ctx):
        user = await self.user_check(ctx.author.id)
        if not user:
            await ctx.send("あなたはデータベースに登録されていません！")
            return
        await ctx.send(f"あなたのタグは {user['tag']} です！")

    @commands.group(alias=["server", "g", "s"])
    async def guild(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("このコマンドにはサブコマンドが必要です。")
            return

    @guild.command(alias=["rs"])
    async def roleset():
        pass


def setup(bot):
    bot.add_cog(Database(bot))
