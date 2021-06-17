from typing import Optional


class Game():
    player_symbol = ["O", "X"]

    def __init__(self):
        self.reset()

    def reset(self):
        self.field = [[" ", " ", " "] for i in range(3)]
        self.current_player_idx = 0
        self.current_player_user = None

    def setField(self, x: int, y: int, player):
        player_name = player.nick if player.nick else player.name
        if self.field[y][x] != " ":
            raise Exception("Field already filled")

        if self.current_player_user == player:
            raise Exception(f"{player_name} :unamused: Wait your turn!")

        self.current_player_idx = (self.current_player_idx+1) % 2
        self.field[y][x] = self.player_symbol[self.current_player_idx]
        self.current_player_user = player

    def check_full(self):
        for i in range(3):
            for j in range(3):
                if self.field[i][j] == " ":
                    return False
        return True

    def check_winner(self) -> Optional[str]:
        # Diagonals
        if (self.field[0][0] == self.field[1][1] == self.field[2][2] != " "):
            return self.player_symbol[self.current_player_idx]
        if (self.field[0][2] == self.field[1][1] == self.field[2][0] != " "):
            return self.player_symbol[self.current_player_idx]
        for i in range(3):
            if (self.field[i][0]
                == self.field[i][1]
                    == self.field[i][2]
                    != " "):
                return self.player_symbol[self.current_player_idx]
            if (self.field[0][i]
                == self.field[1][i]
                    == self.field[2][i]
                    != " "):
                return self.player_symbol[self.current_player_idx]

        return None

    def print(self) -> str:
        return f"""```
  A B C
1 {"|".join(self.field[0])}
  ------
2 {"|".join(self.field[1])}
  ------
3 {"|".join(self.field[2])}```"""


def verify(x_str: str, y: int):
    if (x_str not in ["A", "B", "C"]):
        return False, "Only a, A, b, B, c, C"
    if(y not in [1, 2, 3]):
        return False, "Only 1, 2, 3"
    return True, None
