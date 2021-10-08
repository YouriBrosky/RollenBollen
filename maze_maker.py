# Verkregen van https://github.com/slevin886/maze_maker op 17/09/2021

from typing import List

from maze_search import astar, depth_first_search
from util import Location

factory_hall = [
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 0, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
]


class MazeSymbol:
    """Symbols to use when printing the maze"""

    start = "S"
    finish = "F"
    wall = "X"
    empty = " "
    path = "*"


class Maze:
    def __init__(
        self,
        factory=factory_hall,
        rows=10,
        columns=10,
        start=Location(0, 0),
        finish=Location(9, 0),
    ):
        self.factory: List[List[int]] = factory
        self.rows: int = rows
        self.columns: int = columns
        self.start: Location = start
        self.finish: Location = finish
        self.maze: List[List[MazeSymbol]] = [
            [MazeSymbol.empty for _ in range(columns)] for _ in range(rows)
        ]
        self._fill_maze()

    def _fill_maze(self):
        """Should Fill maze with X's as shown in self.factory above."""
        if self.rows == len(self.factory) or self.columns == len(self.factory):
            for row in range(self.rows):
                for col in range(self.columns):
                    if self.factory[row][col] == 1:
                        self.maze[row][col] = MazeSymbol.wall
        self.maze[self.start.x][self.start.y] = MazeSymbol.start
        self.maze[self.finish.x][self.finish.y] = MazeSymbol.finish

    def frontier(self, curr: Location):
        """curr is a Location for current location"""
        next_moves = []
        # Move one position up
        if curr.x - 1 >= 0 and self.maze[curr.x - 1][curr.y] != MazeSymbol.wall:
            next_moves.append(Location(curr.x - 1, curr.y))
        # Move one position left
        if curr.y - 1 >= 0 and self.maze[curr.x][curr.y - 1] != MazeSymbol.wall:
            next_moves.append(Location(curr.x, curr.y - 1))
        # Move one position right
        if (
            curr.y + 1 < self.columns
            and self.maze[curr.x][curr.y + 1] != MazeSymbol.wall
        ):
            next_moves.append(Location(curr.x, curr.y + 1))
        # Move one position down
        if curr.x + 1 < self.rows and self.maze[curr.x + 1][curr.y] != MazeSymbol.wall:
            next_moves.append(Location(curr.x + 1, curr.y))
        return next_moves

    def finish_line(self, curr: Location):
        return curr.x == self.finish.x and curr.y == self.finish.y

    def draw_path(self, path: List[Location]):
        for loc in path:
            self.maze[loc.x][loc.y] = MazeSymbol.path

    def clear_path(self, path: List[Location]):
        for loc in path:
            self.maze[loc.x][loc.y] = MazeSymbol.empty


def manhattan_distance(finish: Location):
    def distance(loc: Location):
        xdistance = abs(loc.y - finish.y)
        ydistance = abs(loc.x - finish.x)
        return xdistance + ydistance

    return distance