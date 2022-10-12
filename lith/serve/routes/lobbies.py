from typing import List, Optional
from fastapi import APIRouter
from core.models.lobby.info import LobbyInfo
from core.models.lobby.summary import LobbySummary
from core.models.user import UserInfo
from serve.models.lobby.export import LobbyPermissions, LobbyPerspective, Summary
from serve.models.lobby.state import LobbyState
import serve.models.users as users_model
from pydantic import UUID4

from serve.models.lobby.utils import SlotUtils

from fastapi import Depends
import serve.routes.users as user_routes


from serve.store.lobbies import lobby_store

router = APIRouter()

@router.get(
  "/lobbies/",
  tags=["lobbies"],
  response_model=List[LobbySummary],
)
async def list_lobbies(
  user: Optional[users_model.User] = Depends(user_routes.get_optional_current_user),
  skip: int = 0,
  limit: int = 20,
):
  user: Optional[users_model.User] = None
  lobbies = await lobby_store.list(skip=skip, limit=limit)
  return Summary.lobbies(lobbies=lobbies, user=user)

# @router.get("/lobbies/mine", tags=["lobbies"])
# async def my_lobbies():
#     return {"username": "fakecurrentuser"}


@router.get("/lobbies/{uuid}", response_model=LobbyInfo, tags=["lobbies"])
async def get_lobby(
  uuid: UUID4,
  user: Optional[users_model.User] = Depends(user_routes.get_optional_current_user),
):
  lobby = await lobby_store.get(uuid=uuid)
  return LobbyPerspective.lobby(lobby=lobby, user=user)


@router.post("/lobbies/", response_model=str, tags=["lobbies"])
async def create_lobby(
  user: users_model.User = Depends(user_routes.get_current_user)
):
  uuid = await lobby_store.create(
    LobbyState(
      creator=users_model.export_user(user),
    )
  )
  return str(uuid)


@router.delete("/lobbies/{uuid}", response_model=bool, tags=["lobbies"])
async def delete_lobby(
  uuid: UUID4,
  user: users_model.User = Depends(user_routes.get_current_user),
):
  lobby = await lobby_store.get(uuid=uuid)
  can_delete = LobbyPermissions.user_can_edit_lobby(user=user, lobby=lobby)
  if not can_delete:
    return False
  success = lobby_store.delete(id)
  return success

# async def join_lobby():
#   pass


# async def join_lobby():
#   pass


@router.post(
  "/lobbies/{uuid}/slots/{slot_uuid}",
  response_model=Optional[str], tags=["lobbies"]
)
async def heartbeat(
  uuid: UUID4,
  slot_uuid: UUID4,
  user: users_model.User = Depends(user_routes.get_current_user),
):
  lobby = await lobby_store.get(uuid=uuid)
  # users_model.export_user
  SlotUtils.join(user=user, lobby=lobby, slot_uuid=slot_uuid)
  await lobby_store.update(lobby)
  return slot_uuid

@router.delete("/lobbies/{uuid}/slots/{slot_uuid}", response_model=bool, tags=["lobbies"])
async def heartbeat(
  uuid: UUID4,
  slot_uuid: UUID4,
  user: users_model.User = Depends(user_routes.get_current_user),
):
  lobby = await lobby_store.get(uuid=uuid)
  # users_model.export_user
  SlotUtils.leave(user=user, lobby=lobby, slot_uuid=slot_uuid)
  await lobby_store.update(lobby)
  return slot_uuid


