import React, { useState } from 'react';
import axios from 'axios';
import './LoginPage.css';
import ErrorModal from './ErrorModal';

function LoginPage({ setToken }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [validationError, setValidationError] = useState({ username: '', password: '' });

  const validate = () => {
    let isValid = true;
    let errors = { username: '', password: '' };

    if (username.trim().length === 0) {
      errors.username = 'Username is required';
      isValid = false;
    } else if (username.trim().length < 5) {
      errors.username = 'Username must be at least 5 characters';
      isValid = false;
    } else if (username.trim().length > 15) {
      errors.username = 'Username must not exceed 15 characters';
      isValid = false;
    }

    if (password.trim().length === 0) {
      errors.password = 'Password is required';
      isValid = false;
    } else if (password.trim().length > 15) {
      errors.password = 'Password must not exceed 15 characters';
      isValid = false;
    }

    const passwordRegex = /^(?=.*[A-Z])/;
    if (password.trim().length < 6 || !passwordRegex.test(password)) {
      errors.password = 'Password must be at least 6 characters and contain one uppercase letter';
      isValid = false;
    }

    setValidationError(errors);
    return isValid;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!validate()) {
      return;
    }

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
    setValidationError({ username: '', password: '' });
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
          {validationError.username && (
            <div className="error">{validationError.username}</div>
          )}
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {validationError.password && (
            <div className="error">{validationError.password}</div>
          )}
        </div>
        <button type="submit" className="login-button">Login</button>
      </form>
      {error && <ErrorModal isOpen={!!error} onClose={handleCloseModal} message={error} />}
    </div>
  );
}

export default LoginPage;
