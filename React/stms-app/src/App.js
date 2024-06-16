import React from 'react';

import './App.css';
import HomeScreen from './HomeScreen';
import LoginPage from './LoginPage';
import { useState } from "react";


//On entry to the app, either home or login page will be show based on if there's a token.
function App() {
  
  const [token, setToken] = useState(null);

  return (
    <>
       {(token != null) ? <HomeScreen token = {token}/>: <LoginPage setToken={setToken}/>}
  </>
    
  );
}

export default App;
