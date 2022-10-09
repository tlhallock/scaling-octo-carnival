
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


# Could be called perspectives too...
class SlotInfo(BaseModel):
  uuid: str
  slot_type: SlotType
  status: SlotStatus
  user: Optional[UserInfo]
  last_heartbeat: Optional[TimeRep]
  
  you: bool
  available: bool
  editable: bool
  # kickable: bool
  # deletable: bool
  

class LobbyInfo(BaseModel):
  uuid: str
  label: str
  created: TimeRep
  creator: UserInfo
  game: str
  slots: List[SlotInfo]
  spectators: List[UserInfo]
  
  present: bool
  editable: bool
  deletable: bool
  
  