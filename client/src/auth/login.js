import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Button, Alert } from 'react-bootstrap';
import auth from './auth';


const getLogin = (creds, navigate, setError) => async e => {
  // Prevents page reload on wrongs creds
  e.preventDefault();
  setError('');
  try {
    const data = await auth.login(creds);
    if (data) {
      navigate('/home', {replace: true});
    }
  } catch (err) {
    if (err instanceof Error) {
      // Handle errors thrown from frontend
      setError(err.message);
    } else {
      // Handle errors thrown from backend
      if (err === 'LOGIN_BAD_CREDENTIALS') {
        setError('Incorrect credentials');
      }
      else {
        setError('Error occured in the API.');
      }
    }
  }
};

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const login = getLogin({email, password}, navigate, setError);
  return (
    <>
      <h2>Login</h2>
      <Form onSubmit={login}>
        <Form.Group controlId="formLoginEmail">
          <Form.Label>Email</Form.Label>
          <Form.Control
            type="email"
            // type="username"
            placeholder="Enter email"
            value={email}
            onChange={(e) => setEmail(e.currentTarget.value)}
          />
        </Form.Group>
        <Form.Group controlId="formLoginPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(p) => setPassword(p.currentTarget.value)}
          />
        </Form.Group>
        <Alert
          variant='danger'
          style={ error!=='' ? {display:"block"} : {display:"none"}}
        >
          {error}
        </Alert>
        <Button variant="primary" type="submit" block="true">
          Log In
        </Button>
      </Form>
    </>
  );
};

export default Login;
