import React, { Component } from 'react';
import Navigation from './components/Navigation/Navigation';
// import Signin from './components/Signin/Signin';
// import Register from './components/Register/Register';
import Logo from './components/Logo/Logo';
import ImageLinkForm from './components/ImageLinkForm/ImageLinkForm';
// import Rank from './components/Rank/Rank';
import './App.css';

//You must add your own API key here from Clarifai.
// const app = new Clarifai.App({
//  apiKey: 'YOUR_API_HERE'
// });


class App extends Component {
  render() {
    return (
      <div className="App">
        <Navigation />
        <Logo />  
        <ImageLinkForm />
      </div>
      )
  }
}
export default App;
