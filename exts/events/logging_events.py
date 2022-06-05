from discord import Embed, Color, Message, Member
from discord.ext import commands
from discord.utils import get
from sdb_lib import load_json


def get_logging_channel(obj: any):
    return get(obj.guild.channels, id = load_json("./data.json")["logging"]["channel"])


class LoggingEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member: Member):
        embed = Embed(
            color = Color.green(),
            title = member,
            description = f"Member joined, {member.mention}"
        )
        embed.add_field(
            name = "Account created",
            value = member.created_at.utcnow()
        )
        embed.add_field(
            name = "Joined at",
            value = member.joined_at.utcnow()
        )
        embed.set_thumbnail(url = member.avatar)

        await get_logging_channel(member).send(embed = embed)

    @commands.Cog.listener("on_member_remove")
    async def on_member_remove(self, member: Member):
        embed = Embed(
            color = Color.red(),
            title = member,
            description = "Member left"
        )
        embed.set_thumbnail(url = member.avatar)

        await get_logging_channel(member).send(embed = embed)

    @commands.Cog.listener("on_member_update")
    async def on_member_update(self, before: Member, after: Member):
        channel = get_logging_channel(before)

        embed = Embed(
            color = Color.blue()
        )
        embed.set_author(
            name = before,
            icon_url = before.avatar
        )

        if before.nick != after.nick:
            embed.description = f"Nickname changed:\n```diff\n- {before.nick}\n+ {after.nick}\n```".replace("None", before.name)
            return await channel.send(embed = embed)

        elif before.roles != after.roles:
            if len(before.roles) > len(after.roles):
                for role in before.roles:
                    if role not in after.roles:
                        embed.color = Color.red()
                        embed.description = f"Role removed, {role.mention}"
                        break

            else:
                for role in after.roles:
                    if role not in before.roles:
                        embed.color = Color.green()
                        embed.description = f"Role added, {role.mention}"
                        break

            return await channel.send(embed = embed)

    @commands.Cog.listener("on_message_edit")
    async def on_message_edit(self, before: Message, after: Message):
        if before.author.bot or before.content == after.content:
            return

        embed = Embed(
            color = Color.blue(),
            description = f"Message edited [here](https://discord.com/{before.guild.id}/{before.channel.id}/{before.id}):\n```diff\n- {before.content}\n+ {after.content}\n```"
        )
        embed.set_author(
            name = before.author,
            icon_url = before.author.avatar
        )
        await get_logging_channel(before).send(embed = embed)

    @commands.Cog.listener("on_message_delete")
    async def on_message_delete(self, message: Message):
        if message.author.bot:
            return

        embed = Embed(
            color = Color.red(),
            description = f"Message deleted in {message.channel.mention}:\n```diff\n- {message.content}\n```"
        )
        embed.set_author(
            name = message.author,
            icon_url = message.author.avatar
        )
        await get_logging_channel(message).send(embed = embed)


def setup(bot):
    bot.add_cog(LoggingEvents(bot))
