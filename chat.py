"""Chat cog.

Contains many all chat-related commands.

"""
import random
from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone
from discord.ext import commands
from chatterbot import ChatBot
from translate import Translator
import wikiquote


class Chat(object):
    """Card cog."""

    def __init__(self, bot):
        """Initalization function."""
        self.bot = bot
        self.chatbot = ChatBot("Ron Obvious")
        self.chatbot.train("chatterbot.corpus.english")

    @commands.command()
    async def say(self, *text):
        """Echos what you say.

        Keyword arguments:
        *text -- Text to echo

        """
        await self.bot.say(' '.join(text))

    @commands.command()
    async def ping(self):
        """Says 'Pong'.

        Keyword arguments:
        None

        """
        await self.bot.say('Pong')

    @commands.command()
    async def decide(self, *options):
        """Decides between multiple options

        **Use double quotes for each option**

        Keyword arguments:
        options

        """
        if len(options) < 2:
            await self.bot.say('Not enough options to choose from')
        else:
            await self.bot.say(random.choice(options))

    @commands.command()
    async def translate(self, language, *text):
        """Translates text from English to specified language

        **Use double quotes for each option**

        **Dependencies**: pip install translate
                          (https://github.com/terryyin/google-translate-python)

        Keyword arguments:
        language -- Two-letter code for the languate to translate to
        text -- Text to translate.

        """
        text_to_string = ''.join(text)
        translator = Translator(to_lang=language)
        translation = translator.translate(text_to_string)

        await self.bot.say(translation)

    @commands.command()
    async def talk(self, *message):
        """Speak to ChatterBot.

        It uses ChatterBot, is a machine-learning based
        conversational dialog engine build in Python which makes
        it possible to generate responses based on collections of
        known conversations

        **Dependencies**: pip install chatterbot

        Keyword arguments:
        message -- Message to send to the chatbot.

        """
        reply = self.chatbot.get_response(" ".join(message))
        await self.bot.say(reply, tts=True)

    @commands.command()
    async def quote(self, choice):
        """Generating a random quote or get the quote of the day.

        **Dependencies**: pip install wikiquote

        Keyword arguments:
        choice -- either 'QOTD' (Quote of the day) or 'R' (Random)

        """

        if choice.upper() == 'QOTD':
            quote = wikiquote.quote_of_the_day()
            await self.bot.say("'{}' -- {}".format(quote[0], quote[1]))
        elif choice.upper() == 'R':
            while True:
                authors = wikiquote.random_titles(max_titles=5)
                random_author = random.choice(authors)
                if random_author.isdigit():
                    continue
                random_quote = random.choice(wikiquote.quotes(random_author))
                await self.bot.say("'{}' -- {}"
                                   .format(random_quote,
                                           random_author))
                break

    @commands.command()
    async def time(self, timezone_code):
        """Return current time and time in the timezone listed.

        **Dependencies**: pip install pytz tzlocal

        Keyword arguments:
        timezone_code  -- Code for timezone
        """
        local_time = datetime.now(get_localzone())
        converted_time = datetime.now(timezone(timezone_code.upper()))
        await self.bot.say("```Local time : {} \n\n   {}     : {}```"
                           .format(local_time, timezone_code, converted_time))


def setup(bot):
    """Called when cog is loaded via load_extension()."""
    bot.add_cog(Chat(bot))
