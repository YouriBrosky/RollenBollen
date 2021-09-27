"""The flask api to run the BOLT Swarm."""
from typing import Dict, List, Union

import numpy as np
from flask import Flask, jsonify, render_template, request

from bolt import Bolt, Swarm
from maze_maker import Location, Maze, manhattan_distance
from maze_search import astar, breadth_first_search, depth_first_search

app: Flask = Flask(__name__, template_folder="templates")
swarm: Swarm = Swarm()
paths: Dict[int, Dict[str, Union[int, List[Location]]]] = {}


# region: Pages
@app.route("/", methods=["GET", "POST"])
def page_home():
    """Return the home page of the website."""
    m = Maze()
    if request.method == "POST" and request.form["rand"] == "loc":
        # Section: New random finish
        rand_x = np.random.choice(np.arange(5))
        rand_y = (
            np.random.choice(np.arange(5))
            if rand_x != 0
            else np.random.choice(np.arange(1, 5))
        )
        m = Maze(finish=Location(x=rand_x, y=rand_y))
    final_dfs, path_dfs = depth_first_search(m.start, m.finish_line, m.frontier)
    if path_dfs is None:
        while path_dfs is None:
            m = Maze()
            final_dfs, path_dfs = depth_first_search(m.start, m.finish_line, m.frontier)
    final_bfs, path_bfs = breadth_first_search(m.start, m.finish_line, m.frontier)
    distance = manhattan_distance(m.finish)
    final_astar, path_astar = astar(m.start, m.finish_line, m.frontier, distance)

    return render_template(
        "home.html",
        maze_map=m.maze,
        dfs_path=path_dfs,
        bfs_path=path_bfs,
        astar_path=path_astar,
        final_bfs=final_bfs,
        final_dfs=final_dfs,
        final_astar=final_astar,
    )


@app.route("/reset", methods=["GET"])
def reset_webserver():
    """Reset the server."""
    global swarm
    swarm = Swarm()
    global paths
    paths = {}
    return "Succes!"


# endregion


# region: Api
@app.route("/api", methods=["GET"])
def api_index():
    """Root mapping for the api."""
    return "Welkom bij de API"


@app.route("/api/register", methods=["GET"])
def api_register():
    """Register a BOLT via the API."""
    bolt = Bolt()
    return jsonify(swarm.register_bolt(bolt=bolt))


# region: Bolt
@app.route("/api/bolt", methods=["GET"])
def api_list_bolts():
    """Return a list of all BOLT's."""
    return jsonify(swarm.get_bolts())


@app.route("/api/bolt/<int:code>", methods=["GET"])
def api_bolt(code: int):
    """Get the details of a single BOLT."""
    return_code = None
    if code:
        return_code = jsonify(swarm.get_bolt(code))
    return return_code


@app.route("/api/bolt/<int:code>/moved", methods=["GET"])
def api_bolt_move_x_y(code: int):
    """Move a BOLT."""
    ret_string = "BOLT not found"
    if code:
        x = request.args.get("x")
        y = request.args.get("y")
        if x and x.isdigit() and y and y.isdigit():
            swarm.bolts[code - 1].set_position(x=int(x), y=int(y))
            ret_string = f"BOLT<{code}> moved to {x}, {y}"
        elif x and x.isdigit():
            swarm.bolts[code - 1].set_position(x=int(x))
            ret_string = f"BOLT<{code}> moved to {x}"
        elif y and y.isdigit():
            swarm.bolts[code - 1].set_position(y=int(y))
            ret_string = f"BOLT<{code}> moved to {y}"
    return ret_string


