from datetime import datetime
from discord.ext import commands
from .scraper_utils import GeneralScraper


class RedditScraper(GeneralScraper):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        #self.categories = ['hot', 'new', 'controversial', 'rising', 'top']
        self.bot = bot

    @commands.group(name='reddit', pass_context=True)
    async def _reddit(self, ctx):
        """Useful commands for getting information from reddit."""
        if ctx.invoked_subcommand is None:
            await self.bot.pm_help(ctx)

    @_reddit.command(pass_context=True, name='get')
    async def get(self, ctx: commands.Context, subreddit, num_posts=5, category='hot'):
        """Base command for returning data from a subreddit.

        Keyword arguments:
        posts -- Number of posts to return (default 5)
        category -- Category to look at [hot, new, rising, controversial, top] (default hot)
        """
        if num_posts > 25:
            await self.bot.say('Number of posts must be no greater than 25.')
            return
        if subreddit.strip():
            if category in self.categories:
                result = await self.get_subreddit_top(
                    session=self.session, subreddit=subreddit, num_posts=num_posts, category=category)
                await self.bot.say('\n\n'.join(result))
            else:
                await self.bot.say('Valid categories are {}: '.format(', '.join(self.categories)))
        else:
            await self.bot.pm_help(ctx)

    async def get_post_from_json(self, post_data: dict):
        post = post_data['data']
        score = post['score']
        author = post['author']
        is_nsfw = post['over_18']
        link = post['url']
        title = post['title']

        timediff = datetime.now() - datetime.fromtimestamp(post['created_utc'])
        days = timediff.days
        hours = timediff.seconds // 3600
        minutes = (timediff.seconds // 60) % 60
        created = []

        if days != 0:
            if days > 1:
                created.append(str(days) + ' days')
            else:
                created.append(str(days) + ' day')
        if hours != 0:
            if hours > 1:
                created.append(str(hours) + ' hours')
            else:
                created.append(str(hours) + ' hour')
        if minutes != 0:
            if minutes > 1:
                created.append(str(minutes) + ' minutes')
            else:
                created.append(str(minutes) + ' minute')

        return '''
        **Title:** {0}
        **Link:** <{1}>
        **Author:** {2}
        **Created:** {3} ago
        **Score:** {4}
        **NSFW:** {5}
        '''.format(title, link, author, ' '.join(created), score, is_nsfw)

    async def get_posts(self, sr_posts, num):
        posts = []
        i = 0
        for post in sr_posts:
            if i >= num:
                break
            posts.append(await self.get_post_from_json(post))
            i += 1
        return posts

    async def get_subreddit_json(self, session, subreddit, category):
        return await self.fetch_json(
            session=session, url='https://www.reddit.com/r/' + subreddit + '/' + category + '/.json')

    async def get_subreddit_top(self, session, subreddit, num_posts, category):
        try:
            sr_data = await self.get_subreddit_json(session=session, subreddit=subreddit, category=category)
            sr_posts = sr_data['data']['children']
        except KeyError:
            return ['Posts could not be loaded, are you sure thats a subreddit?']
        return await self.get_posts(sr_posts, num_posts)


def setup(bot):
    bot.add_cog(RedditScraper(bot))
