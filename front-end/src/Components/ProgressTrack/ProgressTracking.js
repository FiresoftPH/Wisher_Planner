import pic1 from '../../Pictures/primogem.png'
import pic2 from '../../Pictures/genesis.png'
import pic3 from '../../Pictures/interwinedFate.png'
import './ProgressTrack.css'

export default function ProgressTracking({primo,genesis,interwined,handlePrimosChange,handleGenesisChange,handleInterwinedChange,handleSubmit}){
    return(
            <div className='yourplanner-progress-tracking'>
                <h1 className='yourplanner-body-header'>Progress Tracking</h1>
                <div className='yourplanner-body-input'>
                    <div className='yourplanner-input-container'>
                        <img className='yourplanner-pic' src={pic1}></img>
                        <p className='yourplanner-input-text'>How many primogem you have?</p>
                        <input
                            className='planner-input-boxes'
                            type="number"
                            id="primogems"
                            value={primo}
                            onChange={handlePrimosChange}
                        />
                    </div>
                    
                    <div className='yourplanner-input-container' >
                    <img className='yourplanner-pic' src={pic2}></img>
                    <p className='yourplanner-input-text'>How many Genesis crystals you have?</p>
                    <input
                            className='planner-input-boxes'
                            type="number"
                            id="Genesis"
                            value={genesis}
                            onChange={handleGenesisChange}
                        />
                    </div>
                    
                    <div className='yourplanner-input-container'>
                    <img className='yourplanner-pic' src={pic3}></img>
                    <p className='yourplanner-input-text'>How many Interwined crystals you have?</p>
                    <input
                            className='planner-input-boxes'
                            type="number"
                            id="Interwined"
                            value={interwined}
                            onChange={handleInterwinedChange}
                        />
                    </div>
                    <button className='planner-progress-button' onClick={handleSubmit}>Confirm</button>
                </div>
            </div>
    );

}