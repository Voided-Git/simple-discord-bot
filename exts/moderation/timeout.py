from discord import Member
from discord.commands import slash_command, Option
from discord.ext import commands
from sdb_lib import Config, success_embed, error_embed, Messages, parse_time, Log
from datetime import timedelta, datetime


class Timeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name = "timeout",
        description = "Times out a member of the server",
        guild_ids = Config.guild_ids
    )
    @commands.has_permissions(moderate_members = True)
    @commands.bot_has_permissions(moderate_members = True)
    async def timeout(
        self, ctx,
        member: Option(Member, "member"),
        duration: Option(str, "duration"),
        reason: Option(str, "reason", required = False)
    ):
        _duration = parse_time(duration)
        if not _duration:
            return await ctx.respond(embed = error_embed(Messages.timeout_error.replace("{}", duration)))

        try:
            await member.timeout_for(duration = timedelta(seconds = _duration), reason = reason)
            await ctx.respond(embed = success_embed(Messages.timeout_success.replace("{}", member.mention)))
        except Exception as exc:
            Log.error(exc)
            await ctx.respond(embed = error_embed(Messages.timeout_fail.replace("{}", member.mention)))

    @timeout.error
    async def timeout_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond(embed = error_embed(Messages.missing_permissions.replace("{}", "`MODERATE_MEMBERS`")))

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.respond(embed = error_embed(Messages.bot_missing_permissions.replace("{}", "`MODERATE_MEMBERS`")))


def setup(bot):
    bot.add_cog(Timeout(bot))
