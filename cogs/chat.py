from random import choice
from discord.ext import commands
from chatterbot import ChatBot
from  translate import Translator


# Chat cog
class Chat:

    def __init__(self, bot):
        self.bot = bot

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
            await self.bot.say(choice(options))

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
        translator = Translator(to_lang = language)
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

        chatbot = ChatBot("Ron Obvious")
        #chatbot.train("chatterbot.corpus.english")
        msg = ctx.message.content
        reply = chatbot.get_response(msg)

        await self.bot.send_message(ctx.message.channel, reply, tts=True)


def setup(bot):
    bot.add_cog(Chat(bot))
