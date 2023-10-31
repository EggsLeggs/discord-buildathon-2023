import discord
import os  # default module
from dotenv import load_dotenv

load_dotenv()  # load all the variables from the env file
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

# get all the files in the cogs directory where ends in .py
cogs_list = [cog[:-3] for cog in os.listdir('src/cogs') if cog.endswith('.py')]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')

bot.run(os.getenv('TOKEN'))  # run the bot with the token
