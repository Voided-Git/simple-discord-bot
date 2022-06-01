from discord import Embed, Color, TextChannel
from discord.commands import slash_command, Option
from discord.ext import commands
from sdb_lib import Config, error_embed, success_embed, Messages, load_json
from json import dump


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name = "logging_setup",
        description = "setup logging",
        guild_ids = Config.guild_ids
    )
    async def logging_setup(
        self, ctx,
        channel: Option(TextChannel, "channel")
    ):
        if ctx.author.id not in Config.developer_ids:
            return await ctx.respond(embed = error_embed(Messages.not_developer), ephemeral = True)

        logging_json = load_json("./logging.json")
        logging_json["channel"] = channel.id

        with open("./logging.json", "r") as f:
            dump(logging_json, f, indent = 4)

        await ctx.respond(embed = success_embed(Messages.logging_success), ephemeral = True)


def setup(bot):
    bot.add_cog(Logging(bot))
