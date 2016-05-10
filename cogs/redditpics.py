__author__ = 'pico'

from discord.ext import commands
import requests, random, json, asyncio

# reddit pics cog
class RedditPics:

    def __init__(self, bot):
        self.bot = bot
        self.post = None
        self.random_post = None
        self.is_nsfw = False

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

            post = self.parse_results(subreddit)
            print(post)
            print(post['data']['over_18'])
            self.is_nsfw = post['data']['over_18']
            while self.is_nsfw:
                print("nsfw found")
                post = self.parse_results(subreddit)
                self.is_nsfw = post['data']['over_18']

            # reddit_results = self.get_reddit_top(subreddit)
            # print(len(reddit_results))
            #
            # random_post = self.get_random_post(reddit_results)
            #
            # post = random_post['data']['url']
            #
            # print(post)
            await self.bot.say(post['data']['url'])
            return
        else:
            await self.bot.say("Invalid syntax.")
            return

    def parse_results(self, subreddit: str):
        reddit_results = self.get_reddit_top(subreddit)

        print(len(reddit_results))

        post = self.get_random_post(reddit_results)

        #post = random_post['data']['url']

        return post

    def get_reddit_top(self, subreddit):
        url = "https://www.reddit.com/r/{0}/top/.json?sort=top&t=all".format(subreddit)
        client = requests.session()
        client.get(url)
        header = { 'User-Agent' : 'trying to learn this async thing' }
        reddit_reply = client.get(url, headers=header)
        return reddit_reply.json()['data']['children']

    # not working yet, returns a random post
    def get_random_post(self,random_post: list):
        return random.choice(random_post)






    async def receive_message(self, message):
        if message.author.id == self.bot.user.id:
            return

def setup(bot):
    redditpics = RedditPics(bot)
    bot.add_listener(redditpics.receive_message, "on_message")
    bot.add_cog(RedditPics(bot))

