import asyncio

from app.bot import Bot
from app.database import Database


TOKEN = "NjgyMjUzMzE5OTM4MjQ0NjA5.XlaT6w.HdCLdqG5Y1BkALCJnoOOIvtgQmo"

database = Database(
    "dbname", "dbuser", "dbpassword"
)
bot = Bot(
    database=database,
    command_prefix="!"
)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(database.open())
    bot.run(TOKEN)
