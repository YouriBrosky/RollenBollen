import './BoltViewCard.css';

const BoltViewCard = props => (
    <div
        key={props.id}
        className='bolt'
        style={{ backgroundColor: '#009ddb' }}
        onClick={() => {
            props.setCursor(props.id);
        }}
    >
        <h3>
            ID: {props.id}, POS:
            {props.position.x.toString() + props.position.y.toString()}
        </h3>
    </div>
);
export default BoltViewCard;
