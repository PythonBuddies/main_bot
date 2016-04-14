import random
from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone
from discord.ext import commands
from chatterbot import ChatBot
from translate import Translator
import wikiquote


# Chat cog
class Chat:

    def __init__(self, bot):
        self.bot = bot
        self.chatbot = ChatBot("Ron Obvious")
        self.chatbot.train("chatterbot.corpus.english")

    @commands.command(hidden=True)
    async def say(self, *text):     # !say text
        """Command that echos what you say.

        Keyword arguments:
        *text -- Text to echo
        """
        await self.bot.say(' '.join(text))

    @commands.command(hidden=True)
    async def ping(self):
        """Command that says 'Pong'.

        Keyword arguments:
        None
        """
        await self.bot.say('Pong')

    @commands.command()
    async def decide(self, *options):
        """Command that decided between multiple options
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
        """Command that translates text from english to specified language
        **Use double quotes for each option**

        **Dependencies**: pip install translate (https://github.com/terryyin/google-translate-python)

        **Keyword arguments**:
        language
        text
        """
        text_to_string = ''.join(text)
        translator = Translator(to_lang=language)
        translation = translator.translate(text_to_string)

        print(translation)
        await self.bot.say(translation)

    @commands.command(pass_context=True)
    async def talk(self, ctx):

        """Command that implements the talk to the bot function.
        It uses ChatterBot, is a machine-learning based
        conversational dialog engine build in Python which makes
        it possible to generate responses based on collections of
        known conversations

        **Dependencies**: pip install chatterbot

        **Keyword arguments**:
        chatbot -- stores chatbot object
        ctx     -- Context reference to get message
        tts     -- Set to true for text to speed implementation
        """
        msg = ctx.message.content
        reply = self.chatbot.get_response(msg)

        await self.bot.send_message(ctx.message.channel, reply, tts=True)

    @commands.command()
    async def quote(self, choice):

        """Command that implements the function of generating a
        random quote of the day.

        **Dependencies**: pip install wikiquote

        **Keyword arguments**:
        choice -- either 'QOTD' (Quote of the day) or 'R' (Random)
        """

        if choice == 'QOTD':
            q = wikiquote.quote_of_the_day()
            print(q[0])
            await self.bot.say("'" + q[0] + "'" + ' -- ' + q[1])
        elif choice == 'R':
            authors = []
            authors = wikiquote.random_titles(max_titles=5)
            if authors == []:
                authors = ['Dune', 'Johannes Kepler', 'Rosa Parks']
                random_author = random.choice(authors)
                await self.bot.say("'" + random.choice(wikiquote.quotes(random_author)) + "'")
            else:
                random_author = random.choice(authors)
                await self.bot.say("'" + random.choice(wikiquote.quotes(random_author)) + "'")

    @commands.command()
    async def time(self, t_z):
        """Command that returns current time and time in the timezone listed

        **Dependencies**: pip install pytz tzlocal

        **Keyword arguments**:
        t_z  -- timezone
        """
        local = get_localzone()
        local_time = datetime.now(local)
        required_timezone = timezone(t_z)
        converted_time = datetime.now(required_timezone)
        await self.bot.say("```Local time : {} \n\n   {}     : {}```".format(local_time, t_z, converted_time))

def setup(bot):
    bot.add_cog(Chat(bot))
