from discord import Embed, Color
from discord.commands import slash_command
from discord.ext import commands
from sdb_lib import Config, info_embed


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name = "ping",
        description = "Shows the bot's current ping",
        guild_ids = Config.guild_ids
    )
    async def ping(self, ctx):
        await ctx.respond(embed = info_embed(f"📶 Ping: `{round(self.bot.latency * 1000)}`ms"))


def setup(bot):
    bot.add_cog(Ping(bot))
