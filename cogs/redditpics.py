__author__ = 'pico'

from discord.ext import commands
import requests
import random

# reddit pics cog
class RedditPics:

    def __init__(self, bot):
        self.bot = bot
        self.is_nsfw = False

    @commands.command(hidden=True)
    async def sub(self, *message):
        if len(message) == 0:
            await self.bot.say("Usage: sub r/<subreddit name>")
            return
        elif len(message) > 1:
            await self.bot.say("Too many parameters.")
            return
        elif message[0].startswith("r/") or message[0].startswith("/r/"):
            subreddit = message[0][message[0].rindex("/")+1:].strip()
            await self.execute_request(subreddit)
            return
        else:
            await self.bot.say("Invalid syntax.")
            return

    async def execute_request(self, subreddit):

        # download top reddit images for a given subreddit
        reddit_results = self.get_reddit_top(subreddit)

        # randomly pick a post from the above results
        post = self.get_random_post(reddit_results)

        # if no posts are found, exit
        if len(reddit_results) == 0:
            await self.bot.say("No results found.")
            return

        # if no images were found in the results, exit
        if post == None:
            await self.bot.say("No image results found.")
            return

        # check for NSFW content, exit the search if found
        self.is_nsfw = post['data']['over_18']
        if self.is_nsfw:
            await self.bot.say("NSFW content found, exiting.")
            return

        # this is where the bot replies with what she found
        await self.bot.say(post['data']['url'])


    # connect to reddit and download the top posts of all time for that subreddit (limit 25)
    def get_reddit_top(self, subreddit):
        url = "https://www.reddit.com/r/{0}/top/.json?sort=top&t=all".format(subreddit)
        client = requests.session()
        client.get(url)
        header = { 'User-Agent' : 'trying to learn this async thing' }
        reddit_reply = client.get(url, headers=header)

        return reddit_reply.json()['data']['children']

    # pick a random post from the results, ensure that post is an image
    # if not an image, cycle through the posts
    def get_random_post(self, reddit_results: list):
        # randomize a list of numbers the length of the reddit results download
        # used to randomly cycle through the results
        iteration = random.sample(range(0, len(reddit_results)), len(reddit_results))

        while len(iteration) is not 0:
            result = reddit_results[iteration.pop()]
            if "imgur" not in result['data']['url']:
                continue
            else:
                return result
        self.bot.say("Could not retrieve any picture from the results.")
        return None

def setup(bot):
    bot.add_cog(RedditPics(bot))

