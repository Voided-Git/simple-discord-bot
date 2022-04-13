from discord import Embed, Color
from discord.commands import slash_command, Option
from discord.ext import commands
from sdb_lib import Config, list_exts, error_embed, Messages


class Ext(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name = "ext",
        description = "Loads, unloads or reloads the specified extension(s)",
        guild_ids = Config.guild_ids
    )
    async def ext(
        self, ctx,
        option: Option(str, "load type", choices = ["load", "unload", "reload"]),
        exts: Option(str, "extensions", required = False)
    ):
        if ctx.author.id not in Config.developer_ids:
            return await ctx.respond(embed = error_embed(Messages.not_developer))

        if not exts:
            exts = list_exts()
        else:
            exts = exts.split(",")

        em = Embed(
            color = Color.random(),
            title = "",
            description = ""
        )

        if option.lower() == "load":
            em.title = "Loaded:"

            for ext in exts:
                try:
                    self.bot.load_extension(f"exts.{ext}")
                    em.description += f"\n• {ext}"
                except Exception as exc:
                    em.description += f"\n‣ {ext} failed: ```\n{exc}\n```"

        elif option.lower() == "unload":
            em.title = "Unloaded:"

            for ext in exts:
                try:
                    self.bot.unload_extension(f"exts.{ext}")
                    em.description += f"\n• {ext}"
                except Exception as exc:
                    em.description += f"\n‣ {ext} failed: ```\n{exc}\n```"

        elif option.lower() == "reload":
            em.title = "Reloaded:"

            for ext in exts:
                try:
                    self.bot.reload_extension(f"exts.{ext}")
                    em.description += f"\n• {ext}"
                except Exception as exc:
                    em.description += f"\n‣ {ext} failed: ```\n{exc}\n```"

        await ctx.respond(embed = em)


def setup(bot):
    bot.add_cog(Ext(bot))
