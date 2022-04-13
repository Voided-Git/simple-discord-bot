from discord import Embed, Color
from .json_info import Config


def info_embed(text: str):
    return Embed(color = Color.random(), description = text)


def success_embed(text: str):
    return Embed(color = Color.random(), description = f"{Config.tick} {text}")


def error_embed(text: str):
    return Embed(color = 0xa10000, description = f"{Config.cross} {text}")
