import BoltViewCard from './BoltViewCard';
import './BoltView.css';

const BoltView = props => {
    return (
        <div className='bolt-div' onClick={props.onClick}>
            {props.bolts.map(element => (
                <BoltViewCard
                    key={element.id}
                    id={element.id}
                    position={element.position}
                    setCursor={props.setCursor}
                />
            ))}
        </div>
    );
};
export default BoltView;
