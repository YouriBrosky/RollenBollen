import unittest

from RollenBollen.bolt import Bolt, Swarm


class TestBolt(unittest.TestCase):
    def setUp(self) -> None:
        self.bolt = Bolt()

    def test_method_set_next_move(self):
        x = 3
        y = 5
        self.bolt.set_next_move(x=x, y=y)
        self.assertEqual(self.bolt.next_move["x"], x)
        self.assertEqual(self.bolt.next_move["y"], y)

    def test_method_set_position(self):
        x = 3
        y = 5
        self.bolt.set_position(x=x, y=y)
        self.assertEqual(self.bolt.position["x"], x)
        self.assertEqual(self.bolt.position["y"], y)

    def test_method_is_busy(self):
        x = 3
        y = 5
        self.bolt.set_position(x=x, y=y)
        self.bolt.set_next_move(x=x, y=y)
        self.assertFalse(self.bolt.is_busy())

        self.bolt.set_next_move(x=x + 1, y=y)
        self.assertTrue(self.bolt.is_busy())

        self.bolt.set_next_move(x=x - 1, y=y)
        self.assertTrue(self.bolt.is_busy())

        self.bolt.set_next_move(x=x, y=y + 1)
        self.assertTrue(self.bolt.is_busy())

        self.bolt.set_next_move(x=x, y=y - 1)
        self.assertTrue(self.bolt.is_busy())

        self.bolt.set_next_move(x=x, y=y)
        self.assertFalse(self.bolt.is_busy())


class TestSwarm(unittest.TestCase):
    def setUp(self) -> None:
        self.swarm = Swarm()

    def test_method_register_bolt(self):
        bolt = Bolt()
        self.swarm.register_bolt(bolt)
        self.assertIn(bolt, self.swarm.bolts)

    def test_method_get_bolts(self):
        for _ in range(3):
            self.swarm.register_bolt(Bolt())
        self.assertEqual(len(self.swarm.get_bolts()), 3)

    def test_method_get_bolt(self):
        bolt = Bolt()
        bolt.set_position(x=1, y=2)
        bolt.set_next_move(x=4, y=3)
        self.swarm.register_bolt(bolt)
        result = self.swarm.get_bolt(1)
        expected_result = {
            "position": {"x": 1, "y": 2},
            "next_move": {"x": 4, "y": 3},
            "id": 1,
        }
        self.assertEqual(result, expected_result)

    def test_method_get_bolt_by_id(self):
        bolt = Bolt()
        self.swarm.register_bolt(bolt)
        self.assertEqual(bolt, self.swarm.get_bolt_by_id(1))
        bolt = Bolt()
        self.assertNotEqual(bolt, self.swarm.get_bolt_by_id(1))
        self.swarm.register_bolt(bolt)
        self.assertEqual(bolt, self.swarm.get_bolt_by_id(2))
