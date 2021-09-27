# Verkregen van https://github.com/slevin886/maze_maker op 17/09/2021

from math import sqrt
from typing import NamedTuple

from maze_search import astar, depth_first_search

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


class Location(NamedTuple):
    """Maze locations in the grid as x, y coordinates"""

    x: int
    y: int


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
        barriers=0.4,
        start=Location(0, 0),
        finish=Location(9, 0),
    ):
        self.factory = factory
        self.rows = rows
        self.columns = columns
        self.barriers = barriers
        self.start = start
        self.finish = finish
        self.maze = [
            [MazeSymbol.empty for col in range(columns)] for row in range(rows)
        ]
        self._fill_maze()

    def _fill_maze(self):
        """Should Fill maze with X's as shown in "factory_hall" above."""
        print(self.factory)
        if self.rows == len(factory_hall) or self.columns == len(factory_hall[0]):
            for row in range(self.rows):
                for col in range(self.columns):
                    if factory_hall[row][col] == 1:
                        self.maze[row][col] = MazeSymbol.wall
        self.maze[self.start.x][self.start.y] = MazeSymbol.start
        self.maze[self.finish.x][self.finish.y] = MazeSymbol.finish

    def frontier(self, curr):
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

    def finish_line(self, curr):
        if curr.x == self.finish.x and curr.y == self.finish.y:
            return True
        return False

    def draw_path(self, path):
        for loc in path:
            self.maze[loc.x][loc.y] = MazeSymbol.path

    def clear_path(self, path):
        for loc in path:
            self.maze[loc.x][loc.y] = MazeSymbol.empty

    def __str__(self):
        """Prints the current maze state if used outside of browser, mainly for debugging"""
        pretty_printed = ""
        for num, row in enumerate(self.maze):
            if num == 0:
                pretty_printed += "".join("_" for _ in range(self.columns + 2)) + "\n"
            pretty_printed += "|"
            for space in row:
                pretty_printed += space
            if num == (self.columns - 1):
                pretty_printed += (
                    "|\n" + "".join("-" for _ in range(self.columns + 2)) + "\n"
                )
                break
            pretty_printed += "|\n"
        return pretty_printed


def euclidean_distance(finish_line):
    def distance(loc):
        xdistance = loc.column - finish_line.column
        ydistance = loc.row - finish_line.row
        return sqrt((xdistance ** 2) + (ydistance ** 2))

    return distance


def manhattan_distance(finish):
    def distance(loc):
        xdistance = abs(loc.y - finish.y)
        ydistance = abs(loc.x - finish.x)
        return xdistance + ydistance

    return distance


if __name__ == "__main__":
    m = Maze()
    print(m)
    depth_path, depth_search = depth_first_search(m.start, m.finish_line, m.frontier)
    if depth_path is None:
        print("No successful solution for this maze")
    m.draw_path(depth_path)
    print(m)
    m.clear_path(depth_path)
    distance = manhattan_distance(m.finish)
    astar_path, astar_search = astar(m.start, m.finish_line, m.frontier, distance)
    if astar_path is None:
        print("No successful solution to this maze.")
    m.draw_path(astar_path)
    print(m)
