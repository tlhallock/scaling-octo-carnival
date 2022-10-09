import React from 'react';
import { Navbar, Container, Row, Col, Alert } from 'react-bootstrap';
import Login from '../auth/login';
import Register from '../auth/register';
import NavigationBar from '../components/Header';

const Landing = (props) => (
  <>
    <NavigationBar/>
    <Container className="mt-4">
      <Row>
        <Col className="mt-4">
          <h2>Hello!</h2>
          <Alert variant={'primary'}>
            If you have the FastAPI backend and MongoDB running, then just create a new user account using the registration form and enter the web application.
          </Alert>
        </Col>
      </Row>
      <Row>
        <Col lg={6} md={6} sm={12} className="mt-4">
          <Login {...props}/>
        </Col>
        <Col lg={6} md={6} sm={12} className="mt-4">
          <Register {...props}/>
        </Col>
      </Row>
    </Container>
  </>
);

export default Landing;
