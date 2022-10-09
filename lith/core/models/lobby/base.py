

from typing import Dict

import asyncio

from enum import Enum, auto
import logging
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from core.models.user import UserInfo, UserType

from core.base import TimeRep, get_current_time
  # from core.model.game_launch import GameLaunch





class SlotType(Enum):
    ANY = "AUTO"
    ONLY_HUMAN = "HUMAN"
    ONLY_BOT = "BOT"
    # Could have a local bot


class SlotStatus(Enum):
    EMPTY = "EMPTY"
    NOT_READY = "NOT_READY"
    READY = "READY"
    CONNECTING = "CONNECTING"
    IN_GAME = "IN_GAME"
    

class LobbyStatus(Enum):
    EMPTY = "EMPTY"
    WAITING = "WAITING"
    READY = "READY"
    LAUNCHING = "LAUNCHING"
    IN_GAME = "IN_GAME"



# Should not be here?
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



class LobbyHelpers:
    @staticmethod
    def type_accepts(stype: SlotType, utype: UserType) -> bool:
      try:
        return utype in SLOT_TYPE_ACCEPTS[stype]
      except:
          raise Exception(f"Types not checked: {stype.name}, {utype.name}")
