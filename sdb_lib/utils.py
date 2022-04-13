from discord import Embed, Color


def info_embed(text: str):
    return Embed(color = Color.random(), description = text)
