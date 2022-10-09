
from typing import List, Optional
from core.models.lobby.info import LobbyInfo, SlotInfo
from core.models.lobby.summary import LobbySummary, SlotSummary
from core.models.user import UserInfo
from serve.models.lobby.state import LobbyState, SlotState


class Summary:
  @classmethod
  def slot(cls, slot: SlotState, user: Optional[UserInfo]) -> List[SlotSummary]:
    return SlotSummary(
      status=slot.status,
    )
  
  @classmethod
  def slots(cls, slots: List[SlotState], user: Optional[UserInfo]) -> List[SlotSummary]:
    return [cls.slot(slot=slot, user=user) for slot in slots]
    
  @classmethod
  def lobby(cls, lobby: LobbyState, user: Optional[UserInfo]) -> List[LobbySummary]:
    return LobbySummary(
      uuid=str(lobby.uuid),
      label=lobby.label,
      creator=lobby.creator,
      created=lobby.created,
      game=lobby.game,
      slots=cls.slots(slots=lobby.slots, user=user),
      num_spectators=len(lobby.spectators),
      joinable=False,
      editable=False,
      deletable=False,
    )
  
  @classmethod
  def lobbies(cls, lobbies: List[LobbyState], user: Optional[UserInfo]) -> List[LobbySummary]:
    return [cls.lobby(lobby, user=user) for lobby in lobbies]


class LobbyPerspective:
  @classmethod
  def slot(cls, slot: SlotState, user: Optional[UserInfo]) -> List[SlotInfo]:
    return SlotInfo(
      uuid=str(slot.uuid),
      slot_type=slot.slot_type,
      status=slot.status,
      user=slot.user,
      last_heartbeat=slot.last_heartbeat,
      you=False,
      available=False,
      editable=False,
      deletable=False,
    )
  
  @classmethod
  def slots(cls, slots: List[SlotState], user: Optional[UserInfo]) -> List[SlotInfo]:
    return [cls.slot(slot=slot, user=user) for slot in slots]
  
  @classmethod
  def lobby(cls, lobby: LobbyState, user: Optional[UserInfo] = None) -> LobbyInfo:
    return LobbyInfo(
      uuid=str(lobby.uuid),
      label=lobby.label,
      created=lobby.created,
      creator=lobby.creator,
      game=lobby.game,
      slots=cls.slots(slots=lobby.slots, user=user),
      spectators=lobby.spectators,
      present=False,
      editable=False,
      deletable=False,
    )