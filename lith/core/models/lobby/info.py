
import asyncio

from enum import Enum, auto
import logging
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from core.models.user import UserInfo, UserType

from core.base import TimeRep, get_current_time
  # from core.model.game_launch import GameLaunch
from core.models.lobby.base import SlotStatus
from core.models.lobby.base import SlotType


class SlotPermissions(BaseModel):
  delete: bool
  join: bool
  kick: bool
  set_type: bool


# Could be called perspectives too...
class SlotInfo(BaseModel):
  uuid: str
  slot_type: SlotType
  status: SlotStatus
  user: Optional[UserInfo]
  last_heartbeat: Optional[TimeRep]
  
  present: bool
  permissions: SlotPermissions


class LobbyPermissions(BaseModel):
  rename: bool
  delete: bool
  join: bool
  add_slot: bool
  

class LobbyInfo(BaseModel):
  uuid: str
  label: str
  created: TimeRep
  creator: UserInfo
  game: str
  slots: List[SlotInfo]
  spectators: List[UserInfo]
  
  present: bool
  permissions: LobbyPermissions
  
  