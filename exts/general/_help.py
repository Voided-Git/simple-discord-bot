from discord import Embed, Color
from discord.commands import slash_command
from discord.ext import commands
from sdb_lib import Config, Log, info_embed, Messages


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name = "help",
        description = "View all commands available",
        guild_ids = Config.guild_ids
    )
    async def _help(self, ctx):
        await ctx.respond(embed = info_embed(Messages.help_message))

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            Log.error(error.original)


def setup(bot):
    bot.add_cog(Help(bot))
