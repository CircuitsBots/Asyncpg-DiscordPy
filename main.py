import os
import asyncio

from dotenv import load_dotenv

from app.bot import Bot
from app.database import Database

load_dotenv()


TOKEN = os.getenv("TOKEN")

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
