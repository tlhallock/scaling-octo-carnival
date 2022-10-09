import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { Navbar, Container, Row, Col, Alert, Button } from 'react-bootstrap';
import { FaUserCircle } from 'react-icons/fa';
import auth from '../auth/auth';
import NavigationBar from "../components/Header"

const Home = props => {
  // History hook
  const navigate = useNavigate();
  console.log(auth.isAuthenticated());
  if (!auth.isAuthenticated()) {
    return (<>
      Please <Link to="/login">log in.</Link>
    </>);
  }
  return (
    <>
      <NavigationBar />
      <Container className="mt-4">
        <Row>
          <Col className="mt-4">
            <h2>Welcome!</h2>
            <Alert variant={'primary'}>You have been successfully authenticated.</Alert>
            Please join one of our fabulous <Link to="/lobbies">lobbies</Link>.
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default Home;
