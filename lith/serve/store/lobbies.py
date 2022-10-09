
from typing import Any, List, Optional, Type

from serve.db import Collections

from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import UUID4

from fastapi_users.db.base import BaseUserDatabase
from fastapi_users.models import UD

from motor.motor_asyncio import AsyncIOMotorCollection
from serve.models.lobby.state import LobbyState


from serve.store.base import EntityNotFound


class LobbyStore:
  collection: AsyncIOMotorCollection

  def __init__(
    self,
    collection: AsyncIOMotorCollection,
  ):
    self.collection = collection
    self.collection.create_index("uuid", unique=True)
  
  async def list(self, skip: int, limit: int) -> List[LobbyState]:
    cursor = self.collection.find(skip=skip, limit=limit)
    entities = await cursor.to_list(length=limit)
    return [
      LobbyState.parse_obj(entity)
      for entity in entities
    ]

  async def get(self, uuid: UUID4) -> Optional[LobbyState]:
    entity = await self.collection.find_one({"uuid": uuid})
    if not entity:
      # log...
      raise EntityNotFound(entity_type="lobby", uuid=uuid)
    return LobbyState.parse_obj(entity);

  async def create(self, entity: LobbyState) -> UUID4:
    # This doesn't have an id!!
    result = await self.collection.insert_one(entity.dict())
    print("Created with ObjectId=", result.inserted_id)
    ret = await self.get(uuid=entity.uuid)
    # if ret is None:
    #   raise Exception()
    # return ret
    return entity.uuid

  async def update(self, lobby: LobbyState) -> LobbyState:
    # find_one_and_update
    result = await self.collection.replace_one(
      {"id": lobby.id},
      lobby.dict()
    )
    print(result)
    ret = self.get(lobby.id)
    if ret is None:
      raise Exception()
    return ret

  async def delete(self, id: UUID4) -> bool:
    result = await self.collection.delete_one({"id": id})
    print(result)
    return result.nb_deleted == 1

lobby_store = LobbyStore(collection=Collections.lobbies)
