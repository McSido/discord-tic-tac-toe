from typing import Optional


class Game():
    player_symbol = ["X", "O"]

    def __init__(self):
        self.reset()

    def reset(self):
        self.field = [[" ", " ", " "] for i in range(3)]
        self.current_player = 0

    def setField(self, x: int, y: int):
        if self.field[y][x] != " ":
            raise Exception("Field already filled")

        self.current_player = (self.current_player+1) % 2
        self.field[y][x] = self.player_symbol[self.current_player]

    def check_winner(self) -> Optional[str]:
        # Diagonals
        if (self.field[0][0] == self.field[1][1] == self.field[2][2] != " "):
            return self.player_symbol[self.current_player]
        if (self.field[0][2] == self.field[1][1] == self.field[2][0] != " "):
            return self.player_symbol[self.current_player]

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
        return False, "Only A, B, C"
    if(y not in [1, 2, 3]):
        return False, "Only 1, 2, 3"
    return True, None
