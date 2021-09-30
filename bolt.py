"""The BOLT and Swarm class document."""
from typing import Dict, List


class Bolt:
    """The BOLT python class."""

    def __init__(self) -> None:
        """BOLT, class constructor."""
        self.position: Dict[str, float] = {"x": 0.0, "y": 0.0}
        self.next_move: Dict[str, float] = {"x": 0.0, "y": 0.0}
        self.id: int = -1

    def register(self, code: int):
        """Bind a id to a BOLT."""
        self.id = code

    def set_next_move(self, x=None, y=None):
        """Set the next move of the BOLT."""
        if x is not None:
            self.next_move["x"] = x
        if y is not None:
            self.next_move["y"] = y

    def set_position(self, x=None, y=None):
        """Set the position of the BOLT to the given arguments <x> and <y>."""
        if x is not None:
            self.position["x"] = x
        if y is not None:
            self.position["y"] = y

    def is_busy(self):
        """Determine if the bolt still has a task at hand."""
        return not (
            self.next_move["x"] == self.position["x"]
            and self.next_move["y"] == self.position["y"]
        )


class Swarm:
    """A Swarm is a group of BOLT working together."""

    def __init__(self) -> None:
        """Create a Swarm of BOLT and coordinate them."""
        self.counter: int = 0
        self.bolts: List[Bolt] = []

    def register_bolt(self, bolt: Bolt):
        """Register a BOLT to the Swarm."""
        self.counter += 1
        self.bolts.append(bolt)
        bolt.register(self.counter)
        return self.counter

    def get_bolts(self):
        """Get the info of all the BOLTS."""
        return [bolt.__dict__ for bolt in self.bolts]

    def get_bolt(self, code: int):
        """Get the details of a single BOLT."""
        if code <= len(self.bolts):
            return self.bolts[code - 1].__dict__
        return None
