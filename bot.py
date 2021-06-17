import os
import random
from dotenv import load_dotenv
from discord.ext import commands
from game import Game


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!3')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


game = Game()

@bot.command(name='new', help="Start a new game")
async def tic_tac_toe(ctx, x: int, y: int):
    game = Game()

    await ctx.send("New game started")


@bot.command(name='place', help="TIC TAC TOE COMMAND")
async def tic_tac_toe(ctx, x: int, y: int):
    if(x not in range(1, 3) or y not in range(1, 3)):
        await ctx.send("Only numbers between 1-3 work")
        return

    game.field[x-1][y-1] = "X"

    await ctx.send(game.field)


@tic_tac_toe.error
async def tic_tac_toe_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Bad arguments')
        await ctx.send(error)
    else:
        await ctx.send('Command didn\'t work')
        await ctx.send(error)

bot.run(TOKEN)
