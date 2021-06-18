import os
from typing import Dict, Optional, Tuple

import discord.abc as abc
from discord import User
from discord.ext import commands
from dotenv import load_dotenv

from board import Board
from utils import user_name


class Game():
    _x_mapping = {"A": 0, "B": 1, "C": 2}

    def __init__(self):
        # Channel -> Board
        self._boards: Dict[str, Board] = {}

    async def new_game(self,
                       ctx: commands.Context,
                       creator: User,
                       otherPlayer: User,
                       botUser: User):
        if creator == otherPlayer:
            await ctx.send("Sorry you can't play against yourself!")
            await ctx.send("You need to find some friends :wink:")
            return
        if botUser == otherPlayer:
            await ctx.send("Sorry you can't play against me :confused:")
            await ctx.send("The robot uprising hasn't started :robot:")
            return

        if ctx.channel.id in self._boards:
            board = self._get_board(ctx.channel)
            assert isinstance(board, Board)
            board.reset(creator, otherPlayer)
        else:
            self._boards[ctx.channel.id] = Board(creator, otherPlayer)

        board = self._get_board(ctx.channel)

        # Null check
        assert isinstance(board, Board)

        await ctx.send("New game started!")
        await ctx.send(f" {user_name(creator)} vs {user_name(otherPlayer)}")
        await ctx.send(board.print())

    async def place(self,
                    ctx: commands.Context,
                    arg1: str,
                    arg2: Optional[int]):
        name = user_name(ctx.author)
        board = self._get_board(ctx.channel)
        try:
            x, y = self._handle_arguments(arg1, arg2)
        except Exception as e:
            await ctx.send(e)
            return
        else:
            await self._place_token(ctx, board, x, y, name)

    async def _place_token(self,
                           board: Board,
                           ctx: commands.Context,
                           x: int,
                           y: int,
                           name: str):
        try:
            board.setField(x, y-1, ctx.author)
        except Exception as e:
            await ctx.send(e)
        else:
            if board.check_full():
                await ctx.send(board.print())
                await ctx.send(f"It's a draw." +
                               f"Better luck next time" +
                               " :arrows_counterclockwise:")
                self._delete_board(ctx.channel)
                return

            winner = board.check_winner()
            if (winner):
                await ctx.send(board.print())
                await ctx.send(f"**{user_name(winner)}** has won\n" +
                               f"Congratulations" +
                               " :partying_face:")
                self._delete_board(ctx.channel)
                return
            else:
                await ctx.send(board.print())
                return

    def _handle_arguments(self, argarg1: str,
                          arg2: Optional[int]) -> Tuple[int, int]:

        arg1 = arg1.upper()
        valid, err = self._verify_arguments(arg1, arg2)
        print(valid, err)
        print(arg1, arg2)
        if (not valid):
            raise Exception(err)

        x = arg1 if arg2 else arg1[0]
        y = arg2 if arg2 else int(arg1[1])
        return self._x_mapping[x], y

    def _verify_arguments(self,
                          x: str,
                          y: Optional[int]) -> Tuple[bool, Optional[str]]:
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

    def _get_board(self, channel: abc.Messageable) -> Optional[Board]:
        return self._boards[channel.id]

    def _delete_board(self, channel: abc.Messageable):
        del self._boards[channel.id]
