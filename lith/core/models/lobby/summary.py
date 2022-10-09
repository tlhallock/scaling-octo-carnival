
import asyncio

from enum import Enum, auto
import logging
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from core.models.user import UserInfo, UserType

from core.base import TimeRep, get_current_time
  # from core.model.game_launch import GameLaunch
  
from core.models.lobby.base import SlotStatus


class SlotSummary(BaseModel):
  status: SlotStatus


class LobbySummary(BaseModel):
  uuid: str
  label: str
  creator: UserInfo  # Could be photo
  created: TimeRep
  game: str
  slots: List[SlotSummary]
  num_spectators: int  # Could have photos
  
  joinable: bool
  editable: bool
  deletable: bool
  
