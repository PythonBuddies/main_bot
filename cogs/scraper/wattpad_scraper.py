"""Wattpad scraper cog.

Many features to scrape from wattpad.
"""
from discord.ext import commands
from .scraper_utils import GeneralScraper

# API_STORYINFO = 'https://www.wattpad.com/api/v3/stories/'
# API_HOTSTORYLIST = 'https://www.wattpad.com/api/v3/stories?filter=hot'
API_NEWSTORYLIST = 'https://www.wattpad.com/api/v3/stories?filter=new'
# API_STORYTEXT = 'https://www.wattpad.com/apiv2/storytext'
# API_GETCATEGORIES = 'https://www.wattpad.com/apiv2/getcategories'
# API_CHAPTERINFO = 'https://www.wattpad.com/apiv2/info'


class WattpadScraper(GeneralScraper):
    """Wattpad scraper cog."""

    def __init__(self, bot):
        """Initalization function."""
        super().__init__()
        self.bot = bot

    @commands.group(name='wattpad', pass_context=True)
    async def _wattpad(self, ctx):
        """Useful commands for getting stories from Wattpad."""
        if ctx.invoked_subcommand is None:
            await self.bot.pm_help(ctx)

    @_wattpad.command()
    async def latest(self):
        """Get the latest story posted to Wattpad."""
        result = await self.get_latest_story()
        await self.bot.say(result)

    async def get_latest_story(self, session=None):
        story_json = await self.fetch_json(
            API_NEWSTORYLIST, session=session, headers={"User-Agent": "Chrome/41.0.2228.0"})
        first_story = story_json['stories'][0]
        story_title = first_story['title']
        story_description = first_story['description']
        story_chapter_one_url = first_story['parts'][0]['url']

        return ("**Title:** {}\n"
                "**Description:** {}\n"
                "**Link:** {}"
                .format(story_title,
                        story_description,
                        story_chapter_one_url))


def setup(bot):
    """Called when cog is loaded via load_extension()."""
    bot.add_cog(WattpadScraper(bot))
