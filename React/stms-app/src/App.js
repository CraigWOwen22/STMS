import React from 'react';

import './App.css';
import HomeScreen from './HomeScreen';
import LoginPage from './LoginPage';
import { useState } from "react";

function App() {
  
  const [token, setToken] = useState(null);

  

  
  return (


    <>
       {(token != null) ? <HomeScreen token = {token}/>: <LoginPage setToken={setToken}/>}
  </>
 
    
   
   
    
  );
}

export default App;
