import { layoutSize } from '..';
import Grid from './Grid';
import './GridView.css';

const GridView = props => {
    const changeGrid = item => {
        // calculate x and y based on grid position
        // x and y are flipped because api contains an error
        props.setMaze(
            props.grids[item].index % layoutSize,
            Math.floor(props.grids[item].index / layoutSize));
    };
    return (
        <div className='box-map'>
            <div className='grid-container'>
                {props.grids.map((element, index) => (
                    <Grid
                        item={element}
                        key={props.grids[index].index}
                        changeGrid={() => changeGrid(index)}
                        cursor={props.cursor}
                    />
                ))}
            </div>
        </div>
    );
};
export default GridView;
