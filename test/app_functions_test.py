import unittest

from application import (
    calc_dist,
    digit,
    find_path,
    get_bolt,
    get_path,
    optimize_path,
)
from bolt import Bolt, Swarm
from util import Location


def create_bolt(x=None, y=None):
    bolt = Bolt()
    bolt.set_next_move(x=x, y=y)
    bolt.set_position(x=x, y=y)
    return bolt


class TestAppFunctions(unittest.TestCase):
    def test_get_bolt(self):
        swarm = Swarm()
        swarm.register_bolt(create_bolt(0, 2))
        swarm.register_bolt(create_bolt(4, 3))
        result = get_bolt(0, 0, swarm=swarm)
        self.assertEqual(result, 1)
        result = get_bolt(2, 3, swarm=swarm)
        self.assertEqual(result, 2)

    def test_calc_dist(self):
        start = {"x": 1, "y": 2}
        x = 1
        y = 2
        result = calc_dist(start_pos=start, x=x, y=y)
        self.assertEqual(result, 0)
        start = {"x": 0, "y": 0}
        result = calc_dist(start_pos=start, x=x, y=y)
        self.assertEqual(result, 2)
        x = 2
        y = 4
        result = calc_dist(start_pos=start, x=x, y=y)
        self.assertEqual(result, 5)

    def test_optimize_path(self):
        path = [
            Location(x=0, y=0),
            Location(x=0, y=1),
            Location(x=0, y=2),
            Location(x=0, y=3),
            Location(x=1, y=3),
            Location(x=2, y=3),
            Location(x=2, y=2),
            Location(x=2, y=1),
            Location(x=2, y=0),
        ]
        result = optimize_path(path=path)
        exp_res = [Location(x=0, y=3), Location(x=2, y=3), Location(x=2, y=0)]
        self.assertEqual(result, exp_res)

    def test_get_path(self):
        swarm = Swarm()
        swarm.register_bolt(create_bolt())
        res = get_path(1, 2, 0, swarm)
        exp_res = [
            Location(x=0, y=0),
            Location(x=0, y=1),
            Location(x=0, y=2),
            Location(x=0, y=3),
            Location(x=0, y=4),
            Location(x=1, y=4),
            Location(x=2, y=4),
            Location(x=2, y=3),
            Location(x=2, y=2),
            Location(x=2, y=1),
            Location(x=2, y=0),
        ]
        self.assertEqual(res, exp_res)

    def test_find_path(self):
        layout = [[0, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0]]
        result = find_path(0, 0, 2, 0, layout=layout)
        exp_res = [
            Location(x=0, y=0),
            Location(x=0, y=1),
            Location(x=0, y=2),
            Location(x=0, y=3),
            Location(x=1, y=3),
            Location(x=2, y=3),
            Location(x=2, y=2),
            Location(x=2, y=1),
            Location(x=2, y=0),
        ]
        self.assertEqual(result, exp_res)

    def test_digit(self):
        self.assertTrue(digit("1"))
        self.assertTrue(digit("2"))
        self.assertTrue(digit("05"))
        self.assertTrue(digit("93"))
        self.assertFalse(digit("a"))
        self.assertFalse(digit("9o"))
        self.assertFalse(digit("io"))
