from discord import Member
from discord.commands import slash_command, Option
from discord.ext import commands
from sdb_lib import Config, error_embed, success_embed, Messages


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name = "ban",
        description = "Bans a member from the server",
        guild_ids = Config.guild_ids
    )
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def ban(
        self, ctx,
        member: Option(Member, "member"),
        reason: Option(str, "reason", required = False)
    ):
        try:
            await member.ban(reason = reason)
            await ctx.respond(embed = success_embed(Messages.ban_success.replace("{}", member.name)))
        except Exception:
            await ctx.respond(embed = error_embed(Messages.ban_fail.replace("{}", member.mention)))

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond(embed = error_embed(Messages.missing_permissions.replace("{}", "`BAN_MEMBERS`")))

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.respond(embed = error_embed(Messages.bot_missing_permissions.replace("{}", "`BAN_MEMBERS`")))


def setup(bot):
    bot.add_cog(Ban(bot))
