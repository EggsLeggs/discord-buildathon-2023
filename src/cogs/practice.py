import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, Option
from datetime import datetime
import json
import os
import random


# TODO - This should not be global, consider moving it into a class or something that can be passed through class instances
def generate_answers(answer, possible_answers):
    answers = []
    answers.append(answer)
    # Add 4 random answers to the list of possible answers, no duplicates and don't remove answers in this list
    while len(answers) < 5:
        answer = possible_answers[random.randint(0, len(possible_answers) - 1)]
        if answer not in answers:
            answers.append(answer)
    random.shuffle(answers)
    return answers


class QuizView(discord.ui.View):
    def __init__(self, quiz, answers):
        self.quiz = quiz
        self.answers = answers
        super().__init__(timeout=60)  # Timeout after 60 seconds
        with open(
            f"{os.getcwd()}/src/dict/practice/en.json", "r", encoding="utf-8"
        ) as f:
            self.en_dict = json.load(f)

    async def callback(self, button, interaction):
        self.disable_all_items()
        result = self.quiz["questions"].pop(0)
        was_correct = result["romaji"] == self.answers[int(button.label) - 1]
        await self.message.edit(
            embed=self.generate_question(
                result["kana"],
                self.answers,
                "correct" if was_correct else "incorrect",
                answer=self.answers[int(button.label) - 1],
                correctAnswer=result["romaji"],
            ),
            view=self,
        )
        self.quiz["completed"].append(result | {"wasCorrect": was_correct})
        if len(self.quiz["questions"]) == 0:
            return await interaction.response.send_message(
                embed=self.generate_finish(),
            )
        answers = generate_answers(
            self.quiz["questions"][0]["romaji"], self.quiz["possible-letters"]
        )
        await interaction.response.send_message(
            embed=self.generate_question(
                self.quiz["questions"][0]["kana"], answers, "question"
            ),
            view=QuizView(self.quiz, answers),
        )

    def generate_question(self, kana, answers, state, answer=None, correctAnswer=None):
        body = ""
        for i, possibleAnswer in enumerate(answers):
            body += (
                f"{i + 1} - {possibleAnswer} "
                + (" ✅" if possibleAnswer == correctAnswer else "")
                + (
                    " ❌"
                    if possibleAnswer == answer and possibleAnswer != correctAnswer
                    else ""
                )
                + "\n"
            )
        embed = discord.Embed(
            title=self.en_dict["question"]["title"].format(kana=kana),
            description=body,
            color=int(self.en_dict["question"]["colors"][state], 16),
        )
        embed.set_image(
            url=self.en_dict["image"],
        )
        return embed

    def generate_finish(self):
        total = len(self.quiz["completed"])
        correct = 0
        for result in self.quiz["completed"]:
            if result["wasCorrect"]:
                correct += 1
        incorrect = total - correct
        embed = discord.Embed(
            title=self.en_dict["finish"]["title"].format(correct=correct, total=total),
            description=self.en_dict["finish"]["body"],
            color=int(self.en_dict["color"], 16),
        )
        embed.set_footer(
            text=self.en_dict["finish"]["footer"].format(
                time=datetime.today().strftime("%Y/%m/%d")
            )
        )
        embed.set_image(
            url=self.en_dict["image"],
        )
        return embed

    @discord.ui.button(label="1", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        await self.callback(button, interaction)

    @discord.ui.button(label="2", style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        await self.callback(button, interaction)

    @discord.ui.button(label="3", style=discord.ButtonStyle.primary)
    async def third_button_callback(self, button, interaction):
        await self.callback(button, interaction)

    @discord.ui.button(label="4", style=discord.ButtonStyle.primary)
    async def forth_button_callback(self, button, interaction):
        await self.callback(button, interaction)

    @discord.ui.button(label="5", style=discord.ButtonStyle.primary)
    async def fifth_button_callback(self, button, interaction):
        await self.callback(button, interaction)


class StartView(discord.ui.View):
    def __init__(self, quiz):
        self.quiz = quiz
        super().__init__(timeout=60)  # Timeout after 60 seconds
        with open(
            f"{os.getcwd()}/src/dict/practice/en.json", "r", encoding="utf-8"
        ) as f:
            self.en_dict = json.load(f)

    # TODO: this triggers when the view times out, even if the button was already clicked
    async def on_timeout(self):
        self.disable_all_items()
        await self.message.edit(embed=self.get_timeout_message(), view=self)

    @discord.ui.button(label="Get Started!", style=discord.ButtonStyle.green)
    async def button_callback(self, button, interaction):
        self.disable_all_items()
        answers = generate_answers(
            self.quiz["questions"][0]["romaji"], self.quiz["possible-letters"]
        )
        await self.message.edit(embed=self.get_started_message(), view=self)
        quiz = QuizView(self.quiz, answers)
        await interaction.response.send_message(
            embed=quiz.generate_question(
                self.quiz["questions"][0]["kana"], answers, "question"
            ),
            view=quiz,
        )

    def get_timeout_message(self):
        embed = discord.Embed(
            description=self.en_dict["start"]["timeout"]["body"],
            color=int(self.en_dict["color"], 16),
        )
        embed.set_image(
            url=self.en_dict["image"],
        )
        return embed

    def get_started_message(self):
        embed = discord.Embed(
            description=self.en_dict["start"]["started"]["body"],
            color=int(self.en_dict["color"], 16),
        )
        embed.set_image(
            url=self.en_dict["image"],
        )
        return embed


class PracticeCog(commands.Cog):
    def __init__(
        self, bot
    ):  # this is a special method that is called when the cog is loaded
        self.bot = bot
        with open(
            f"{os.getcwd()}/src/dict/practice/en.json", "r", encoding="utf-8"
        ) as f:
            self.en_dict = json.load(f)

    practiceGroup = SlashCommandGroup(
        "practice",
        "Practice Hiragana and Katakana.",
    )

    @practiceGroup.command(name="hiragana", description="Practice Hiragana.")
    async def learn_hiragana(
        self,
        ctx: discord.ApplicationContext,
        exclude: Option(
            str,
            "Exclude Hiragana characters.",
            required=False,
        ),
        include: Option(
            str,
            "Include Hiragana characters.",
            required=False,
        ),
    ):
        await ctx.respond(embed=self.get_info_message())
        # Create a thread to play the game in
        message = await ctx.interaction.original_response()
        thread = await message.create_thread(name="Kana Quiz", auto_archive_duration=60)
        await thread.send(
            embed=self.get_start_message(),
            view=StartView(self.generate_quiz(exclude, include)),
        )

    def get_start_message(self):
        embed = discord.Embed(
            description=self.en_dict["start"]["body"],
            color=int(self.en_dict["color"], 16),
        )
        embed.set_image(
            url=self.en_dict["image"],
        )
        return embed

    def get_info_message(self):
        embed = discord.Embed(
            title=self.en_dict["info"]["title"],
            description=self.en_dict["info"]["body"],
            color=int(self.en_dict["color"], 16),
        )
        embed.set_author(name=" Menu", icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(
            url="https://cdn-icons-png.flaticon.com/512/4474/4474828.png"
        )
        embed.set_image(
            url=self.en_dict["image"],
        )
        embed.set_footer(
            text=self.en_dict["info"]["footer"].format(
                time=datetime.today().strftime("%Y/%m/%d")
            ),
        )  # footers can have icons too
        return embed

    def generate_quiz(self, exclude, include):
        # TODO - This can be optimized by not loading the dictionary every time
        options = {
            "all-main-kana": {
                "a": "あ",
                "ka": "か",
                "sa": "さ",
                "ta": "た",
                "na": "な",
                "ha": "は",
                "ma": "ま",
                "ya": "や",
                "ra": "ら",
                "wa": "わ",
            },
            "all-dakuten-kana": {
                "ga": "が",
                "za": "ざ",
                "da": "だ",
                "ba": "ば",
                "pa": "ぱ",
            },
            "all-combination-kana": {
                "kya": "きゃ",
                "sha": "しゃ",
                "cha": "ちゃ",
                "nya": "にゃ",
                "hya": "ひゃ",
                "mya": "みゃ",
                "rya": "りゃ",
                "gya": "ぎゃ",
                "ja": "じゃ",
                "dya": "ぢゃ",
                "bya": "びゃ",
                "pya": "ぴゃ",
            },
        }

        allKana = [
            value for sub_dict in options.values() for value in sub_dict.values()
        ]
        allRomaji = [key for sub_dict in options.values() for key in sub_dict.keys()]
        translations = {
            **options["all-main-kana"],
            **options["all-dakuten-kana"],
            **options["all-combination-kana"],
        }

        excludedList = self.convert_option(
            exclude, options, allKana, allRomaji, translations
        )
        reAddList = self.convert_option(
            include, options, allKana, allRomaji, translations
        )

        includedList = [kana for kana in allKana if kana not in excludedList]
        includedList = list(set(includedList + reAddList))
        with open(
            f"{os.getcwd()}/src/config/dictionary.json", "r", encoding="utf-8"
        ) as f:
            dictionary = json.load(f)
        quiz = {
            "completed": [],
            "questions": [],
            "possible-letters": [],
        }

        for alphabet in dictionary.keys():
            for kanaGroup in dictionary[alphabet].keys():
                for kanaSubGroup in dictionary[alphabet][kanaGroup].keys():
                    if kanaSubGroup in includedList:
                        for kana in dictionary[alphabet][kanaGroup][kanaSubGroup]:
                            quiz["questions"].append(kana)
                            quiz["possible-letters"].append(kana["romaji"])
        return quiz

    def convert_option(self, option, options, allKana, allRomaji, translations):
        # Valid options:
        characters = []
        if option is not None:
            characters = option.split(" ")
            # Remove any options that aren't a key of options or a key or item of each option
            characters = [
                option
                for option in characters
                if option in options.keys() or option in allKana or option in allRomaji
            ]
            # Translate any romaji to kana
            characters = [translations.get(option, option) for option in characters]
            # Expand any kana sets to the kana values nested inside (eg. "all-main-kana" -> ["a", "ka", "sa", ...])
            for character in characters[:]:
                if character in options.keys():
                    characters.remove(character)
                    characters.extend(options[character].values())
            # Remove any duplicates
            characters = list(set(characters))
        return characters


def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(PracticeCog(bot))  # add the cog to the bot
