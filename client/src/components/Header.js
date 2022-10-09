import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Navbar, Container, Row, Col, Alert, Button } from 'react-bootstrap';
import { FaUserCircle } from 'react-icons/fa';
import auth from '../auth/auth';


const getUser = setUser => () => {
  const fetch = async () => {
    if (auth.isAuthenticated()){
      const result = await auth.getUser();
      setUser(result);
    } else {
      console.log("Not logged in...")
    };
  };
  fetch();
};

const getLogout = navigate => () => {
    auth.logout();
    navigate('/login', {replace: true});
};

const INITIAL_USER = {
    "id": "",
    "email": "",
    "is_active": true,
    "is_superuser": false,
};

const NavigationBar = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(INITIAL_USER);
  // Currently, this calls getUser more than it has to.
  useEffect(getUser(setUser), [setUser]);
  const logout = getLogout(navigate);
  return (
      <Navbar className="align-middle justify-content-between" bg="dark" variant="dark">
        <div>
          <Navbar.Brand href="/">
            {/* <img
              alt=""
              src={require("../images/logo.svg")}
              width="40" height="40"
              className="d-inline-block align-top"
            /> */}
            <Navbar.Brand><strong>Project</strong></Navbar.Brand>
          </Navbar.Brand>
        </div>
        <div>
          <label className="ml-4 text-white" style={{}}><FaUserCircle size={21}/></label>
          <label className="ml-4 text-white">{user.username}</label>
          <Button className="ml-4" variant="outline-light" onClick={logout}>Log Out</Button>
        </div>
      </Navbar>
  );
};


export default NavigationBar;
