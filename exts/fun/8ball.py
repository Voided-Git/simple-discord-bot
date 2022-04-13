from discord.commands import slash_command, Option
from discord.ext import commands
from sdb_lib import Config, info_embed, Messages
from random import choice


class _8Ball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name = "8ball",
        description = "Asks the infamous 8 ball a question",
        guild_ids = Config.guild_ids
    )
    async def _8ball(
        self, ctx,
        question: Option(str, "question")
    ):
        if not question.endswith("?"):
            question += "?"

        await ctx.respond(embed = info_embed(f"{question.capitalize()}\n{choice(Messages._8ball_responses)}"))


def setup(bot):
    bot.add_cog(_8Ball(bot))
