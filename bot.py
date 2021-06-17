import os
import random
from dotenv import load_dotenv
from discord.ext import commands
from game import Game, verify


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!3')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

x_mapping = {"A": 0, "B": 1, "C": 2}
game = Game()


@bot.command(name='new', help="Start a new game")
async def new_game(ctx):
    game.reset()

    await ctx.send("New game started")
    await ctx.send(game.print())


@bot.command(name='place', help="place your token")
async def place(ctx: commands.Context, x_str: str, y: int):
    name = ctx.author.nick if ctx.author.nick else ctx.author.name

    valid, msg = verify(x_str, y)

    if (not valid):
        await ctx.send(msg)
        return

    x = x_mapping[x_str]

    try:
        game.setField(x, y-1)
    except Exception as e:
        await ctx.send(e)
    else:
        winner = game.check_winner()
        if (winner):
            await ctx.send(game.print())
            await ctx.send(f"**{winner}** has won\n" +
                           f"Congratulations {name}" +
                           " :partying_face:")
            game.reset()
        else:
            await ctx.send(game.print())


@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Bad arguments')
        await ctx.send(error)
    else:
        await ctx.send('Command didn\'t work')
        await ctx.send(error)

bot.run(TOKEN)
