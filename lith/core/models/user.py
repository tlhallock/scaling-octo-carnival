from enum import Enum
from pydantic import BaseModel


class UserType(Enum):
  ROBOT = "ROBOT"
  HUMAN = "HUMAN"
    
  # TODO: implement...
  LOCAL_BOT = "LOCAL_BOT"
  ANONYMOUS = "ANONYMOUS"


class UserInfo(BaseModel):
  uuid: str  # uuid?
  username: str
  user_type: UserType
  
  class Config:  
    use_enum_values = True
