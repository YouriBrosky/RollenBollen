from time import sleep
import json
import unittest

from application import app

from bolt import Bolt


def create_bolt(x=None, y=None):
    bolt = Bolt()
    bolt.set_next_move(x=x, y=y)
    bolt.set_position(x=x, y=y)
    return bolt


class TestAppServer(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.client = app.test_client()
        self.API = "/api"
        self.maxDiff = None
        return super().setUp()

    def client_register(self, number=1):
        for _ in range(number):
            self.client.get(f"{self.API}/register")

    def client_move(self, code=0, x=0, y=0):
        self.client.get(f"{self.API}/bolt/{code}/moved?x={x}&y={y}")
        self.client.get(f"{self.API}/bolt/{code}/move?x={x}&y={y}")

    def test_reset_webserver(self):
        resp = handle_client_request(self.client.get(f"{self.API}/bolt"))
        exp_res = []
        self.assertEqual(resp, exp_res)
        self.client_register(2)
        resp = handle_client_request(self.client.get(f"{self.API}/bolt"))
        exp_res = [
            {"id": 1, "next_move": {"x": 0, "y": 0}, "position": {"x": 0, "y": 0}},
            {"id": 2, "next_move": {"x": 0, "y": 0}, "position": {"x": 0, "y": 0}},
        ]
        self.assertEqual(resp, exp_res)
        self.client.get(f"{self.API}/reset")
        resp = handle_client_request(self.client.get(f"{self.API}/bolt"))
        exp_res = []
        self.assertEqual(resp, exp_res)

    def test_api_index(self):
        result = handle_client_request(self.client.get(f"{self.API}"))
        exp_res = "Welkom bij de API"
        self.assertEqual(result, exp_res)
        handle_client_request(self.client.get(f"{self.API}"))

    def test_api_register(self):
        resp = handle_client_request(self.client.get(f"{self.API}/register"))
        result = handle_client_request(self.client.get(f"{self.API}/register"))
        exp_res = resp + 1
        self.assertEqual(result, exp_res)

        handle_client_request(self.client.get(f"{self.API}/register"))

    def test_api_list_bolts(self):
        self.client_register()
        resp = handle_client_request(self.client.get(f"{self.API}/bolt"))
        exp_res = [
            {"id": 1, "next_move": {"x": 0, "y": 0}, "position": {"x": 0, "y": 0}}
        ]
        self.assertEqual(resp, exp_res)
        self.client_register(3)
        exp_res = [
            {"id": 1, "next_move": {"x": 0, "y": 0}, "position": {"x": 0, "y": 0}},
            {"id": 2, "next_move": {"x": 0, "y": 0}, "position": {"x": 0, "y": 0}},
            {"id": 3, "next_move": {"x": 0, "y": 0}, "position": {"x": 0, "y": 0}},
            {"id": 4, "next_move": {"x": 0, "y": 0}, "position": {"x": 0, "y": 0}},
        ]
        resp = handle_client_request(self.client.get(f"{self.API}/bolt"))
        self.assertEqual(resp, exp_res)

    def test_api_bolt(self):
        self.client_register()
        code = 1

        resp = handle_client_request(self.client.get(f"{self.API}/bolt/{code}"))
        exp_res = {"id": 1, "next_move": {"x": 0, "y": 0}, "position": {"x": 0, "y": 0}}
        self.assertEqual(resp, exp_res)

    def test_api_bolt_move_x_y(self):
        self.client_register()
        code = 1
        xy = [(1, 1), (4, 3), (None, 6), (None, None), (0, None)]
        for x, y in xy:
            if x is not None:
                old_x = x
            if y is not None:
                old_y = y

            self.client.get(f"{self.API}/bolt/{code}/moved?x={x}&y={y}")
            resp = handle_client_request(self.client.get(f"{self.API}/bolt/{code}"))
            exp_res = {
                "id": 1,
                "next_move": {"x": 0, "y": 0},
                "position": {"x": old_x, "y": old_y},
            }
            self.assertEqual(resp, exp_res)

    def reset(self):
        self.client.get(f"{self.API}/reset")

    def test_api_bolt_set_next_move(self):
        self.client_register()
        code = 1
        xy = [(1, 1), (4, 3)]
        for x, y in xy:
            self.client.get(f"{self.API}/bolt/{code}/move?x={x}&y={y}")
            resp = handle_client_request(self.client.get(f"{self.API}/bolt/{code}"))
            exp_res = {
                "id": 1,
                "next_move": {"x": x, "y": y},
                "position": {"x": 0, "y": 0},
            }
            self.assertEqual(resp, exp_res)

    def test_api_bolt_goto(self):
        self.client_register()
        code = 1

        x = 4
        y = 3
        self.client.get(f"{self.API}/bolt/{code}/goto?x={x}&y={y}")

        path = handle_client_request(self.client.get(f"{self.API}/bolt/{code}/path"))
        for loc in path["optimal_route"]:
            resp = handle_client_request(
                self.client.get(f"{self.API}/bolt/{code}/command")
            )
            self.assertEqual(resp["x"], loc[0])
            self.assertEqual(resp["y"], loc[1])

    def test_api_bolt_command(self):
        self.client_register()
        code = 1
        x = 5
        y = 7
        self.client.get(f"{self.API}/bolt/{code}/move?x={x}&y={y}")
        result = handle_client_request(
            self.client.get(f"{self.API}/bolt/{code}/command")
        )
        exp_res = {"x": x, "y": y}
        self.assertEqual(result, exp_res)

    def test_api_bolt_path(self):
        self.client_register()
        code = 1

        x = 4
        y = 3
        self.client.get(f"{self.API}/bolt/{code}/goto?x={x}&y={y}")

        resp = handle_client_request(self.client.get(f"{self.API}/bolt/{code}/path"))
        exp_res = {
            "optimal_route": [[0, 4], [2, 4], [2, 3], [4, 3]],
            "path": [
                [0, 0],
                [0, 1],
                [0, 2],
                [0, 3],
                [0, 4],
                [1, 4],
                [2, 4],
                [2, 3],
                [3, 3],
                [4, 3],
            ],
        }

        self.assertEqual(resp, exp_res)

    def test_api_go_home(self):

        exp_res = [0, 0]
        for bolt in range(1, 6):
            self.client_register()
            self.client_move(bolt, 4, 3)
        self.client.get(f"{self.API}/home")
        for bolt in range(1, 6):
            result = handle_client_request(
                self.client.get(f"{self.API}/bolt/{bolt}/path")
            )
            self.assertEqual(result["path"][-1], exp_res)

    def test_api_nest_command(self):
        self.client_register(2)
        self.client_move(1, 3, 4)
        self.client_move(2, 2, 4)
        code = "00"
        result = handle_client_request(self.client.get(f"{self.API}/nest/{code}"))
        exp_res = {
            "bolt": 2,
            "optimal_route": [[0, 4], [0, 0]],
            "path": [[2, 4], [1, 4], [0, 4], [0, 3], [0, 2], [0, 1], [0, 0]],
        }
        self.assertEqual(result, exp_res)

    def test_api_get_maze(self):
        resp = handle_client_request(self.client.get(f"{self.API}/maze"))
        exp_res = {
            "maze": [
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                [1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
                [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 1, 0, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
            ]
        }
        self.assertEqual(resp, exp_res)
        xyv = [(6, 0, 0), (1, 6, 1)]
        for x, y, v in xyv:
            self.client.get(f"{self.API}/maze?x={x}&y={y}&v={v}")
        resp = handle_client_request(self.client.get(f"{self.API}/maze"))
        exp_res = {
            "maze": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
                [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 1, 0, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
            ]
        }
        self.assertEqual(resp, exp_res)


def handle_client_request(resp):
    return json.loads(resp.data.decode("utf-8"))