# @router.post("/lobbies/{uuid}/heartbeat", response_model=bool, tags=["lobbies"])
# async def heartbeat(
#   uuid: UUID4,
#   slot_uuid: UUID4,
#   user: users_model.User = Depends(user_routes.get_current_user),
# ):
#   pass


  
    # def is_ready(self) -> bool:
    #     return self.status == SlotStatus.READY
    
    # def heartbeat(self, user: UserInfo) -> None:
    #   if self.user is None or user.id != self.user.id:
    #     raise Exception("User can not set heartbeat for this slot.")
    #   self.last_heartbeat = get_current_time()
    
    # def set_slot_type(self, type: SlotType) -> None:
    #     if self.status != SlotStatus.EMPTY:
    #         return False
    #     self.type = type
    #     return True
    
    # def set_ready(self, ready: bool) -> bool:
    #     if ready and self.status == SlotStatus.NOT_READY:
    #         self.status = SlotStatus.READY
    #         return True
    #     if not ready and self.status == SlotStatus.READY:
    #         self.status = SlotStatus.NOT_READY
    #         return True
    #     return False
    
    # def kick(self) -> bool:
    #     # TODO: Check if empty first
    #     self.status = SlotStatus.EMPTY
    #     self.user = None
    #     return True
    
    # def can_accept(self, user: User) -> bool:
    #     return (
    #         self.status == SlotStatus.EMPTY and
    #         type_accepts(self.type, user.type)
    #     )
    
    # def fill(self, user: User) -> None:
    #     self.status = SlotStatus.NOT_READY
    #     self.client = LobbyClient(user=user)
    
    # def notify(self, updates: "LobbyUpdates") -> None:
    #     if self.client is not None:
    #         self.client.put_updates(updates)


    
    # # TODO: Is there a better way
    # # lobby_state: LobbyState = LobbyState.EMPTY
    # def is_ready(self):
    #     return all(
    #         slot.is_ready() 
    #         for slot in self.slots)
    
    # def validate_heartrates(self) -> bool:
    #     # TODO: Update the state, so that in the ui we can disable the launch button.
    #     ctime = get_current_time()
    #     for slot in self.slots:
    #         if slot.client is None:
    #             continue
    #         if slot.status != SlotStatus.READY:
    #             continue
    #         if (slot.last_heartbeat is None or 
    #             slot.last_heartbeat < ctime - REQUIRED_HEARTRATE):
    #             pass
    #             # logging.getLogger(__name__).debug(
    #             #     f"Would have set slot status to not ready: {ctime - REQUIRED_HEARTRATE}")
    #             # slot.status = SlotStatus.NOT_READY
    #     return True
    
    # def update_ready(self):
    #     self.validate_heartrates()
    #     self.ready = self.is_ready()
    
    # def get_status(self) -> LobbyStatus:
    #     if all(
    #         slot.status == SlotStatus.EMPTY
    #         for slot in self.slots):
    #         return LobbyStatus.EMPTY
    #     if all(
    #         slot.is_ready()
    #         for slot in self.slots):
    #         return LobbyStatus.READY
    #     return LobbyStatus.WAITING
    
    # def add_slot(self) -> bool:
    #     self.slots.append(SlotState())
    #     self.update_ready()
    #     return True
    
    # def remove_slot(self, idx: int) -> bool:
    #     if idx < 0 or idx >= len(self.slots):
    #         return False
    #     del self.slots[idx]
    #     self.update_ready()
    #     return True
    
    # def set_slot_type(self, idx: int, type: SlotType) -> bool:
    #     if idx < 0 or idx >= len(self.slots):
    #         return False
    #     ret = self.slots[idx].set_slot_type(type)
    #     self.update_ready()
    #     return ret
    
    # def set_ready(self, idx: int, ready: bool) -> bool:
    #     if idx < 0 or idx >= len(self.slots):
    #         return False
    #     ret = self.slots[idx].set_ready(ready)
    #     self.update_ready()
    #     return ret
        
    # def add_user(self, user: User) -> bool:
    #     for slot in self.slots:
    #         if slot.can_accept(user):
    #             slot.fill(user)
    #             self.update_ready()
    #             return True
    #     return False
    
    # def kick(self, idx: int) -> bool:
    #     if idx < 0 or idx >= len(self.slots):
    #         return False
    #     ret = self.slots[idx].kick()
    #     self.update_ready()
    #     return ret
    
    # def heartbeat(self, user: User) -> bool:
    #     idx = self.get_idx(user)
    #     if idx is None:
    #         return False
    #     ret = self.slots[idx].heartbeat(user)
    #     self.update_ready()
    #     return ret
    
    # def get_idx(self, user: User) -> Optional[int]:
    #     for idx, slot in enumerate(self.slots):
    #         if slot.client is not None and slot.client.user.uuid == user.uuid:
    #             return idx
    #     return None
    
    # def notify_all(self, updates: "LobbyUpdates" = None) -> None:
    #     if updates is None:
    #         logging.getLogger(__name__).warn("Missing updates.")
    #         return
    #         # updates = LobbyUpdates(
    #         #     update_type=LobbyUpdateType.STATE_CHANGED,
    #         #     state=self.state,
    #         #     launch=None,
    #         # )
    #     # TODO: throttle these...
    #     for spec in self.spectators:
    #         spec.put_updates(updates)
    #     for slot in self.slots:
    #         slot.notify(updates)
    
    # # async def create_config(self, user: User) -> GameConfig:
    # #     # TODO: Should just use the full user...
    # #     return GameConfig(
    # #         player_names=[
    # #             slot.user.name
    # #             for slot in self.slots
    # #         ])
