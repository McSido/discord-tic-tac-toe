import os
import random
from dotenv import load_dotenv
from discord.ext import commands
from game import Game
from typing import Optional, Tuple

x_mapping = {"A": 0, "B": 1, "C": 2}
game = Game()


async def new_game(ctx):
    game.reset()

    await ctx.send("New game started")
    await ctx.send(game.print())


async def place(ctx: commands.Context, arg1: str, arg2: Optional[int]):
    name = ctx.author.nick if ctx.author.nick else ctx.author.name
    try:
        x, y = handle_arguments(arg1, arg2)
        print("X", x, "Y", y)
    except Exception as e:
        await ctx.send(e)
        return
    else:
        await place_token(ctx, x, y, name)


async def place_token(ctx: commands.Context, x: int, y: int, name: str):
    try:
        game.setField(x, y-1, ctx.author)
    except Exception as e:
        await ctx.send(e)
    else:
        if game.check_full():
            await ctx.send(game.print())
            await ctx.send(f"It's a draw." +
                           f"Better luck next time" +
                           " :arrows_counterclockwise:")
            game.reset()
            return

        winner = game.check_winner()
        if (winner):
            await ctx.send(game.print())
            await ctx.send(f"**{winner}** has won\n" +
                           f"Congratulations {name}" +
                           " :partying_face:")
            game.reset()
            return
        else:
            await ctx.send(game.print())
            return


def handle_arguments(arg1: str,
                     arg2: Optional[int]) -> Tuple[int, int]:

    arg1 = arg1.upper()
    valid, err = verify_arguments(arg1, arg2)
    print(valid, err)
    print(arg1, arg2)
    if (not valid):
        raise Exception(err)

    x = arg1 if arg2 else arg1[0]
    y = arg2 if arg2 else int(arg1[1])
    return x_mapping[x], y


def verify_arguments(x: str, y: Optional[int]) -> Tuple[bool, Optional[str]]:
    if (y is not None):
        if (x not in ["A", "B", "C"]):
            return False, "Only a, A, b, B, c, C"
        if (y not in [1, 2, 3]):
            return False, "Only 1, 2, 3"
    else:
        if len(x) != 2:
            return False, f"Invalid argument {x}"
        if (x[0] not in ["A", "B", "C"]):
            return False, "Only a, A, b, B, c, C"
        if (int(x[1]) not in [1, 2, 3]):
            return False, "Only 1, 2, 3"

    return True, None
