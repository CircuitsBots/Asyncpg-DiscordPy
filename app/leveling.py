import discord
from discord.ext import commands

from .bot import Bot


class Leveling(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if not message.guild:
            return
        await self.bot.create_data(message)
        await self.bot.db.execute(
            """UPDATE members SET total_messages = total_messages + 1
            WHERE user_id=$1 AND guild_id=$2""",
            message.author.id, message.guild.id
        )
        await self.bot.db.execute(
            """UPDATE guilds SET total_messages = total_messages + 1
            WHERE id=$1""",
            message.guild.id
        )

    @commands.command(
        name="xp",
        brief="Shows the number of messages you or another user has sent"
    )
    @commands.guild_only()
    async def show_messages(
        self, ctx: commands.Context, user: discord.Member = None
    ) -> None:
        user = user or ctx.author
        sql_user = await self.bot.db.fetchrow(
            """SELECT * FROM members
            WHERE user_id=$1 AND guild_id=$2""",
            user.id, ctx.guild.id
        )
        if not sql_user:
            await ctx.send("That user has not sent any messages.")
            return
        total = sql_user["total_messages"]
        if user.id == ctx.author.id:
            await ctx.send(f"You have sent {total} message(s).")
        else:
            await ctx.send(f"{user} has sent {total} message(s).")


def setup(bot: Bot) -> None:
    bot.add_cog(Leveling(bot))
