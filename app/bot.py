import typing

import discord
from discord.ext import commands

if typing.TYPE_CHECKING:
    from .database import Database


EXTENSIONS = [
    "app.leveling"
]


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        self.db: Database = kwargs.pop("database")
        super().__init__(*args, **kwargs)

        for ext in EXTENSIONS:
            self.load_extension(ext)

    async def before_invoke(self, ctx: commands.Context) -> None:
        await self.create_data(ctx.message)

    async def create_data(self, message: discord.Message) -> None:
        guild_exists = await self.db.fetchrow(
            """SELECT * FROM guilds WHERE id=$1""",
            message.guild.id
        ) is not None
        if not guild_exists:
            await self.db.execute(
                """INSERT INTO guilds (id) VALUES ($1)""",
                message.guild.id
            )

        user_exists = await self.db.fetchrow(
            """SELECT * FROM members WHERE user_id=$1
            AND guild_id=$2""",
            message.author.id, message.guild.id
        )
        if not user_exists:
            await self.db.execute(
                """INSERT INTO members (user_id, guild_id)
                VALUES ($1, $2)""",
                message.author.id, message.guild.id
            )

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user} in {len(self.guilds)} guilds!")
