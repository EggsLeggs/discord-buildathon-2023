import discord
import os  # default module
import logging
from dotenv import load_dotenv

settings = {"debug": False}

# TODO: to setup file logger:
# https://github.com/boilercodes/pycord/blob/main/bot/__init__.py

# Console handler prints to terminal.
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG if settings["debug"] else logging.INFO)

# Format configuration.
fmt = "%(asctime)s - %(name)s %(levelname)s: %(message)s"
datefmt = "%H:%M:%S"

# Remove old loggers, if any.
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)

# Silence irrelevant loggers.
logging.getLogger("discord").setLevel(logging.INFO)
logging.getLogger("discord.gateway").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)

# Setup new logging configuration.
logging.basicConfig(
    format=fmt,
    datefmt=datefmt,
    level=logging.DEBUG,
    handlers=[console_handler],
)

log = logging.getLogger(__name__)

bot = discord.Bot()


@bot.event
async def on_ready():
    log.info("Started bot as %s", bot.user)


# get all the files in the cogs directory where ends in .py
cogs_list = [cog[:-3] for cog in os.listdir("src/cogs") if cog.endswith(".py")]

for cog in cogs_list:
    log.info("Loading cog %s", cog)
    bot.load_extension(f"cogs.{cog}")

# if bot_token environment variable is not set, then use the token from the .env file
bot_token = ""
try:
    bot_token = os.environ["BOT_TOKEN"]
except KeyError:
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")

bot.run(bot_token)  # run the bot with the token
