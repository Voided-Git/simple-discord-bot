from json import load


def load_json(filename: str):
    return load(open(filename, "r"))


class Config:
    config = load_json("./config.json")

    token = config["token"]

    prefix = config["prefix"]

    guild_ids = config["guild_ids"]

    tick = config["emotes"]["tick"]
    cross = config["emotes"]["cross"]
    loading = config["emotes"]["loading"]


class Messages:
    messages = load_json("./config.json")["messages"]

    missing_permissions = messages["events"]["error.missing_permissions"]
    bot_missing_permissions = messages["events"]["error.bot_missing_permissions"]
    missing_argument = messages["events"]["error.missing_argument"]
    command_error = messages["events"]["error.command_error"]

    help_message = messages["general"]["help.message"]
    ping_message = messages["general"]["ping.message"]

    ban_fail = messages["moderation"]["ban.fail"]
    ban_success = messages["moderation"]["ban.success"]
    clear_fail = messages["moderation"]["clear.fail"]
    clear_success = messages["moderation"]["clear.success"]
    kick_fail = messages["moderation"]["kick.fail"]
    kick_success = messages["moderation"]["kick.success"]
