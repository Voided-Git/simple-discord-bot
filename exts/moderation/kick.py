from discord import Member
from discord.commands import slash_command, Option
from discord.ext import commands
from sdb_lib import Config, error_embed, success_embed, Messages


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name = "kick",
        description = "Kicks a member from the server",
        guild_ids = Config.guild_ids
    )
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(kick_members = True)
    async def kick(
        self, ctx,
        member: Option(Member, "member"),
        reason: Option(str, "reason", required = False)
    ):
        try:
            await member.kick(reason = reason)
            await ctx.respond(embed = success_embed(Messages.kick_success.replace("{}", member.name)))
        except Exception:
            await ctx.respond(embed = error_embed(Messages.kick_fail.replace("{}", member.mention)))


def setup(bot):
    bot.add_cog(Kick(bot))
