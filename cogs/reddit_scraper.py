from discord.ext import commands

from .utils import checks, scraper, wattpadscraper

class RedditScraper:

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name='reddit', pass_context=True)
    @checks.is_owner()
    async def _reddit(self, ctx):
        """Useful commands for getting information from reddit."""
        if ctx.invoked_subcommand is None:
            await self.bot.pm_help(ctx)

    @_reddit.command(pass_context=True, name='get')
    async def get(self, ctx: commands.Context, subreddit, posts=5, category='hot'):
        """Base command for returning data from a subreddit.

        Keyword arguments:
        posts -- Number of posts to return (default 5)
        category -- Category to look at [hot, new, rising, controversial, top] (default hot)
        """
        if posts > 25:
            await self.bot.say('Number of posts must be no greater than 25.')
            return
        if subreddit.strip():
            if category in scraper.categories:
                result = await scraper.get_subreddit_top(self.bot.session, subreddit, posts, category)
                await self.bot.say('\n\n'.join(result))
            else:
                await self.bot.say('Category must be valid: ' + ', '.join(scraper.categories))
        else:
            await self.bot.pm_help(ctx)
class WattpadScraper:
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.group(name ='wattpad',pass_context = True)
    @checks.is_owner()
    async def _wattpad(self,ctx):

    @_wattpad.command(pass_context=True,name = 'fetch')
    async def fetch(self, ctx: commands.Context):
        result = await wattpadscraper.get_random_story_info(self.bot.session)
        await self.bot.say(result)

def setup(bot):
    bot.add_cog(RedditScraper(bot))
    bot.add_cog(WattpadScraper(bot))

