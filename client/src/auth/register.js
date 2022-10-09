import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Button, Alert } from 'react-bootstrap';
import auth from './auth';


const ERROR_STYLE = {
  display:"block"
};

const NO_ERROR_STYLE = {
  display:"none"
};


const getRegister = (navigate, setError, creds) => async e => {
  // Prevents page reload on wrongs creds
  e.preventDefault();
  setError('');
  try {
    const data = await auth.register(creds);
    if (data) {
      await auth.login(creds);
      alert('Registration Successful!');
      navigate('/home', {replace: true});
    }
  } catch (err) {
    if (err instanceof Error) {
      setError(err.message);
      return;
    } 

    if (err === 'REGISTER_USER_ALREADY_EXISTS') {
      setError('Username is already registered. Please use your credentials to login.');
      return;
    }

    setError('Error occured in the API.');
  }
};

const randomString = n => Array(n)
  .fill(null)
  .map(() => Math.random()*100%25 + 'a'.charCodeAt(0))
  .map(a => String.fromCharCode(a))
  .join('');


const Register = () => {
  const navigate = useNavigate();


  

  const [email, setEmail] = useState(
    randomString(5) + '@' + randomString(5) + '.com');
  const [username, setUsername] = useState(randomString(10));
  const [password, setPassword] = useState('a');
  const [passwordConfirmation, setPasswordConfirmation] = useState('a');
  const [error, setError] = useState('');

  const creds = {email, username, password, passwordConfirmation};
  const register = getRegister(navigate, setError, creds);
  return (
    <>
      <h2>Register</h2>
      <Form onSubmit={register}>
        <Form.Group controlId="formRegisterEmail">
          <Form.Label>Email</Form.Label>
          <Form.Control
            type="email"
            placeholder="Enter an email"
            value={email}
            onChange={e => setEmail(e.currentTarget.value)}
          />
        </Form.Group>
        <Form.Group controlId="formRegisterUsername">
          <Form.Label>Username</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter a username"
            value={username}
            onChange={e => setUsername(e.currentTarget.value)}
          />
        </Form.Group>
        <Form.Group controlId="formRegisterPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={e => setPassword(e.currentTarget.value)}
          />
        </Form.Group>
        <Form.Group controlId="formRegisterPasswordConfirmation">
          <Form.Label>Confirm Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Confirm password"
            value={passwordConfirmation}
            onChange={e => setPasswordConfirmation(e.currentTarget.value)}
          />
        </Form.Group>
        <Alert
          variant='danger'
          style={error !== '' ? ERROR_STYLE : NO_ERROR_STYLE}
        >
          {error}
        </Alert>
        <Button variant="primary" type="submit" block="true">
          Register
        </Button>
      </Form>
    </>
  );
};

export default Register;
