import React from 'react';
import Tilt from 'react-tilt';
import NewEngineeringDkBlue from './NewEngineeringDkBlue.png';
// import './Logo.css';

const Logo = () => {
  return (
    <article class='center'>
	<div>
	  <Tilt className="Tilt" options={{ max : 40 }} style={{ height: 150, width: 450 }} >
	    <div className="Tilt-inner pa3">
	      <img style={{padding: '10px 5px 15px 10px'}} alt='logo' src={NewEngineeringDkBlue}/>
	    </div>
	  </Tilt>
	</div>
    </article>
  );
}

export default Logo;