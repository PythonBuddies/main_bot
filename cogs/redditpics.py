"""Module adds discord bot ability to randomly pick a top rated image from
a user-specified subreddit and outputs the url to the chat room."""

import random
from discord.ext import commands
import aiohttp


class RedditPics:
    """Reddit pics cog. Fetches random top post from a user-specified subreddit.
    Must be an image."""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.command(hidden=True)
    async def sub(self, *message):
        """Executed when bot is triggered. Accepts r/<subreddit> as an argument."""
        if len(message) == 0:
            await self.bot.say("Usage: sub r/<subreddit name>")
        elif len(message) > 1:
            await self.bot.say("Too many parameters.")
        elif message[0].startswith("r/") or message[0].startswith("/r/"):
            subreddit = message[0][message[0].rindex("/")+1:].strip()
            await self.execute_request(subreddit)
        else:
            await self.bot.say("Invalid syntax. Usage: sub r/<subreddit name>")

    async def execute_request(self, subreddit):
        """download subreddit top results, pick a random post, display url to channel"""
        # download top reddit images for a given subreddit
        reddit_results = await self.fetch(subreddit)
        reddit_results = reddit_results['data']['children']

        # if no posts are found, exit
        if len(reddit_results) == 0:
            await self.bot.say("No results found.")

        # randomly pick a post from the above results
        post = self.get_random_post(reddit_results)

        if post is None:
            # if no images were found in the results, exit
            await self.bot.say("No image results found.")
        else:
            # this is where the bot replies with what she found
            await self.bot.say(post)

    async def fetch(self, subreddit):
        """connect to reddit and download the top posts of all time for that subreddit (limit 25)"""
        header = {'User-Agent': 'trying to learn this async thing'}
        url = "https://www.reddit.com/r/{0}/top/.json?sort=top&t=all".format(subreddit)

        with aiohttp.Timeout(10):
            async with self.session.get(url, headers=header) as response:
                return await response.json()

    @staticmethod
    def get_random_post(reddit_results: list):
        """pick a random post from the results, ensure that post is an image and is SFW,
        return None if no images found"""
        picture_list = []

        for item in reddit_results:
            if "imgur" in item['data']['url'] and not item['data']['over_18']:
                picture_list.append(item['data']['url'])

        try:
            return random.choice(picture_list)
        except IndexError:
            return None


def setup(bot):
    """Adds this bot to the cog list."""
    bot.add_cog(RedditPics(bot))
