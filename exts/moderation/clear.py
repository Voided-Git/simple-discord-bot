from discord.commands import slash_command, Option
from discord.ext import commands
from sdb_lib import Config, Messages, success_embed, error_embed


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name = "clear",
        description = "Clears a number of messages",
        guild_ids = Config.guild_ids
    )
    @commands.has_permissions(manage_messages = True)
    @commands.bot_has_permissions(manage_messages = True)
    async def clear(
        self, ctx,
        amount: Option(int, "messages", min_value = 1)
    ):
        if amount <= 0:
            return await ctx.respond(embed = error_embed(Messages.clear_invalid_argument.replace("{}", str(amount))))

        try:
            await ctx.channel.purge(limit = amount)
            await ctx.respond(embed = success_embed(Messages.clear_success.replace("{}", str(amount))))
        except Exception:
            await ctx.respond(embed = error_embed(Messages.clear_fail))

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond(embed = error_embed(Messages.missing_permissions.replace("{}", "`MANAGE_MESSAGES`")))

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.respond(embed = error_embed(Messages.bot_missing_permissions.replace("{}", "`MANAGE_MESSAGES`")))


def setup(bot):
    bot.add_cog(Clear(bot))
