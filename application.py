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

FACTORY_HALL = [
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


# region: Pages
@app.route("/", methods=["GET", "POST"])
def page_home():
    """Return the home page of the website."""
    sx = request.args.get("sx")
    sy = request.args.get("sy")
    fx = request.args.get("fx")
    fy = request.args.get("fy")
    if digit(sx) and digit(sy):
        start = Location(y=int(sx), x=int(sy))
    else:
        start = Location(x=0, y=0)
    if digit(fx) and digit(fy):
        finish = Location(y=int(fx), x=int(fy))
    else:
        finish = Location(x=9, y=0)
    m = Maze(factory=FACTORY_HALL, start=start, finish=finish)
    if request.method == "POST" and request.form["rand"] == "loc":
        # Section: New random finish
        rand_x = np.random.choice(np.arange(10))
        rand_y = (
            np.random.choice(np.arange(10))
            if rand_x != 0
            else np.random.choice(np.arange(1, 10))
        )
        m = Maze(
            factory=FACTORY_HALL,
            start=start,
            finish=Location(x=rand_x, y=rand_y),
        )
    final_dfs, path_dfs = depth_first_search(m.start, m.finish_line, m.frontier)
    if path_dfs is None:
        while path_dfs is None:
            m = Maze(factory=FACTORY_HALL, start=start, finish=finish)
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
        optimal_final_astar=optimize_path(final_astar),
    )


