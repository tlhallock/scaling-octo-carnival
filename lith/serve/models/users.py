
from typing import Any, Dict, Optional
from uuid import uuid4
import motor.motor_asyncio
from fastapi import FastAPI, Request, Depends
from fastapi_users import FastAPIUsers, models
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users.authentication import CookieAuthentication, JWTAuthentication
from core.models.user import UserInfo, UserType
from pydantic import UUID4

from pydantic import Field

# --- Users Collection Schema Setup -------------------------------------------

# Pydantic models for MongoDB "User" collection schema
# Learn more at https://frankie567.github.io/fastapi-users/configuration/model/

class User(models.BaseUser):
  """
  Fields "id", "email", "is_active" and "is_superuser" are created by this model
  """
    
  # Needs to be optional, otherwise it must be present in login requests.
  uuid: UUID4 = Field(default_factory=uuid4)
  username: str
  user_type: UserType
  
  class Config:  
    use_enum_values = True


class UserCreate(models.BaseUserCreate):
  username: str
  user_type: Optional[UserType] = UserType.HUMAN
  
  class Config:  
    use_enum_values = True


class UserUpdate(User, models.BaseUserUpdate):
  username: Optional[str]


class UserDB(User, models.BaseUserDB):
  """
    Field "hashed_password" is created by this model
  """
  user_type: Optional[UserType] = UserType.HUMAN
  
  class Config:  
    use_enum_values = True


def export_user(user: UserDB) -> UserInfo:
  return UserInfo(
    uuid=str(user.uuid),
    username=user.username,
    user_type=user.user_type,
  )


def export_optional_user(user: Optional[UserDB]) -> Optional[UserInfo]:
  if user is None:
    return None
  return export_user(user)
