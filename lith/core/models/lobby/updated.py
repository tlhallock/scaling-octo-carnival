
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
from core.models.lobby.info import LobbyInfo
from core.models.game.launched import GameLaunched


class LobbyUpdateType(Enum):
    STATE_CHANGED = auto
    REQUEST_HEARTBEAT = auto
    KICKED = auto
    LAUNCHED = auto


class LobbyUpdated(BaseModel):
    update_type: LobbyUpdateType
    state: Optional[LobbyInfo]
    launch: Optional[GameLaunched]
    terminal: bool
    
    def has_more_updates(self) -> bool:
        return self.update_type in [
            LobbyUpdateType.STATE_CHANGED,
            LobbyUpdateType.REQUEST_HEARTBEAT,
        ]
    
    def no_more_updates(self) -> bool:
        return not self.has_more_updates()


