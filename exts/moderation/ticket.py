from discord import Embed, Color, CategoryChannel, Role
from discord.commands import slash_command, Option
from discord.ext import commands
from discord.utils import get
from sdb_lib import Config, Messages, info_embed, success_embed, error_embed, load_json
from json import dump
from asyncio import sleep


def format_number(number: str):
    if len(number) == 3:
        return f"0{number}"
    elif len(number) == 2:
        return f"00{number}"
    elif len(number) == 1:
        return f"000{number}"
    return number


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name = "ticket",
        description = "Ticketing",
        guild_ids = Config.guild_ids
    )
    @commands.bot_has_permissions(manage_channels = True)
    async def ticket(
        self, ctx,
        option: Option(str, "option", choices = ["new", "delete"])
    ):
        try:
            tickets = load_json("./tickets.json")
        except FileNotFoundError:
            with open("./tickets.json", "w+") as f:
                f.write({
                    "number": 0,
                    "category": None,
                    "support": None,
                    "tickets": []
                })

        if option == "new":
            for i in tickets["tickets"]:
                if ctx.author.id == i["user_id"]:
                    return await ctx.respond(embed = error_embed(Messages.ticket_create_fail))

            tickets["number"] += 1
            ticket = format_number(str(tickets["number"]))
            channel = await ctx.guild.create_text_channel(f"ticket-{ticket}", category = get(ctx.guild.categories, id = tickets["category"]))

            await channel.set_permissions(
                get(ctx.guild.roles, name = "@everyone"),
                view_channel = False
            )
            await channel.set_permissions(
                get(ctx.guild.roles, id = tickets["support"]),
                view_channel = True,
                send_messages = True,
                read_message_history = True
            )
            await channel.set_permissions(
                ctx.author,
                view_channel = True,
                send_messages = True,
                read_message_history = True
            )

            await ctx.respond(embed = info_embed(Messages.ticket_create_success.replace("{}", channel.mention)), ephemeral = True)

            await channel.send("@everyone")
            await channel.send(embed = Embed(
                color = Color.random(),
                title = channel.name.capitalize(),
                description = Messages.ticket_message
            ))

            with open("./tickets.json", "w") as f:
                tickets["tickets"].append({
                    "user_id": ctx.author.id,
                    "channel_id": channel.id
                })
                dump(tickets, f, indent = 4)

        elif option == "delete":
            t = True

            for i in tickets["tickets"]:
                if ctx.author.id == i["user_id"]:
                    t = tickets["tickets"].index(i)

            if t:
                return await ctx.respond(embed = error_embed(Messages.ticket_delete_fail), ephemeral = True)

            channel = get(ctx.guild.channels, id = tickets["tickets"][t]["channel_id"])

            await ctx.respond(embed = success_embed(Messages.ticket_delete_success), ephemeral = True)
            await sleep(5)

            if channel:
                await channel.delete()

            with open("./tickets.json", "w") as f:
                tickets["tickets"].pop(t)
                dump(tickets, f, indent = 4)

    @slash_command(
        name = "tickets_setup",
        description = "Setting up ticketing",
        guild_ids = Config.guild_ids
    )
    async def ticket_setup(
        self, ctx,
        category: Option(CategoryChannel, "category"),
        support: Option(Role, "support role")
    ):
        if ctx.author.id not in Config.developer_ids:
            return await ctx.respond(embed = error_embed(Messages.not_developer), ephemeral = True)

        tickets = load_json("./tickets.json")
        tickets["category"] = category.id
        tickets["support"] = support.id

        with open("./tickets.json", "w") as f:
            dump(tickets, f, indent = 4)

        await ctx.respond(embed = success_embed(Messages.tickets_success), ephemeral = True)

    @ticket.error
    async def ticket_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.respond(embed = error_embed(Messages.bot_missing_permissions.replace("{}", "`MANAGE_CHANNELS`")), ephemeral = True)


def setup(bot):
    bot.add_cog(Ticket(bot))