@app.route("/api/reset", methods=["GET"])
def reset_webserver():
    """Reset the server."""
    global swarm
    swarm = Swarm()
    global paths
    paths = {}
    global FACTORY_HALL
    FACTORY_HALL = [
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
    return "Success!"


# endregion
# region: Api
@app.route("/api", methods=["GET"])
def api_index():
    """Root mapping for the api."""
    return CORS_resp("Welkom bij de API")


@app.route("/api/register", methods=["GET"])
def api_register():
    """Register a BOLT via the API."""
    bolt = Bolt()
    return CORS_resp(swarm.register_bolt(bolt=bolt))


# region: Bolt
@app.route("/api/bolt", methods=["GET"])
def api_list_bolts():
    """Return a list of all BOLT's."""
    return CORS_resp(swarm.get_bolts())


@app.route("/api/bolt/<int:code>", methods=["GET"])
def api_bolt(code: int):
    """Get the details of a single BOLT.

    Parameters
    ----------
    code : int
        The bolt id

    Returns
    -------
    Bolt
        The info about the bolt
    """
    return_code = None
    if code:
        return_code = CORS_resp(swarm.get_bolt(code))
    return return_code


@app.route("/api/bolt/<int:code>/moved", methods=["GET"])
def api_bolt_move_x_y(code: int):
    """Move a BOLT.

    Parameters
    ----------
    code : int
        the id of the bolt

    Returns
    -------
    Bolt
        The info about the bolt
    """
    if code:
        x = request.args.get("x")
        y = request.args.get("y")
        if digit(x) and digit(y):
            swarm.get_bolt_by_id(code).set_position(x=int(x), y=int(y))
        elif digit(x):
            swarm.get_bolt_by_id(code).set_position(x=int(x))
        elif digit(y):
            swarm.get_bolt_by_id(code).set_position(y=int(y))
    return CORS_resp(swarm.get_bolt(code))


@app.route("/api/bolt/<int:code>/move", methods=["GET"])
def api_bolt_set_next_move(code: int):
    """Set the next move of a BOLT.

    Parameters
    ----------
    code : int
        the id of the bolt

    Returns
    -------
    Bolt
        The info about the bolt
    """
    if code:
        x = request.args.get("x")
        y = request.args.get("y")
        if digit(x) and digit(y):
            swarm.get_bolt_by_id(code).set_next_move(x=int(x), y=int(y))
        elif digit(x):
            swarm.get_bolt_by_id(code).set_next_move(x=int(x))
        elif digit(y):
            swarm.get_bolt_by_id(code).set_next_move(y=int(y))
    return CORS_resp(swarm.get_bolt(code))


@app.route("/api/bolt/<int:code>/goto", methods=["GET"])
def api_bolt_goto(code: int):
    """Set the next location of a BOLT.

    Parameters
    ----------
    code : int
        the id of the bolt

    Returns
    -------
    Bolt
        The info about the bolt
    """
    if code:
        x = request.args.get("x")
        y = request.args.get("y")
        if digit(x) and digit(y):
            route = get_path(code, int(x), int(y), factory_hall=FACTORY_HALL)
            opt_route = optimize_path(route)
            set_path(code, route)
            return CORS_resp({"path": route, "optimized_path": opt_route})
    return CORS_resp(swarm.get_bolt(code))


@app.route("/api/bolt/<int:code>/command", methods=["GET"])
def api_bolt_command(code: int):
    """Send a command to the bolt."""
    if code in paths and len(paths[code]["path"]) > 0:
        loc: Location = paths[code]["path"][paths[code]["counter"]]
        paths[code]["counter"] += 1
        if paths[code]["counter"] == len(paths[code]["path"]):
            del paths[code]
        swarm.get_bolt_by_id(code).set_position(x=loc.x, y=loc.y)
        return CORS_resp({"x": loc.x, "y": loc.y})
    pos = swarm.get_bolt_by_id(code).next_move
    swarm.get_bolt_by_id(code).set_position(x=pos["x"], y=pos["y"])
    return CORS_resp(pos)


@app.route("/api/bolt/<int:code>/path", methods=["GET"])
def api_bolt_path(code: int):
    """Get the path from a given bolt."""
    if code in paths and len(paths[code]["path"]) > 0:
        x = paths[code]["path"][-1].x
        y = paths[code]["path"][-1].y
        route = get_path(code=code, x=x, y=y, factory_hall=FACTORY_HALL)
        opt_route = optimize_path(route)
        return CORS_resp({"path": route, "optimal_route": opt_route})
    return CORS_resp(swarm.get_bolt_by_id(code).next_move)


@app.route("/api/home")
def api_go_home():
    """Send all bolts to 0, 0 AKA Homebase."""
    for bolt in swarm.bolts:
        route = get_path(bolt.id, 0, 0, factory_hall=FACTORY_HALL)
        set_path(bolt.id, route)
    return CORS_resp(swarm.get_bolts())


# endregion
# region: Nest
@app.route("/api/nest/<code>")
def api_nest_command(code: str):
    """Api-point for the Google Nest."""
    if len(code) == 1:
        code = "0" + code
    x = int(code[0])
    y = int(code[1])
    bolt_code = get_bolt(x, y)
    route = get_path(bolt_code, x, y, factory_hall=FACTORY_HALL)
    opt_route = optimize_path(route)
    set_path(bolt_code, route)
    return {"bolt": bolt_code, "path": route, "optimal_route": opt_route}


# endregion
# region: Maze
@app.route("/api/maze")
def api_get_maze():
    """Give the current maze, with options to edit the options."""
    x = request.args.get("x")
    y = request.args.get("y")
    value = request.args.get("v")
    if digit(x) and digit(y) and digit(value):
        FACTORY_HALL[int(y)][int(x)] = int(value)
    return CORS_resp({"maze": FACTORY_HALL})


# endregion


# endregion
# region: Custom Functions
def digit(string_value: str):
    """Check if a value is a string and digit.

    Parameters
    ----------
    string_value : str
        The string which should be a digit

    Returns
    -------
    Boolean
        is digit
    """
    return string_value and string_value.isdigit()


def get_path(code: int, x: int, y: int, factory_hall: List[List[int]]):
    """Get a path via A* for the given BOLT and coordinates.

    Parameters
    ----------
    code : int
        The id of the bolt
    x : int
        the x position
    y : int
        the y postition

    Returns
    -------
    List[Location]
        The final route from the current postition to the end position
    """
    pos = swarm.get_bolt_by_id(code).position
    start = Location(x=int(pos["x"]), y=int(pos["y"]))
    m = Maze(factory=factory_hall, start=start, finish=Location(x=x, y=y))
    distance = manhattan_distance(m.finish)
    final_astar, _ = astar(m.start, m.finish_line, m.frontier, distance)
    final_astar.append(m.finish)
    return [start] + final_astar


def set_path(code: int, path: List[Location]):
    """Set the Path of Bolt[<code>].

    Parameters
    ----------
    code : int
        The id of the bolt
    path : List[Location]
        The path (pre-optimization)
    """
    final_path = optimize_path(path)
    paths[code] = {"path": final_path, "counter": 0}
    swarm.get_bolt_by_id(code).next_move = {
        "x": final_path[-1].x,
        "y": final_path[-1].y,
    }


def optimize_path(path: List[Location]):
    """Optimize the path so it will be run in less actions.

    Parameters
    ----------
    path : List[Location]
        The original path

    Returns
    -------
    List[Location]
        The final optimized path
    """
    counter = 0
    optimized_path: List[Location] = []
    optimized_path.append(path[0])
    x = path[counter].x
    y = path[counter].y
    counter += 1
    while optimized_path[-1] != path[-1]:
        while counter < len(path) and (path[counter].x == x or path[counter].y == y):
            counter += 1
        optimized_path.append(path[counter - 1])
        if optimized_path[-1] != path[-1]:
            x = path[counter - 1].x
            y = path[counter - 1].y
    optimized_path = optimized_path[1:]
    return optimized_path


def get_bolt(x: int, y: int):
    """Get the id of the nearest Bolt to position x, y.

    Parameters
    ----------
    x : int
        The x position
    y : int
        The y position

    Returns
    -------
    int
        The id of the nearest BOLT
    """
    min_dist = 100
    bolt_id = -1
    for bolt in swarm.bolts:
        curr_dist = calc_dist(bolt.position, x, y)
        if not bolt.is_busy() and curr_dist < min_dist and curr_dist > 0:
            bolt_id = bolt.id
            min_dist = curr_dist
    return bolt_id


def calc_dist(xy_dict: Dict[str, int], x: int, y: int):
    """Calc the length of a path from the Bolt to <x> and <y>.

    Parameters
    ----------
    xy_dict : Dict[str, int]
        The x and y position of the BOLT
    x : int
        The end.x position
    y : int
        The end.y position

    Returns
    -------
    int
        The total length of the path
    """
    start = Location(x=int(xy_dict["x"]), y=int(xy_dict["y"]))
    m = Maze(factory=FACTORY_HALL, start=start, finish=Location(x=x, y=y))
    distance = manhattan_distance(m.finish)
    final_astar, _ = astar(m.start, m.finish_line, m.frontier, distance)
    return len(final_astar)


def CORS_resp(data):
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


# endregion

if __name__ == "__main__":
    app.run(port=80)
