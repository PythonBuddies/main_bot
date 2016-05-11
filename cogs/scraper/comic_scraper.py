"""Comic scraper cog.

Contains comic, comic random, and comic latest commands - the latter
two choose a random command from sub-group-commands of comic to execute.

"""
import re
import random
from discord.ext import commands
from .scraper_utils import GeneralScraper


class ComicScraper(GeneralScraper):
    """Main base comic cog.

    Extends GeneralScraper.
    Contains the comic, comic latest, and comic random commands.

    """

    def __init__(self, bot):
        """Initalization method."""
        super().__init__()
        self.bot = bot
        self.latest_commands = []
        self.random_commands = []
        self.current_comic = 0

        self.latest_commands.append(self.commitstrip_latest)
        self.random_commands.append(self.commitstrip_random)

        self.latest_commands.append(self.cubedrone_latest)
        self.random_commands.append(self.cubedrone_random)

    @commands.group(pass_context=True)
    async def comic(self, ctx):
        """Main comic command."""
        if ctx.invoked_subcommand is None:
            await ctx.bot.pm_help(ctx)

    @comic.command(name="random", pass_context=True)
    async def comic_random(self, ctx):
        """Return random comic from a random comic website."""
        await random.choice(self.random_commands).invoke(ctx)

    @comic.command(name="latest", pass_context=True)
    async def comic_latest(self, ctx):
        """Return the latest comic from the next comic website."""
        await self.latest_commands[self.current_comic].invoke(ctx)
        self.current_comic = self.current_comic + 1 if self.current_comic != len(self.latest_commands)-1 else 0


#   Begin CommitStrip Section

    @comic.group(pass_context=True)
    async def commitstrip(self, ctx):
        """Main CommitStrip command."""
        if ctx.invoked_subcommand is None:
            await self.bot.pm_help(ctx)

    @commitstrip.command(name="random")
    async def commitstrip_random(self):
        """Return a random CommitStrip comic."""
        # Get the last page number
        message = await self.bot.say("Loading...")
        index_html = (await self.fetch_page("http://www.commitstrip.com/")).decode("utf-8")
        last_page_number = int(index_html.split('<a class="last" href="')[1].split('"')[0].split("/")[5].split("/")[0])

        # Get the HTML of a random page between 1 and last page number
        random_page_url = "http://www.commitstrip.com/en/page/{}".format(random.randint(1, last_page_number))
        random_page = (await self.fetch_page(random_page_url)).decode("utf-8")
        comic_list_html = [comic_raw.split("</div>")[0] for comic_raw in random_page.split('<div class="excerpt">')]

        # Get rid of all non-comic code before first '<div class="excerpt">'
        comic_list_html.pop(0)

        # Get the title and image of random comic.
        comic_url = random.choice(comic_list_html).split('<a href="')[1].split('"')[0]
        comic = (await self.commitstrip_comic_from_url(comic_url))
        await self.bot.edit_message(message, "**Title**: `{}`\n"
                                             "**Image**: {}".format(comic[0],
                                                                    comic[1]))

    @commitstrip.command(name="latest")
    async def commitstrip_latest(self):
        """Return the latest CommitStrip comic."""
        message = await self.bot.say("Loading...")
        index_html = (await self.fetch_page("http://www.commitstrip.com/")).decode("utf-8")
        url_http = index_html.split('<div class="excerpt">')[1].split('<a href="')[1].split('"')[0]
        comic = (await self.commitstrip_comic_from_url(url_http))
        await self.bot.edit_message(message, "**Title**: `{}`\n"
                                             "**Image**: {}".format(comic[0],
                                                                    comic[1]))

    async def commitstrip_comic_from_url(self, comic_url):
        """Return comic title and comic image url from comic page url.

        Keyword Arguments:
        comic_url -- URL of comic page.

        Returns:
        list -- 0 -- str -- Title of comic.
                1 -- str -- URL of the comic image.

        """
        comic_html = (await self.fetch_page(comic_url)).decode("utf-8")
        # 'src' is not always the first attribute after the opening img tag.
        comic_image = comic_html.split('<div class="entry-content">')[1]
        comic_image = comic_image.split("<img ")[1].split('src="')[1].split('"')[0]
        comic_title = comic_html.split('<h1 class="entry-title">')[1].split("</h1>")[0]
        return [parse_html_entities(comic_title), comic_image]

#   End CommitStrip Section
#   Begin CubeDrone Section

    @comic.group(pass_context=True)
    async def cubedrone(self, ctx):
        """Main CubeDrone command."""
        if ctx.invoked_subcommand is None:
            await self.bot.pm_help(ctx)


    @cubedrone.command(name="random")
    async def cubedrone_random(self):
        """Return a random CubeDrone comic."""
        # Get the last page number
        message = await self.bot.say("Loading...")
        index_html = (await self.fetch_page("https://cube-drone.com/")).decode("utf-8")
        total_comics = int(index_html.split("<div class='order bg-primary'>")[1].split("</div>")[0])
        comic_url = "https://cube-drone.com/comics/n/{}".format(random.randint(1, total_comics))
        comic = (await self.cubedrone_comic_from_url(comic_url))
        await self.bot.edit_message(message, "**Title**: `{}`\n"
                                             "**Image**: {}".format(comic[0],
                                                                    comic[1]))

    @cubedrone.command(name="latest")
    async def cubedrone_latest(self):
        """Return the latest CubeDrone comic."""
        message = await self.bot.say("Loading...")
        comic = (await self.cubedrone_comic_from_url("https://cube-drone.com/"))
        await self.bot.edit_message(message, "**Title**: `{}`\n"
                                             "**Image**: {}".format(comic[0],
                                                                    comic[1]))


    async def cubedrone_comic_from_url(self, comic_url):
        """Return comic title and comic image url from comic page url.

        Keyword Arguments:
        comic_url -- URL of comic page.

        Returns:
        list -- 0 -- str -- Title of comic.
                1 -- str -- URL of the comic image.

        """
        comic_html = (await self.fetch_page(comic_url)).decode("utf-8")
        comic_image = comic_html.split("<img class='comic img-responsive' src='")[1].split("'")[0]
        comic_title = comic_html.split("<h2 class='comic_title'>")[1].split("<small>")[0]
        return [parse_html_entities(comic_title), comic_image]

#   End CubeDrone Section

def parse_html_entities(string):
    """Replace ASCII character codes with the actual characters.

    Keyword Arguments:
    string -- String with ASCII codes within it.

    Returns:
    str -- 'string' with ASCII codes replaced with characters.

    Note: May be moved into a utility file if there is another
    time it is needed. Maybe into the GeneralScraper class.

    """
    for hit in re.findall("&#\\d+;", string):
        try:
            string = string.replace(hit, chr(int(hit[2:-1])))
        except ValueError:
            pass
    return string


def setup(bot):
    """Called when cog is loaded via load_extension()."""
    bot.add_cog(ComicScraper(bot))
