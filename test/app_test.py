import unittest

from application import (
    app,
    calc_dist,
    digit,
    find_path,
    get_bolt,
    get_path,
    optimize_path,
    set_path,
)
from flask import json

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


class TestAppServer(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.client = app.test_client()
        self.API = "/api"

    def client_register(self):
        self.client.get(f"{self.API}/register")

    def client_move(self, code=0, x=0, y=0):
        self.client.get(f"{self.API}/bolt/{code}/moved?x={x}&y={y}")
        self.client.get(f"{self.API}/bolt/{code}/move?x={x}&y={y}")

    def test_page_home(self):
        # TODO(Philip): Create a unittest!
        self.fail("TODO(Philip): Create a unittest!")

    def test_reset_webserver(self):
        # TODO(Philip): Create a unittest!
        self.fail("TODO(Philip): Create a unittest!")

        print(self.client.get(f"{self.API}/reset"))

    def test_api_index(self):
        # TODO(Philip): Create a unittest!
        self.fail("TODO(Philip): Create a unittest!")

        handle_client_request(self.client.get(f"{self.API}"))

    def test_api_register(self):
        # TODO(Philip): Create a unittest!
        self.fail("TODO(Philip): Create a unittest!")

        handle_client_request(self.client.get(f"{self.API}/register"))

    def test_api_list_bolts(self):
        self.client_register()
        resp = handle_client_request(self.client.get(f"{self.API}/bolt"))
        exp_val = [
            {
                "id": 1,
                "next_move": {"x": 0.0, "y": 0.0},
                "position": {"x": 0.0, "y": 0.0},
            }
        ]
        self.assertEqual(resp, exp_val)
        self.client_register()
        self.client_register()
        self.client_register()
        exp_val = [
            {
                "id": 1,
                "next_move": {"x": 0.0, "y": 0.0},
                "position": {"x": 0.0, "y": 0.0},
            },
            {
                "id": 2,
                "next_move": {"x": 0.0, "y": 0.0},
                "position": {"x": 0.0, "y": 0.0},
            },
            {
                "id": 3,
                "next_move": {"x": 0.0, "y": 0.0},
                "position": {"x": 0.0, "y": 0.0},
            },
            {
                "id": 4,
                "next_move": {"x": 0.0, "y": 0.0},
                "position": {"x": 0.0, "y": 0.0},
            },
        ]
        resp = handle_client_request(self.client.get(f"{self.API}/bolt"))
        self.assertEqual(resp, exp_val)

    def test_api_bolt(self):
        # TODO(Philip): Create a unittest!
        self.fail("TODO(Philip): Create a unittest!")

        self.client_register()
        code = 1
        handle_client_request(self.client.get(f"{self.API}/bolt/{code}"))

    def test_api_bolt_move_x_y(self):
        # TODO(Philip): Create a unittest!
        self.fail("TODO(Philip): Create a unittest!")

        self.client_register()
        code = 1
        handle_client_request(self.client.get(f"{self.API}/bolt/{code}/moved"))

    def test_api_bolt_set_next_move(self):
        # TODO(Philip): Create a unittest!
        self.fail("TODO(Philip): Create a unittest!")

        code = 1
        handle_client_request(self.client.get(f"{self.API}/bolt/{code}/move"))

    def test_api_bolt_goto(self):
        # TODO(Philip): Create a unittest!
        self.fail("TODO(Philip): Create a unittest!")

        code = 1
        handle_client_request(self.client.get(f"{self.API}/bolt/{code}/goto"))

    def test_api_bolt_command(self):
        # TODO(Philip): Create a unittest!
        self.fail("TODO(Philip): Create a unittest!")

        self.client_register()
        code = 1
        handle_client_request(self.client.get(f"{self.API}/bolt/{code}/command"))

    def test_api_bolt_path(self):
        # TODO(Philip): Create a unittest!
        self.fail("TODO(Philip): Create a unittest!")

        self.client_register()
        code = 1
        handle_client_request(self.client.get(f"{self.API}/bolt/{code}/path"))

    def test_api_go_home(self):
        # TODO(Philip): Create a unittest!
        self.fail("TODO(Philip): Create a unittest!")

        self.client_register()
        code = 1
        self.client_move(code, 2, 4)
        handle_client_request(self.client.get(f"{self.API}/home"))

    def test_api_nest_command(self):
        self.client_register()
        self.client_register()
        self.client_move(1, 3, 4)
        self.client_move(2, 2, 4)
        code = "00"
        resp = handle_client_request(self.client.get(f"{self.API}/nest/{code}"))
        expected_value = {
            "bolt": 2,
            "optimal_route": [[0, 4], [0, 0]],
            "path": [[2, 4], [1, 4], [0, 4], [0, 3], [0, 2], [0, 1], [0, 0]],
        }
        self.assertEqual(resp, expected_value)

    def test_api_get_maze(self):
        # TODO(Philip): Create a unittest!
        self.fail("TODO(Philip): Create a unittest!")

        handle_client_request(self.client.get(f"{self.API}/maze"))


def handle_client_request(resp):
    return json.loads(resp.data.decode("utf-8"))
