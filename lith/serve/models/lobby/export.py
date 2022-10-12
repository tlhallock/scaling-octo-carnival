
from typing import List, Optional
from core.models.lobby.info import LobbyInfo, LobbyPermissions, SlotInfo, SlotPermissions
from core.models.lobby.summary import LobbySummary, SlotSummary
from core.models.user import UserInfo
from serve.models.lobby.state import LobbyState, SlotState
from serve.models.users import User

from typing import Dict, List
from core.base import get_current_time
from core.models.lobby.base import SlotType
from core.models.lobby.base import SlotStatus
from core.models.user import UserType, UserInfo

from serve.models.lobby.state import SlotState
from serve.models.lobby.state import LobbyState


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


class LobbyUtils:
  @classmethod
  def user_is_superuser(cls, user: Optional[User]) -> bool:
    return user is not None and user.is_superuser
  
  @classmethod
  def user_is(cls, user: Optional[User], user_info: Optional[UserInfo]) -> bool:
    return (
      user is not None and
      user_info is not None and 
      user.uuid == user_info.uuid
    )
    
  @classmethod
  def slot_type_accepts_user_type(slot_type: SlotType, user_type: UserType) -> bool:
    try:
      return user_type in SLOT_TYPE_ACCEPTS[slot_type]
    except:
      raise Exception(f"Types not implemented: {slot_type.name}, {user_type.name}")
    
  @classmethod
  def user_can_join_slot(cls, user: Optional[User], lobby: LobbyState, slot: SlotState) -> bool:
    if user is None:
      return False
    if slot.status != SlotStatus.EMPTY:
      return False
    if slot.user is not None:
      raise Exception("This is an illegal state.")
    if not cls.slot_type_accepts_user_type(user.user_type, slot.slot_type):
      return False
    # The user is already present
    if cls.user_is_present(user=user, lobby=lobby):
      return False
    return True
    
  # Rename
  @classmethod
  def user_can_join_lobby(cls, user: Optional[User], lobby: LobbyState) -> bool:
    return any(
      cls.user_can_join_slot(user=user, lobby=lobby, slot=slot)
      for slot in lobby.slots
    ) and not cls.user_is_present(user=user, lobby=lobby)
    
  @classmethod
  def user_in_slot(cls, user: Optional[User], slot: SlotState) -> bool:
    return cls.user_is(user, slot.user)
    
  @classmethod
  def user_is_present(cls, user: Optional[User], lobby: LobbyState) -> bool:
    return any(cls.user_in_slot(user, slot) for slot in lobby.slots)
  
  @classmethod
  def user_can_edit_lobby(cls, user: Optional[User], lobby: LobbyState) -> bool:
    return cls.user_is_superuser(user) or cls.user_is(user, lobby.creator)
  
  @classmethod
  def user_can_kick_slot(cls, user: Optional[User], lobby: LobbyState, slot: SlotInfo) -> bool:
    return (
      cls.user_can_edit_lobby(user=user, lobby=lobby) or
      cls.user_in_slot(user=user, slot=slot)
    )
  
  @classmethod
  def user_can_set_slot_type(cls, user: Optional[User], lobby: LobbyState, slot: SlotInfo) -> bool:
    return (
      slot.status == SlotStatus.EMPTY and
      cls.user_can_edit_lobby(user=user, lobby=lobby)
    )
    
    
    
  


class Summary:
  @classmethod
  def slot(cls, slot: SlotState, user: Optional[User]) -> List[SlotSummary]:
    return SlotSummary(
      status=slot.status,
    )
  
  @classmethod
  def slots(cls, slots: List[SlotState], user: Optional[User]) -> List[SlotSummary]:
    return [cls.slot(slot=slot, user=user) for slot in slots]
    
  @classmethod
  def lobby(cls, lobby: LobbyState, user: Optional[User]) -> List[LobbySummary]:
    return LobbySummary(
      uuid=str(lobby.uuid),
      label=lobby.label,
      creator=lobby.creator,
      created=lobby.created,
      game=lobby.game,
      slots=cls.slots(slots=lobby.slots, user=user),
      num_spectators=len(lobby.spectators),
      joinable=LobbyUtils.user_can_join_lobby(user=user, lobby=lobby),
      editable=False,
      deletable=False,
    )
  
  @classmethod
  def lobbies(cls, user: Optional[User], lobbies: List[LobbyState]) -> List[LobbySummary]:
    return [cls.lobby(user=user, lobby=lobby) for lobby in lobbies]


class LobbyPerspective:
  @classmethod
  def slot_permissions(cls, user: Optional[User], lobby: LobbyState, slot: SlotInfo) -> SlotPermissions:
    return SlotPermissions(
      join=LobbyUtils.user_can_join_slot(user=user, lobby=lobby, slot=slot),
      delete=LobbyUtils.user_can_edit_lobby(user=user, lobby=lobby),
      kick=LobbyUtils.user_can_kick_slot(user=user, lobby=lobby, slot=slot),
      set_type=LobbyUtils.user_can_set_slot_type(user=user, lobby=lobby, slot=slot),
    )
    
  @classmethod
  def slot(cls, user: Optional[User], lobby: LobbyState, slot: SlotState) -> List[SlotInfo]:
    return SlotInfo(
      uuid=str(slot.uuid),
      slot_type=slot.slot_type,
      status=slot.status,
      user=slot.user,
      last_heartbeat=slot.last_heartbeat,
      present=LobbyUtils.user_in_slot(user, slot),
      permissions=cls.slot_permissions(user=user, lobby=lobby, slot=slot),
    )
  
  @classmethod
  def slots(cls, user: Optional[User], lobby: LobbyState, slots: List[SlotState]) -> List[SlotInfo]:
    return [cls.slot(user=user, lobby=lobby, slot=slot) for slot in slots]
  
  @classmethod
  def lobby_permissions(cls, user: Optional[User], lobby: LobbyState) -> LobbyPermissions:
    return LobbyPermissions(
      rename=LobbyUtils.user_can_edit_lobby(user=user, lobby=lobby),
      delete=LobbyUtils.user_can_edit_lobby(user=user, lobby=lobby),
      add_slot=LobbyUtils.user_can_edit_lobby(user=user, lobby=lobby),
      join=LobbyUtils.user_can_join_lobby(user=user, lobby=lobby),
    )
  
  @classmethod
  def lobby(cls, lobby: LobbyState, user: Optional[User] = None) -> LobbyInfo:
    return LobbyInfo(
      uuid=str(lobby.uuid),
      label=lobby.label,
      created=lobby.created,
      creator=lobby.creator,
      game=lobby.game,
      slots=cls.slots(user=user, lobby=lobby, slots=lobby.slots),
      spectators=lobby.spectators,
      present=LobbyUtils.user_is_present(user=user, lobby=lobby),
      permissions=cls.lobby_permissions(user=user, lobby=lobby),
    )