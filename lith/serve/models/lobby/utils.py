
from typing import Dict, List
from core.base import get_current_time
from core.models.lobby.base import SlotType
from core.models.lobby.base import SlotStatus
from core.models.user import UserType, UserInfo

from serve.models.lobby.state import SlotState
from serve.models.lobby.state import LobbyState

from pydantic import UUID4

import serve.models.users as users_model

from serve.models.lobby.export import LobbyUtils

import structlog


REQUIRED_HEARTRATE = 5



LOGGER = structlog.get_logger("mutations")



class SlotUtils:

  @classmethod
  def get_slot(cls, lobby: LobbyState, slot_uuid: UUID4) -> SlotState:
    for slot in lobby.slots:
      # TODO: str(x) needed?
      if str(slot.uuid) == str(slot_uuid):
        return slot
    return None


  @classmethod  
  def join(cls, user: users_model.User, lobby: LobbyState, slot_uuid: UUID4) -> None:
    slot = cls.get_slot(lobby=lobby, slot_uuid=slot_uuid)
    if not LobbyUtils.user_can_join_slot(user=user, lobby=lobby, slot=slot):
      # Log
      raise Exception("Cannot join slot.")
    slot.status = SlotStatus.NOT_READY
    slot.user = users_model.export_user(user)
    slot.last_heartbeat = get_current_time()
    
    LOGGER.info(
        "User joined slot",
        user=str(user.uuid),
        lobby=str(lobby.uuid),
        slot=str(slot_uuid),
    )
    
  @classmethod  
  def leave(cls, user: users_model.User, lobby: LobbyState, slot_uuid: UUID4) -> None:
    slot = cls.get_slot(lobby=lobby, slot_uuid=slot_uuid)
    if not LobbyUtils.user_in_slot(user=user, lobby=lobby, slot=slot):
      # Log
      raise Exception("Cannot join slot.")
    slot.status = SlotStatus.EMPTY
    slot.user = None
    slot.last_heartbeat = None
    
    LOGGER.info(
        "User left slot",
        user=str(user.uuid),
        lobby=str(lobby.uuid),
        slot=str(slot_uuid),
    )
  
  
  # def is_ready(slot: SlotState) -> bool:
  #   return self.status == SlotStatus.READY
  
#   @staticmethod
#   def receive_heartbeat(slot: SlotState, user: UserInfo) -> None:
#     if slot.user is None or user.id != slot.user.id:
#       # log warn
#       raise Exception("User can not set heartbeat for this slot.")
#     # log debug
#     slot.last_heartbeat = get_current_time()
    
#   @staticmethod
#   def set_slot_type(slot: SlotState, type: SlotType) -> None:
#     if self.status != SlotStatus.EMPTY:
#             return False
#         self.type = type
#         return True
    
#     def set_ready(self, ready: bool) -> bool:
#         if ready and self.status == SlotStatus.NOT_READY:
#             self.status = SlotStatus.READY
#             return True
#         if not ready and self.status == SlotStatus.READY:
#             self.status = SlotStatus.NOT_READY
#             return True
#         return False
    
#     def kick(self) -> bool:
#         # TODO: Check if empty first
#         self.status = SlotStatus.EMPTY
#         self.user = None
#         return True
    
#     def can_accept(self, user: User) -> bool:
#         return (
#             self.status == SlotStatus.EMPTY and
#             type_accepts(self.type, user.type)
#         )
    
#     def fill(self, user: User) -> None:
#         self.status = SlotStatus.NOT_READY
#         self.client = LobbyClient(user=user)
    
#     def notify(self, updates: "LobbyUpdates") -> None:
#         if self.client is not None:
#             self.client.put_updates(updates)

