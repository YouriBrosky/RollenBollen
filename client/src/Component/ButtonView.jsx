import { apiLink } from '..';
import './ButtonView.css';

const ButtonView = props => {
    const onReset = async () => {
        const eraseBoltsFromGrid = boltsInGrid => {
            boltsInGrid.map((element, index) => {
                if (element.util === '#009ddb') {
                    boltsInGrid[index].util = '#C8EFF9';
                }
            });
        };
        fetch(`${apiLink}reset`);
        const array = props.grids;
        setTimeout(() => {
            // erase bolts after 0.1s
            eraseBoltsFromGrid(array);
        }, 100);
        // check if all bolts are really reset
        setTimeout(() => {
            eraseBoltsFromGrid(array);
        }, 5000);
    };
    return (
        <div className='panel'>
            <div
                className='button'
                style={{ backgroundColor: '#C8EFF9' }}
                onClick={() => props.setCursor('#C8EFF9')}
            >
                <h2 style={{ color: 'grey' }}>Beschikbaar</h2>
            </div>
            <div
                className='button'
                style={{ backgroundColor: '#e71d07' }}
                onClick={() => props.setCursor('#e71d07')}
            >
                <h2>Obstakel</h2>
            </div>

            <div
                className='button'
                style={{ backgroundColor: '#42b132' }}
                onClick={() => props.setCursor('#42b132')}>
                <h2>Doel</h2>
            </div>
            <div
                className='button'
                style={{ backgroundColor: '#fc9803' }}
                onClick={() => onReset()}
            >
                <h2>Reset BOLTs</h2>
            </div>
            <div
                className='button'
                style={{ backgroundColor: '#b103fc' }}
                onClick={() => {
                    // sends all connected BOLTs home
                    fetch(`${apiLink}home`);
                }}
            >
                <h2>Thuisfront</h2>
            </div>
            
            {/* a seperator */}
            <div style={{width: 230, height: 1, backgroundColor: '#cfcfcf', marginBottom: 10}}/>

            <div className='button' style={{ backgroundColor: '#fcd200' }}>
                <h2>Route</h2>
            </div>
            <div className='button' style={{ backgroundColor: '#009ddb', marginBottom: 0 }}>
                <h2>Positie</h2>
            </div>
        </div>
    );
};
export default ButtonView;
