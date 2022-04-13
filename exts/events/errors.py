from discord.ext import commands
from sdb_lib import error_embed, Messages


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond(embed = error_embed(Messages.missing_permissions))

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.respond(embed = error_embed(Messages.bot_missing_permissions))

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond(embed = error_embed(Messages.missing_argument))

        elif isinstance(error, commands.CommandError):
            await ctx.respond(embed = error_embed(Messages.command_error))


def setup(bot):
    bot.add_cog(Errors(bot))