@app.route("/api/bolt/<int:code>/move", methods=["GET"])
def api_bolt_set_next_move(code: int):
    """Set the next move of a BOLT."""
    ret_string = "Request Failed!"
    if code:
        x = request.args.get("x")
        y = request.args.get("y")
        if x and x.isdigit() and y and y.isdigit():
            swarm.bolts[code - 1].set_next_move(x=int(x), y=int(y))
            ret_string = f"Request Succes, moving BOLT<{code}> to x:{x}, y:{y}"
        elif x and x.isdigit():
            swarm.bolts[code - 1].set_next_move(x=int(x))
            ret_string = f"Request Succes, moving BOLT<{code}> to x:{x}"
        elif y and y.isdigit():
            swarm.bolts[code - 1].set_next_move(y=int(y))
            ret_string = f"Request Succes, moving BOLT<{code}> to y:{y}"
    return ret_string


@app.route("/api/bolt/<int:code>/goto", methods=["GET"])
def api_bolt_goto(code: int):
    """Set the next location of a BOLT."""
    ret_string = "Request Failed!"
    if code:
        x = request.args.get("x")
        y = request.args.get("y")
        if x and x.isdigit() and y and y.isdigit():
            get_path(code, int(x), int(y))
            ret_string = f"Request Succes, new location of BOLT<{code}> is x:{x}, y:{y}"
    return ret_string


def get_path(code: int, x: int, y: int):
    """Get a path via A* for the given BOLT and coordinates."""
    global swarm
    pos = swarm.bolts[code - 1].position
    start = Location(x=int(pos["x"]), y=int(pos["y"]))
    m = Maze(start=start, finish=Location(x=x, y=y))
    distance = manhattan_distance(m.finish)
    final_astar, _ = astar(m.start, m.finish_line, m.frontier, distance)
    final_astar.append(m.finish)
    paths[code] = {"path": final_astar, "counter": 0}
    swarm.bolts[code - 1].next_move = {"x": final_astar[-1].x, "y": final_astar[-1].y}


def get_bolt(x, y):
    """Get the id of the nearest Bolt to position x, y."""
    global swarm
    min_dist = 100
    bolt_id = -1
    for bolt in swarm.bolts:
        if (
            calc_dist(bolt.position, x, y) < min_dist
            and calc_dist(bolt.position, x, y) > 0
        ):
            bolt_id = bolt.id
            min_dist = calc_dist(bolt.position, x, y)
    return bolt_id


def calc_dist(xy_dict, x, y):
    """Calc the length of a path from the Bolt to <x> and <y>."""
    start = Location(x=int(xy_dict["x"]), y=int(xy_dict["y"]))
    m = Maze(start=start, finish=Location(x=x, y=y))
    distance = manhattan_distance(m.finish)
    final_astar, _ = astar(m.start, m.finish_line, m.frontier, distance)

    return len(final_astar)


@app.route("/api/bolt/<int:code>/command", methods=["GET"])
def api_bolt_command(code: int):
    """Send a command to the bolt."""
    global paths
    if code in paths and len(paths[code]["path"]) > 0:
        loc: Location = paths[code]["path"][paths[code]["counter"]]
        paths[code]["counter"] += 1
        if paths[code]["counter"] == len(paths[code]["path"]):
            del paths[code]
        swarm.bolts[code - 1].set_position(x=loc.x, y=loc.y)
        return {"x": loc.x, "y": loc.y}
    pos = swarm.bolts[code - 1].next_move
    swarm.bolts[code - 1].set_position(x=pos["x"], y=pos["y"])
    return jsonify(pos)


@app.route("/api/home")
def api_go_home():
    """Send all bolts to 0, 0 AKA Homebase."""
    for bolt in swarm.bolts:
        get_path(bolt.id, 0, 0)


# endregion

# region: Nest
@app.route("/api/nest/<code>")
def api_nest_command(code: str):
    """The api-point for the Google Nest."""
    if len(code) == 1:
        code = "0" + code
    x = int(code[0])
    y = int(code[1])

    bolt_code = get_bolt(x, y)
    get_path(bolt_code, x, y)

    return f"<h1>NEST</h1><br><p>bolt:{bolt_code} GOTO x:{x}, y:{y}</p>"


# endregion

# endregion


if __name__ == "__main__":
    app.run(port=80)
