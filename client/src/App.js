import React from "react";
import { apiLink, layoutSize } from ".";
import "./App.css";
import BoltView from "./Component/BoltView";
import ButtonView from "./Component/ButtonView";
import GridView from "./Component/GridView";
const App = (props) => {
  const [cursor, setCursor] = React.useState("#C8EFF9");
  const [grids, setGrids] = React.useState([]);
  const [bolts, setBolts] = React.useState([]);
  React.useEffect(() => {
    const getMaze = async () => {
      const response = await fetch(apiLink + "maze");
      const json = await response.json();
      // JSON is object with property 'maze'
      const maze = json.maze;
      const array = [];
      for (let i = 0; i < maze.length; i++) {
        for (let j = 0; j < maze[i].length; j++) {
          array.push({
            index: i * layoutSize + j,
            util:
              maze[i][j] === 0
                ? //available
                "#C8EFF9"
                : //obstacle
                "#e71d07",
          });
        }
      }
      setGrids(array);
    };
    getMaze();
    // remove brackets if you want to loop request the server
  }, []);
  const setMaze = async (x, y) => {
    if (typeof cursor === "string") {
      if (cursor === "#42b132") {
        await fetch(`${apiLink}nest/${y.toString()}${x.toString()}`);
      } else {
        // handles toggle of grid by x and y
        const param = `?x=${x}&y=${y}&v=${cursor === "#C8EFF9" ? "0" : "1"}`;
        await fetch(`${apiLink}maze${param}`);
      }
    } else {
      const bolt = `bolt/${cursor}`;
      const param = `?x=${y}&y=${x}`;
      await fetch(`${apiLink}${bolt}/goto${param}`);
    }
  };
  React.useEffect(() => {
    const getBolts = async () => {
      const response = await fetch(apiLink + "bolt");
      const json = await response.json();
      setBolts(await json);

      let array = grids;
      if (bolts.length > 0) {
        bolts.map((element, index) => {
          // when goal is reached
          if (
            element.next_move.x * 10 + element.next_move.y ==
            element.position.x * 10 + element.position.y
          ) {
            if (
              array[element.next_move.x * 10 + element.next_move.y].util !=
              "#009ddb"
            ) {
              array[element.position.x * 10 + element.position.y].util =
                "#009ddb"; // overrides

              array.map((element) => {
                let util = "#fcd200" + bolts[index].id;
                console.log(util);
                if (element.util == "#fcd200" + bolts[index].id) {
                  // erases route of specific bolt
                  element.util = "#C8EFF9";
                }
              });
            }
          } else {
            // goal hasn't been reached
            if (
              array[element.next_move.x * 10 + element.next_move.y].util !=
              "#42b132"
            ) {
              array[element.next_move.x * 10 + element.next_move.y].util =
                "#42b132";
            }

            (async () => {
              let boltId = element.id;
              const response = await fetch(
                apiLink + "bolt/" + element.id + "/path"
              );
              const json = await response.json();
              if (await json.hasOwnProperty("path")) {
                json.path.map((element) => {
                  if (
                    array[element[0] * 10 + element[1]].util !=
                    "#fcd200" + boltId
                  ) {
                    array[element[0] * 10 + element[1]].util =
                      "#fcd200" + boltId;
                  }
                });
              }
            })();
          }
        });
        setGrids(array);
      }
    };

    if (grids != []) {
      getBolts();
    }
  }); // should work (json.map function is een onderkruipsel)
  return (
    <div className="app-container">
      {/* <link rel="stylesheet" href="static/stylesheet.css" /> */}
      <audio controls>
        <source
          src="https://vgmsite.com/soundtracks/super-mario-64-soundtrack/zqtpbfkskm/06%20Slider.mp3"
          type="audio/mpeg"
        />
      </audio>
      <div className="container">
        <div className="side-container">
          <ButtonView setCursor={setCursor} grids={grids} />
        </div>
        {grids !== [] ? (
          <GridView cursor={cursor} grids={grids} setMaze={setMaze} />
        ) : null}
        {bolts !== [] ? <BoltView setCursor={setCursor} bolts={bolts} /> : null}
      </div>
      <div className="title-view">
        <img
          src="https://fontmeme.com/permalink/211007/ee6670dba76f4367bd3d070b9a3cb143.png"
          alt="super-mario-lettertype"
        />
      </div>
    </div>
  );
};

export default App;
