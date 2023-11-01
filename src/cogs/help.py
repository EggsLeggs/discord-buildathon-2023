import discord
from discord.ext import commands
from datetime import datetime
import json
import os
import logging

log = logging.getLogger(__name__)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open(f"{os.getcwd()}/src/dict/help/en.json", "r", encoding="utf-8") as f:
            self.en_dict = json.load(f)
        log.info("Loaded cog Help")

    @commands.slash_command(name="help")
    async def help(self, ctx: discord.ApplicationContext):
        log.info("Help command invoked by %s", ctx.author)
        # This could be optimized by including it in the init
        # This would remove the ability to change the language in the future though
        main_embed = discord.Embed(
            title=self.en_dict["title"],
            description=self.en_dict["body"],
            color=int(self.en_dict["color"], 16),
        )
        main_embed.set_author(name="Help Menu", icon_url=self.bot.user.avatar.url)
        main_embed.set_thumbnail(
            url="https://cdn-icons-png.flaticon.com/512/4474/4474828.png"
        )
        main_embed.set_image(
            url=self.en_dict["image"],
        )
        main_embed.set_footer(
            text=self.en_dict["footer"].format(
                time=datetime.today().strftime("%Y/%m/%d")
            ),
        )  # footers can have icons too

        hiragana_embed = discord.Embed(
            title=self.en_dict["hiragana"]["title"],
            description=self.en_dict["hiragana"]["body"],
            color=int(self.en_dict["color"], 16),
        )
        hiragana_embed.set_image(
            url=self.en_dict["image"],
        )
        for field in self.en_dict["hiragana"]["fields"]:
            hiragana_embed.add_field(
                name=field["title"],
                value=field["body"],
                inline=True,
            )

        katakana_embed = discord.Embed(
            title=self.en_dict["katakana"]["title"],
            description=self.en_dict["katakana"]["body"],
            color=int(self.en_dict["color"], 16),
        )
        katakana_embed.set_image(
            url=self.en_dict["image"],
        )
        for field in self.en_dict["katakana"]["fields"]:
            katakana_embed.add_field(
                name=field["title"],
                value=field["body"],
                inline=True,
            )

        await ctx.respond(embeds=[main_embed, hiragana_embed, katakana_embed])
        log.info("Help command completed for %s", ctx.author)


def setup(bot):
    bot.add_cog(Help(bot))
