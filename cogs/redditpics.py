__author__ = 'pico'

from discord.ext import commands
import requests, random, json

# reddit pics cog
class RedditPics:

    def __init__(self, bot):
        self.bot = bot

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
            await self.bot.say("Looking up info for {}".format(subreddit))

            # do stuff
            full_json_top = self.get_reddit_top(subreddit)
            print(full_json_top)
            #print(self.get_random_post(full_json_top))

        else:
            await self.bot.say("Invalid syntax.")
            return


    async def get_reddit_top(self, subreddit):
        url = "https://www.reddit.com/r/{0}/top/.json".format(subreddit)
        client = requests.session()
        client.get(url)
        reddit_reply = await client.post(url)
        if len(reddit_reply['data']['children']) == 0:
            self.bot.say("No posts found.")
        else:
            return reddit_reply.text

    def get_random_post(self,reddit_reply: json):
        return random.choice(reddit_reply['data']['children'])









    async def receive_message(self, message):
        if message.author.id == self.bot.user.id:
            return

def setup(bot):
    redditpics = RedditPics(bot)
    bot.add_listener(redditpics.receive_message, "on_message")
    bot.add_cog(RedditPics(bot))

