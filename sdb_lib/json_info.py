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
