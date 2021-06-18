import os
import random
from typing import Optional

from discord.ext import commands
from dotenv import load_dotenv

from game import Game

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!t')

game = Game()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='new', help="Start a new game")
async def new_game(ctx):
    await game.new_game(ctx)


@bot.command(name='p', help="place your token")
async def place_short(ctx: commands.Context, arg1: str, arg2: Optional[int]):
    await game.place(ctx, arg1, arg2)


@bot.command(name='place', help="place your token")
async def place(ctx: commands.Context,  arg1: str, arg2: Optional[int]):
    await game.place(ctx, arg1, arg2)


@place_short.error
async def place_short_error(ctx, error):
    await place_error(ctx, error)


@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Bad arguments')
        await ctx.send(error)
    else:
        await ctx.send('Command didn\'t work')
        await ctx.send(error)

bot.run(TOKEN)
