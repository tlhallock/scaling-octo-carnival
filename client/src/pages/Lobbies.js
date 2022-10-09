import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Navbar, Container, Row, Col, Alert, Button } from 'react-bootstrap';
import { FaUserCircle } from 'react-icons/fa';
import auth from '../auth/auth';
import NavigationBar from '../components/Header';
import lobbyApi from '../api/lobbies';
import TimeRep from '../components/TimeRep';


const getSlotColor = slotStatus => {
  switch (slotStatus) {
    case "EMPTY": return "green";
    case "NOT_READY": return "red";
    case "READY": return "yellow";
    case "CONNECTING": return "black";
    case "IN_GAME": return "black";
    default:
      throw Error(`status not recognized: ${slotStatus}`);
  }
}

const SlotSummary = ({slot}) => {
  return <div
    style={{
      height: "30px",
      width: "5px",
      backgroundColor: getSlotColor(slot.status),
      border: "2px solid black",
      margin: "2px"
    }}
  />
};

const SlotsSummary = ({slots}) => (
  <Row>
    {
      slots.map((slot, idx) => (
        <SlotSummary key={`slot-${idx}`} slot={slot} />
      ))
    }
  </Row>
);

const LobbySummary = ({lobby}) => (
  <Row>
  <Col className="mt-4">
    {lobby.label}
  </Col>
    <Col className="mt-4">
      {lobby.creator.username}
    </Col>
    <Col  className="mt-4">
      <TimeRep time={lobby.created}/>
    </Col>
    <Col className="mt-4">
      {lobby.game}
    </Col>
    {/* <Col className="mt-4">
      {lobby.num_spectators}
    </Col> */}
    <Col className="mt-4">
      {/* <Container> */}
        <SlotsSummary slots={lobby.slots} />
      {/* </Container> */}
    </Col>
    <Col className="mt-4">
      <Link to={`/lobby/${lobby.uuid}`}>Go</Link>
    </Col>
    <Col className="mt-4">
      <Button>-</Button>
    </Col>
  </Row>
)

const refreshLobbies = async setLobbies => {
  const lobbies = await lobbyApi.listLobbies();
  setLobbies(lobbies);
};


const Lobbies = props => {
  // History hook
  const navigate = useNavigate();
  const [lobbies, setLobbies] = useState([]);

  const createLobby = async () => {
    await lobbyApi.createLobby();
    await refreshLobbies(setLobbies);
  };
  useEffect(() => {
    refreshLobbies(setLobbies);
  }, [setLobbies]);

  return (
    <>
      <NavigationBar />
      <Container className="mt-4">
        <Row>
          <Col className="mt-4">
            <h2>Lobbies</h2>
          </Col>
          <Col className="mt-4">
            <Button
              onClick={createLobby}
            >
              +
            </Button>
          </Col>
        </Row>
        <Row>
          <Col className="mt-4">
            <Container>
              {
                lobbies.map((lobby, idx) => (
                  <LobbySummary
                    lobby={lobby}
                    index={`lobby-${idx}`}
                  />
                ))
              }
            </Container>
          </Col>
        </Row>
      </Container>
    </>
  );
};



export default Lobbies;
