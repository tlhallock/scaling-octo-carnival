
from pydantic import UUID4

class EntityNotFound(Exception):
  entity_type: str
  uuid: UUID4
  
  def __init__(self, entity_type: str, uuid: UUID4, *args) -> None:
    super().__init__(*args)
    self.entity_type = entity_type
    self.uuid = uuid
