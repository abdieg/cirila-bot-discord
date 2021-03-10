import cogs.libs.Settings as ST
import cogs.libs.Utils as UT
import discord
import asyncio
import platform
from discord.ext import commands

BOT = ST.BOT

startup_ext = [
	"cogs.messages",
    "cogs.management"
]

@BOT.event
async def on_ready():
    print("\nLogged in as " + BOT.user.name + " with ID: " + str(BOT.user.id))
    print("Connected to " + str(len(BOT.guilds)) + " servers and " + str(len(set(BOT.get_all_members()))) + " users")
    print("Current Discord.py Version: {} | Current Python Version: {}".format(discord.__version__, platform.python_version()))
    print("Invite {}:".format(BOT.user.name))
    print("https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=3200".format(BOT.user.id))
    print("Bot Cirila ideado originalmente por Agent Type: None y modificado con COGS por Abdieg.")

    for extension in startup_ext:
        try:
            BOT.load_extension(extension)
            print("\n>>>Extension loaded: {}".format(extension))
        except Exception as e:
            print(">>>Failed to load extension: {}\n{}".format(extension, e))

    juego = discord.Game(name="Autsilio | $help")
    await BOT.change_presence(status=discord.Status.online, activity=juego)

@BOT.command(hidden=True)
@commands.check(UT.is_owner)
async def load(ctx, extension_name : str):
    """Loads an extension."""
    try:
        BOT.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} loaded.".format(extension_name))

@BOT.command(hidden=True)
@commands.check(UT.is_owner)
async def unload(ctx, extension_name : str):
    """Unloads an extension."""
    BOT.unload_extension(extension_name)
    await ctx.send("{} unloaded.".format(extension_name))

@BOT.command(hidden=True)
@commands.check(UT.is_owner)
async def reload(ctx, extension_name : str = None):
    """Reloads and extension given the name. If no name is given, then all extensions are reloaded"""
    if extension_name is None:
        for i in startup_ext:
            try:
                BOT.unload_extension(i)
                BOT.load_extension(i)
            except Exception as e:
                print("Failed to load extension: {}\n{}".format(e))
                await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        await ctx.send("Extensions reloaded")
        return
    try:
        BOT.unload_extension(extension_name)
        BOT.load_extension(extension_name)
        await ctx.send("{} reloaded.".format(extension_name))
    except Exception as e:
        print("Failed to load extension: {}\n{}".format(e))
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))

@BOT.command(hidden=True)
@commands.check(UT.is_owner)
async def loaded(ctx):
    """List loaded cogs"""
    string = ""
    for cog in startup_ext:
        string += str(cog) + "\n"
    await ctx.send("Currently loaded extensions:\n```{}```".format(string))

@BOT.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("El comando podrá ser reutilizado en %.2f segundos" % error.retry_after)
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Permisos insuficientes")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Argumento de comando inválido")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Falta argumento para el comando")
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Error inesperado en el comando")
    if isinstance(error, commands.ExtensionNotLoaded):
        await ctx.send("Error al cargar extensión")
    if isinstance(error, commands.ExtensionNotFound):
        await ctx.send("Extensión inválida")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando no encontrado. Para mostrar la lista de comandos disponibles use " + UT.bold("$ayuda"))
    raise error  #No borrar, para que todos los errores sigan siendo mostrados en consola

# BOT.remove_command("help") #Area de oportunidad, pendiente
BOT.run(ST.TOKEN, bot=True, reconnect=True)