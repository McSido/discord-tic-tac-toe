from typing import Optional

import discord.abc as abc
from discord import User
from discord.ext import commands

from utils import user_name


class Player():
    def __init__(self, user: User, symbol: str) -> None:
        self.user = user
        self.symbol = symbol

    def name(self):
        return user_name


class Board():

    def __init__(self, player1: User, player2: User) -> None:
        self.reset(player1, player2)

    def reset(self, player1: User, player2: User):
        self.field = [[" ", " ", " "] for i in range(3)]
        self.players = [Player(player1, "X"), Player(player2, "O")]
        self.curr_player_idx = 0

    def setField(self, x: int, y: int, player: Player):
        if self.field[y][x] != " ":
            raise Exception("Field already filled")

        if self._get_current_player().user == player:
            raise Exception(f"{user_name(player)} :unamused: Wait your turn!")

        self.current_player_idx = (self.curr_player_idx+1) % 2
        self.field[y][x] = self._get_current_player().symbol
        self.current_player_user = player

    def check_full(self):
        for i in range(3):
            for j in range(3):
                if self.field[i][j] == " ":
                    return False
        return True

    def check_winner(self) -> Optional[User]:
        # Diagonals
        if (self.field[0][0] == self.field[1][1] == self.field[2][2] != " "):
            return self._get_current_player().user
        if (self.field[0][2] == self.field[1][1] == self.field[2][0] != " "):
            return self._get_current_player().user
        for i in range(3):
            if (self.field[i][0]
                == self.field[i][1]
                    == self.field[i][2]
                    != " "):
                return self._get_current_player().user
            if (self.field[0][i]
                == self.field[1][i]
                    == self.field[2][i]
                    != " "):
                return self._get_current_player().user

        return None

    def print(self) -> str:
        return f"""```
  A B C
1 {"|".join(self.field[0])}
  ------
2 {"|".join(self.field[1])}
  ------
3 {"|".join(self.field[2])}```"""

    def _get_current_player(self):
        return self.players[self.curr_player_idxs]
