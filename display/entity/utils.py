from conf.config import WORLD_ENTITIES
from display.entity.world_entity import WorldEntity


def get_entity(token: str) -> WorldEntity | None:
    """
    Return the entity associated to the token\n
    Return (entity: WorldEntity)
    """
    return WORLD_ENTITIES.get(token, None)
