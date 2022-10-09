
from typing import Dict, List
from core.base import get_current_time
from core.models.lobby.base import SlotType
from core.models.lobby.base import SlotStatus
from core.models.user import UserType, UserInfo

from serve.models.lobby.state import SlotState
from serve.models.lobby.state import LobbyState


REQUIRED_HEARTRATE = 5

SLOT_TYPE_ACCEPTS: Dict[SlotType, List[UserType]] = {
  SlotType.ANY: [
    UserType.ROBOT,
    UserType.HUMAN,
    UserType.LOCAL_BOT,
    UserType.ANONYMOUS,
  ],
  SlotType.ONLY_HUMAN: [UserType.HUMAN],
  SlotType.ONLY_BOT: [UserType.ROBOT],
};


def type_accepts(stype: SlotType, utype: UserType) -> bool:
  try:
    return utype in SLOT_TYPE_ACCEPTS[stype]
  except:
      raise Exception(f"Types not checked: {stype.name}, {utype.name}")






class SlotUtils:
  # def is_ready(slot: SlotState) -> bool:
  #   return self.status == SlotStatus.READY
  
  @staticmethod
  def receive_heartbeat(slot: SlotState, user: UserInfo) -> None:
    if slot.user is None or user.id != slot.user.id:
      # log warn
      raise Exception("User can not set heartbeat for this slot.")
    # log debug
    slot.last_heartbeat = get_current_time()
    
  @staticmethod
  def set_slot_type(slot: SlotState, type: SlotType) -> None:
    if self.status != SlotStatus.EMPTY:
            return False
        self.type = type
        return True
    
    def set_ready(self, ready: bool) -> bool:
        if ready and self.status == SlotStatus.NOT_READY:
            self.status = SlotStatus.READY
            return True
        if not ready and self.status == SlotStatus.READY:
            self.status = SlotStatus.NOT_READY
            return True
        return False
    
    def kick(self) -> bool:
        # TODO: Check if empty first
        self.status = SlotStatus.EMPTY
        self.user = None
        return True
    
    def can_accept(self, user: User) -> bool:
        return (
            self.status == SlotStatus.EMPTY and
            type_accepts(self.type, user.type)
        )
    
    def fill(self, user: User) -> None:
        self.status = SlotStatus.NOT_READY
        self.client = LobbyClient(user=user)
    
    def notify(self, updates: "LobbyUpdates") -> None:
        if self.client is not None:
            self.client.put_updates(updates)


class LobbyMutations:
  pass