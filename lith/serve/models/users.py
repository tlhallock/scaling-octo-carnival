
from typing import Any, Dict, Optional
import motor.motor_asyncio
from fastapi import FastAPI, Request, Depends
from fastapi_users import FastAPIUsers, models
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users.authentication import CookieAuthentication, JWTAuthentication
from core.models.user import UserType



# --- Users Collection Schema Setup -------------------------------------------

# Pydantic models for MongoDB "User" collection schema
# Learn more at https://frankie567.github.io/fastapi-users/configuration/model/

class User(models.BaseUser):
  """
  Fields "id", "email", "is_active" and "is_superuser" are created by this model
  """
    
  # Needs to be optional, otherwise it must be present in login requests.
  username: str
  user_type: UserType
  
  class Config:  
    use_enum_values = True


class UserCreate(models.BaseUserCreate):
  username: str
  user_type: Optional[UserType] = None
  
  class Config:  
    use_enum_values = True


class UserUpdate(User, models.BaseUserUpdate):
  username: Optional[str]


class UserDB(User, models.BaseUserDB):
  """
    This class Extends/Inherits the User class

    Field "hashed_password" is created by this model
  """
  user_type: UserType = UserType.HUMAN
  
  class Config:  
    use_enum_values = True

#   def dict(self, *args, **kwargs) -> Dict[Any, Any]:
#     d = super().dict()
#     print("serializing", d)
#     d["user_type"] = self.user_type.name
#     return d
