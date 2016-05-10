__author__ = 'pico'

from discord.ext import commands
import requests, random, json, asyncio

# reddit pics cog
class RedditPics:

    def __init__(self, bot):
        self.bot = bot
        self.loop = asyncio.get_event_loop()

    @commands.command(hidden=True)
    async def sub(self, *message):
        if len(message) == 0:
            await self.bot.say("Help file goes here.")
            return
        elif len(message) > 1:
            await self.bot.say("Too many parameters.")
            return
        elif message[0].startswith("r/") or message[0].startswith("/r/"):
            subreddit = message[0][message[0].rindex("/")+1:].strip()
            self.bot.say("Looking up info for {}".format(subreddit))

            # do stuff
            self.get_reddit_top(subreddit)
            self.get_random_post(self.reddit_reply['data']['children'])

            await self.bot.say(self.random_post['data']['url'])
            return
        else:
            await self.bot.say("Invalid syntax.")
            return


    def get_reddit_top(self, subreddit):
        url = "https://www.reddit.com/r/{0}/top/.json".format(subreddit)
        client = requests.session()
        client.get(url)
        header = { 'User-Agent' : 'trying to learn this async thing' }
        reddit_reply = client.get(url, headers=header)
        self.reddit_reply =  reddit_reply.json()

    # not working yet, returns a random post
    def get_random_post(self,random_post: list):
        self.random_post = random.choice(random_post)






    async def receive_message(self, message):
        if message.author.id == self.bot.user.id:
            return

def setup(bot):
    redditpics = RedditPics(bot)
    bot.add_listener(redditpics.receive_message, "on_message")
    bot.add_cog(RedditPics(bot))

