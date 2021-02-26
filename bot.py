import discord
from discord.ext.commands import Bot
from discord.ext import commands
from huachiapi import Huachiapi
import random


bot = Bot(command_prefix='!')
token = 'your-token'

api = Huachiapi()


AF_DET= './txt/afecto_detonador.txt'
AF_RESP = './txt/afecto_respuesta.txt'
RESP_DEF = './txt/respuestas_por_defecto.txt'


def load_file(file):
    """Load the log file and creates it if it doesn't exist.

     Parameters
    ----------
    file : str
        The file to write down
    Returns
    -------
    list
        A list of urls.

    """

    try:
        with open(file, 'r', encoding='utf-8') as temp_file:
            return temp_file.read().splitlines()
    except Exception:

        with open(LOG_FILE, 'w', encoding='utf-8') as temp_file:
            return []

_af_det = load_file(AF_DET)
_af_resp = load_file(AF_RESP)
_def_resp = load_file(RESP_DEF)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="en la otra caja le atienden"))


@bot.command(name='server',pass_context=True)
@commands.has_permissions(administrator=True)
async def fetchServerInfo(context):
    guild = context.guild

    await context.send(f'Server Name: {guild.name}')
    await context.send(f'Server Size: {len(guild.members)}')
    await context.send(f'Server Name: {guild.owner.display_name}')


@bot.command(name='saldazo')
async def fetchServerInfo(context):
    response = api.saldazo(None)
    await context.send(response)


@bot.command(name='shop')
async def fetchServerInfo(context):
    response = api.shop(None)
    await context.send(response)

@bot.command(name='tip')
async def fetchServerInfo(context):
    response = api.tip(None)
    await context.send(response)


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    # we do not want the bot to reply to itself
    if message.author.id == bot.user.id:
        return

    print(message.content)

    if bot.user.mentioned_in(message):
        if any(map(message.content.lower().__contains__, _af_det)):
            resp = random.choice(_af_resp)
            await message.channel.send(resp)
        else:
            resp = random.choice(_def_resp)
            await message.channel.send(resp)

bot.run(token)
