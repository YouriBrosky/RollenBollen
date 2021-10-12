import React from 'react';
import './Grid.css';

const Grid = props => {
    const [color, setColor] = React.useState(
        props.item.util.substring(0, 7)
    );
    React.useEffect(() => {
        setColor(props.item.util.substring(0, 7));
        // if color changes, re-render
    }, [props.item.util]);
    const onChangeGrid = () => {
        if (props.cursor !== color) {
            props.changeGrid();
        }
    };
    return (
        <div
            className='grid-item'
            style={{ backgroundColor: color }}
            onClick={() => {
                // this is needed
                setColor(props.cursor);
                onChangeGrid();
            }}
        >
            {props.item.index}
        </div>
    );
};
export default Grid;
