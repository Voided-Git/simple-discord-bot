from discord import Embed, Color
from .json_info import Config


def info_embed(text: str):
    return Embed(color = Color.random(), description = text)


def success_embed(text: str):
    return Embed(color = Color.random(), description = f"{Config.tick} {text}")


def error_embed(text: str):
    return Embed(color = 0xa10000, description = f"{Config.cross} {text}")


def is_int(value: str):
    try:
        int(value)
        return True
    except ValueError:
        return False


def parse_time(time: str):
    if is_int(time):
        return int(time)
    if not is_int(time[:-1]):
        return None

    _time = time[-1:].lower()
    time = int(time[:-1])

    if _time == "s":
        return time
    elif _time == "m":
        return time * 60
    elif _time == "h":
        return time * 3600
    elif _time == "d":
        return time * 21600
    elif _time == "w":
        return time * 151200
    elif _time == "y":
        return time * 7884000
