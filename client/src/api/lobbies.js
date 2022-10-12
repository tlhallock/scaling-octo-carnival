


const baseUrl = 'http://localhost:8081';



class LobbyApi {

  get = async (lobbyUuid) => {
    const token = localStorage.getItem('token');
    const request = new Request(baseUrl + '/lobbies/' + lobbyUuid, {
      method: 'GET',
      headers: {'Authorization': `Bearer ${token}`}
    });
    const response = await fetch(request);
    const data = await response.json();
    return data;
  }

  listLobbies = async () => {
    const token = localStorage.getItem('token');
    const request = new Request(baseUrl + '/lobbies/', {
      method: 'GET',
      headers: {'Authorization': `Bearer ${token}`}
    });
    const response = await fetch(request);
    const data = await response.json();
    return data;
  }

  createLobby = async () => {
    const token = localStorage.getItem('token');
    const request = new Request(baseUrl + '/lobbies/', {
      method: 'POST',
      headers: {'Authorization': `Bearer ${token}`}
    });
    const response = await fetch(request);
    const data = await response.json();
    console.log("created lobby", data);
    return data;
  }

  joinLobby = async (lobbyUuid, slotUuid) => {
    const token = localStorage.getItem('token');
    const request = new Request(
      baseUrl + '/lobbies/' + lobbyUuid,
      {
        method: 'POST',
        headers: {'Authorization': `Bearer ${token}`},
        body: JSON.stringify({
          
        }),
      }
    );
    const response = await fetch(request);
    const data = await response.json();
    console.log("created lobby", data);
    return data;
  }

};


export default new LobbyApi();
