import os
import random
from typing import Optional

from discord import User
from discord.ext import commands
from dotenv import load_dotenv

from game import Game

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!!')

game = Game()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='n', help="Start a new game. Needs a second player")
async def new_game_short(ctx, player2: User):
    await game.new_game(ctx, ctx.author, player2, bot.user)


@bot.command(name='new', help="Start a new game. Needs a second player")
async def new_game(ctx, player2: User):
    await game.new_game(ctx, ctx.author, player2, bot.user)


@bot.command(name='p', help="place your token")
async def place_short(ctx: commands.Context, arg1: str, arg2: Optional[int]):
    await game.place(ctx, arg1, arg2)


@bot.command(name='place', help="place your token")
async def place(ctx: commands.Context,  arg1: str, arg2: Optional[int]):
    await game.place(ctx, arg1, arg2)


@new_game_short.error
async def new_game_short_error(ctx, error):
    await basic_error(ctx, error)


@new_game.error
async def new_game_error(ctx, error):
    await basic_error(ctx, error)


@place_short.error
async def place_short_error(ctx, error):
    await place_error(ctx, error)


@place.error
async def place_error(ctx, error):
    await basic_error(ctx, error)


async def basic_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Bad arguments')
        await ctx.send(error)
    else:
        await ctx.send('Command didn\'t work')
        await ctx.send(error)

bot.run(TOKEN)
