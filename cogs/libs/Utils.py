from . import Settings
import discord

def is_owner(ctx):
    return ctx.author.id == Settings.OWNER

def is_server_owner(ctx):
    return ctx.author.id == ctx.guild.owner

def italics(text):
    return "*{}*".format(text)

def bold(text):
    return "**{}**".format(text)

def underline_bold(text):
    return "_**{}**_".format(text)