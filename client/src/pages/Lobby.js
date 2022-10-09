
// import { lobby_client, } from "./apollo_clients";
import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";

// import { SubscriptionServer } from 'subscriptions-transport-ws';
import { Link, useParams } from 'react-router-dom';
import _ from 'lodash';
import TimeRep from '../components/TimeRep';
import { Navbar, Container, Row, Col, Alert, Button } from 'react-bootstrap';

// import { graphql,  } from 'react-apollo';
import NavigationBar from '../components/Header';

import lobbyApi from '../api/lobbies';

// TODO: Leave on navigate away
// const SlotStatus = ({isCurrentUser, status, setReady}) => {
//     if (status === "EMPTY") {
//         return <div/>
//     }
//     return <span>
//         <input
//             type="checkbox"
//             readOnly
//             checked={isChecked(status)}
//             onClick={getStatusCallback(isCurrentUser, status, setReady)} />
//     </span>;
// };


// const Slot = props => {
//     return (<>
//         <label>{props.idx + 1}</label>
//         <span>
//             <select 
//                 value={props.type}
//                 disabled={props.status !== "EMPTY"}
//                 readOnly
//                 onChange={args => props.setSlotType(args.target.value)}
//             >
//                 <option value="ANY">auto</option>
//                 <option value="ONLY_BOT">bot</option>
//                 <option value="ONLY_HUMAN">human</option>
//             </select>
//         </span>
//     </>);
// };



































const SlotType = ({slotType}) => {
  const setSlotType = () => {};
  return (
    <select 
      value={slotType}
      // disabled={slotType !== "EMPTY"}
      onChange={setSlotType}
    >
      <option value="ANY">auto</option>
      <option value="ONLY_BOT">bot</option>
      <option value="ONLY_HUMAN">human</option>
    </select>
  );
};








const Slot = ({lobbyUuid, slot, index}) => {
  console.log("slot", slot);

  const kick = () => {};
  const remove = () => {};
  const setSlotType = () => {};

  // <span><button onClick={props.fill}>Fill</button></span>
  // <span><button>Reset</button></span>

  return (
    <Row>
      <Col>{index + 1}</Col>
      <Col><SlotType slotType={slot.slot_type}/></Col>

      {/* <SlotStatus 
            isCurrentUser={props.isCurrentUser}
            status={props.status}
            setReady={props.setReady} /> */}
      <Col>Status</Col>
      <Col>{_.get(slot, "user.username", "empty")}</Col>
      <Col><TimeRep time={_.get(slot, "last_heartbeat", 0)} /></Col>
      
      <Col>
        <Button onClick={kick}>kick</Button>
        <Button onClick={remove}>-</Button>
      </Col>
    </Row>
  );
};



const Slots = ({lobbyUuid, slots}) => {
  const addSlot = async () => {};
  return (<>
    <Row>
      <Col>Slot</Col>
      <Col>Type</Col>
      <Col>Status</Col>
      <Col>User</Col>
      <Col>Health</Col>
      <Col><Button onClick={addSlot}>+</Button></Col>
    </Row>
    {
      slots.map((slot, idx) => (
        <Slot
          key={`slot-${slot.uuid}`}
          lobbyUuid={lobbyUuid}
          slot={slot}
          index={idx}
        />
      ))
    }
  </>);
};









const fetchLobby = async (lobbyUuid, setLobby) => {
  const lobby = await lobbyApi.get(lobbyUuid);
  setLobby(lobby);
};

const getSubscriptionHandler = (navigate, setLobby) => arg => {
  console.log("arg", arg);
};


const INITIAL_LOBBY = {
  inLobby: false,
  deletable: false,
  slots: [],
};


const Lobby = props => {
  const params = useParams();
  const navigate = useNavigate();
  const [lobby, setLobby] = useState(INITIAL_LOBBY);


  const lobbyUuid = params.uuid;
  useEffect(() => {
    fetchLobby(lobbyUuid, setLobby);
  }, [setLobby]);

  console.log("lobby", lobby);

    // TODO: No longer needed...
    // const [gameUuid, setGameUuid] = useState(null);
    // useEffect(() => {
    //     if (!creds) {
    //         return;
    //     }
    //     const subscription = lobby_client.subscribe({
    //         query: LOBBY_UPDATES,
    //         variables: {
    //             creds, lobbyUuid,
    //         }
    //     }).subscribe({
    //         next(data) {
    //             const updateType = _.get(data, 'data.lobbyUpdates.updateType');
    //             console.log('update type', updateType)
    //             switch (updateType) {
    //                 case "STATE_CHANGED":
    //                     refetchLobby();
    //                     return;
    //                 case "LAUNCHED":
    //                     console.log("data", data)
    //                     const game_uuid = _.get(data, 'data.lobbyUpdates.launch.gameUuid')
    //                     // console.log("game uuid", game_uuid)
    //                     // setGameUuid(game_uuid)
    //                     navigate("game/${game_uuid}")
    //                     return;
    //                 // ignore...
    //                 case "REQUEST_HEARTBEAT":
    //                 case "KICKED":
    //                 default:
    //                     return;
    //             }
    //         },
    //         complete() {
    //             console.log('complete');
    //         },
    //         error(err) {
    //             console.log('error', err);
    //         }
    //     });
    //     return () => subscription.unsubscribe();
    //   }, [creds, lobbyUuid, refetchLobby, navigate]);

    // const {sendHeartbeat} = props;
    // useEffect(() => {
    //     const interval = setInterval(() => {
    //         if (!hasUser) {
    //             return;
    //         }
    //         sendHeartbeat();
    //     }, 5000);
    //     return () => clearInterval(interval);
    //   }, [sendHeartbeat, hasUser]);

  const leave = async () => {};
  const join = async () => {};
  const launch = async () => {};
  const imReady = async () => {};
  const deleteLobby = async () => {};
  return (
    <>
      <NavigationBar/>
      <Container className="mt-4">
        <Row>
          <Col>
            <Link to={"/lobbies"}>Back to lobbies</Link>
          </Col>
          <Col>
            <Button disabled={!lobby.inLobby} onClick={leave}>Leave</Button>
            <Button disabled={!!lobby.inLobby} onClick={join}>Join</Button>
            <Button disabled={!lobby.deletable} onClick={deleteLobby}>Delete</Button>
          </Col>
        </Row>
        <Row>
          <Col>
            <label>Lobby:</label>
            <label>{ _.get(lobby, 'label', 'no lobby found')}</label>
          </Col>
          <Col>
            <label>Created:</label>
            <TimeRep time={_.get(lobby, 'created', 0.0)} />
          </Col>
          <Col>
            <label>Creator:</label>
            <label>{_.get(lobby, 'creator.username', "unknown")}</label>
          </Col>
        </Row>
        <Row>
          <Col>
            <label>Ready:</label>
            <label>{_.get(lobby, 'ready', false) ? "Yes" : "No"}</label>
          </Col>
          <Col>
              <Button disabled={!lobby.present} onClick={imReady}>Ready Up</Button>
          </Col>
          <Col>
            <Button 
              disabled={!_.get(lobby, "ready", false)} 
              onClick={launch}
            >
              Launch!
          </Button>
          </Col>
        </Row>
        <Slots lobbyUuid={lobbyUuid} slots={lobby.slots}/>
      </Container>
    </>
  );
};


export default Lobby;
