import React, { useState } from 'react';
import axios from "axios";
import './LoginPage.css';
import ErrorModal from './ErrorModal';


function LoginPage({setToken}) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);


  const handleSubmit = async (event) => {
    event.preventDefault();
    
    try {
      const response = await axios.post('http://localhost:8000/authentication/login', {
        username,
        password,
      });

      if (response.status === 200) {
        const { access_token } = response.data;
        setToken(access_token);
      } else {
        setError('Login failed. Please try again.');
      }
    } catch (error) {
      setError('Login failed. Please check your credentials and try again.');
    }
  };

  const handleCloseModal = () => {
    setError(null);
    setUsername('');  
    setPassword('');  
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit" className="login-button">Login</button>
      </form>
      {error && <ErrorModal isOpen={!!error} onClose={handleCloseModal} message={error} />}

    </div>
  );
}

export default LoginPage;
