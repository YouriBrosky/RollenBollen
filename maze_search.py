# Verkregen van https://github.com/slevin886/maze_maker op 17/09/2021

from collections import deque
from heapq import heappop, heappush
from typing import Callable, List

from util import Location


class Stack:
    def __init__(self):
        self._next_moves = []

    def push(self, loc):
        self._next_moves.append(loc)

    def pop(self):
        return self._next_moves.pop()

    @property
    def stuck(self):
        return not self._next_moves

    def __repr__(self):
        if self._next_moves:
            return repr([(loc.x, loc.y) for loc in self._next_moves])
        return None


class Queue:
    def __init__(self):
        self._next_moves = deque()

    def push(self, loc):
        self._next_moves.append(loc)

    def pop(self):
        return self._next_moves.popleft()

    @property
    def stuck(self):
        return not self._next_moves

    def __repr__(self):
        if self._next_moves:
            return repr([(loc.x, loc.y) for loc in self._next_moves])
        return None


class PriorityQueue:
    def __init__(self):
        self._container = []

    @property
    def empty(self):
        return not self._container

    def push(self, item):
        heappush(self._container, item)

    def pop(self):
        return heappop(self._container)

    def __repr__(self):
        return repr(self._container)


class Move:
    def __init__(self, current, previous, cost=0.0, heuristic=0.0):
        self.current = current
        self.previous = previous
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        """
        This method is a comparison of cost functions for two moves based on euclidean distance to the maze end.
        :param other: another object of class Move
        :return: Bool
        """
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def get_path(search_algorithm, locations):
    path = []
    while locations.previous is not None:
        locations = locations.previous
        path.append(locations.current)
    # print("{} - Path: {}".format(searchAlgorithm, path[::-1]))
    return path[::-1]


def depth_first_search(start, finish_line, next_moves):
    """
    Algorithm for a depth-first search on class Maze
    :param start: of class 'Move' includes a class 'Location' of current and previous moves
    :param finish_line: a function from class 'Maze' that checks if you reached the finish line
    :param next_moves: a list of class Location for available next moves given a Location
    :return: None if there is no maze solution or embedded Class 'Move' with the path and all searched locations.
    """
    frontier = Stack()
    frontier.push(Move(start, None))
    searched = {start}
    full_search = []
    while not frontier.stuck:
        loc = frontier.pop()
        active = loc.current
        full_search.append(active)
        if finish_line(active):
            final_path = get_path("Depth First:", loc)
            return final_path[1:], full_search[1:-1]
        for space in next_moves(active):
            if space not in searched:
                searched.add(space)
                frontier.push(Move(space, loc))
    return None, None


def breadth_first_search(start, finish_line, next_moves):
    """
    Algorithm for a breadth-first search on class Maze
    :param start: of class 'Move' includes a class 'Location' of current and previous moves
    :param finish_line: a function from class 'Maze' that checks if you reached the finish line
    :param next_moves: a list of class Location for available next moves given a Location
    :return: None if there is no maze solution or embedded Class 'Move' with the path and all searched locations.
    """
    frontier = Queue()
    frontier.push(Move(start, None))
    searched = {start}
    full_search = []
    while not frontier.stuck:
        loc = frontier.pop()
        active = loc.current
        full_search.append(active)
        if finish_line(active):
            final_path = get_path("Breadth First:", loc)
            return final_path[1:], full_search[1:-1]
        for space in next_moves(active):
            if space not in searched:
                searched.add(space)
                frontier.push(Move(space, loc))
    return None, None


def astar(
    start: Location,
    finish_line: Callable[[Location], bool],
    next_moves: Callable[[Location], List[Location]],
    heuristic: Callable[[Location], int],
):
    frontier = PriorityQueue()
    frontier.push(Move(start, None, 0.0, heuristic(start)))
    searched = {start: 0.0}
    full_search = []
    while not frontier.empty:
        loc = frontier.pop()
        active = loc.current
        full_search.append(active)
        if finish_line(active):
            final_path = get_path("A*:", loc)
            return final_path[1:], full_search[1:-1]
        for space in next_moves(active):
            new_cost = loc.cost + 1
            if space not in searched or searched[space] > new_cost:
                searched[space] = new_cost
                frontier.push(Move(space, loc, new_cost, heuristic(space)))
    return None
