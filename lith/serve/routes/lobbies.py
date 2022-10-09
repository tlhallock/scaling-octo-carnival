from typing import List, Optional
from fastapi import APIRouter
from core.models.lobby.info import LobbyInfo
from core.models.lobby.summary import LobbySummary
from core.models.user import UserInfo
from serve.models.lobby.export import LobbyPerspective, Summary
from serve.models.lobby.state import LobbyState
import serve.models.users as users_model
from pydantic import UUID4


from fastapi import Depends
import serve.routes.users as user_routes


from serve.store.lobbies import lobby_store

router = APIRouter()

@router.get(
  "/lobbies/",
  tags=["lobbies"],
  response_model=List[LobbySummary],
)
async def list_lobbies(skip: int = 0, limit: int = 20):
  user: Optional[users_model.User] = None
  lobbies = await lobby_store.list(skip=skip, limit=limit)
  return Summary.lobbies(lobbies=lobbies, user=user)

# @router.get("/lobbies/mine", tags=["lobbies"])
# async def my_lobbies():
#     return {"username": "fakecurrentuser"}


@router.get("/lobbies/{uuid}", response_model=LobbyInfo, tags=["lobbies"])
async def get_lobby(uuid: UUID4):
  user: Optional[users_model.User] = None
  lobby = await lobby_store.get(uuid=uuid)
  return LobbyPerspective.lobby(lobby=lobby, user=user)


@router.post("/lobbies/", response_model=str, tags=["lobbies"])
async def create_lobby(
    user: users_model.User = Depends(user_routes.get_current_user)
):
  print("creator", user)
  uuid = await lobby_store.create(
    LobbyState(
      creator=UserInfo(
        uuid=str(user.id),
        user_type=user.user_type,
        username=user.username
      )
    )
  )
  return str(uuid)


@router.delete("/lobbies/{id}", response_model=bool, tags=["lobbies"])
async def delete_lobby(id: UUID4):
  user: Optional[users_model.User] = None
  lobbies = lobby_store.delete(id)
  return Summary.lobbies(lobbies=lobbies, user=user)

# async def join_lobby():
#   pass


# async def join_lobby():
#   pass
