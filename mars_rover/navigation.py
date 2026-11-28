from mars_rover.grid import Grid
from mars_rover.heading import turn_left, turn_right

MOVES = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}


class Rover:
    def __init__(self, x: int, y: int, heading: str, grid: Grid | None = None) -> None:
        self.x = x
        self.y = y
        self.heading = heading
        self.grid = grid

    def turn_left(self) -> None:
        self.heading = turn_left(self.heading)

    def turn_right(self) -> None:
        self.heading = turn_right(self.heading)

    def move_forward(self) -> bool:
        dx, dy = MOVES[self.heading]
        new_x, new_y = self.x + dx, self.y + dy
        if self.grid is not None and not self.grid.contains(new_x, new_y):
            return False
        self.x, self.y = new_x, new_y
        return True
