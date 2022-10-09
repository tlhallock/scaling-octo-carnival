import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import Home from './pages/Home';
import auth from './auth/auth';
import Lobbies from './pages/Lobbies';
import Lobby from './pages/Lobby';
import Landing from './pages/Landing';
import { Redirect } from 'react-router-dom';
import './App.css';

const App = () => {
  const authenticated = auth.isAuthenticated();
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          <Route path='/' exact strict element={
                authenticated ? 
                <Navigate to="/home" /> :
                <Navigate to="/login" />
          }/>
          <Route path='/home' exact strict element={<Home/>}/>
          <Route path='/login' exact strict element={<Landing/>}/>
          <Route path='/lobbies' exact strict element={<Lobbies/>}/>
          <Route path="/lobby/:uuid" exact strict element={<Lobby/>} />
       </Routes>
     </div>
    </BrowserRouter>
  )
};
export default App;
