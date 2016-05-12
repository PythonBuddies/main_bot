__author__ = 'pico'

from discord.ext import commands
import random
import aiohttp
import asyncio


# reddit pics cog
class RedditPics:

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.command(hidden=True)
    async def sub(self, *message):
        if len(message) == 0:
            await self.bot.say("Usage: sub r/<subreddit name>")
        elif len(message) > 1:
            await self.bot.say("Too many parameters.")
        elif message[0].startswith("r/") or message[0].startswith("/r/"):
            subreddit = message[0][message[0].rindex("/")+1:].strip()
            await self.execute_request(subreddit)
        else:
            await self.bot.say("Invalid syntax.")

    async def execute_request(self, subreddit):

        # download top reddit images for a given subreddit
        reddit_results = await self.fetch(self.session, subreddit)
        reddit_results = reddit_results['data']['children']

        # if no posts are found, exit
        if len(reddit_results) == 0:
            await self.bot.say("No results found.")

        # randomly pick a post from the above results
        post = self.get_random_post(reddit_results)

        if post == None:
            # if no images were found in the results, exit
            await self.bot.say("No image results found.")
        else:
            # this is where the bot replies with what she found
            await self.bot.say(post)

    # connect to reddit and download the top posts of all time for that subreddit (limit 25)
    # TODO make this function download multiple pages of 25 posts for better result variety
    async def fetch(self, session, subreddit):
        header = {'User-Agent': 'trying to learn this async thing'}
        url = "https://www.reddit.com/r/{0}/top/.json?sort=top&t=all".format(subreddit)

        with aiohttp.Timeout(10):
            async with session.get(url, headers=header) as response:
                return await response.json()

    # pick a random post from the results, ensure that post is an image and is SFW
    # return None if no images found
    def get_random_post(self, reddit_results: list):
        picture_list = []

        for item in reddit_results:
            if "imgur" in item['data']['url']:
                if item['data']['over_18']:
                    continue
                picture_list.append(item['data']['url'])

        if len(picture_list) == 0:
            self.bot.say("Could not retrieve a picture from the results.")
            return None
        else:
            return random.choice(picture_list)

def setup(bot):
    bot.add_cog(RedditPics(bot))

