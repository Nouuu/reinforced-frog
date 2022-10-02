from typing import Tuple
from arcade import Sprite

from display.entity.world_entity import WorldEntity
from game.Position import Position
from game.utils import get_collisions
from game.world import World
from utils import is_in_safe_zone_on_water

class Player:
    # Est ce le fait d'être mort ne doit pas être dans le state
    def __init__(self, world: World, position: Position):
        self.__world = world
        self._position = position

        # Not sure about this
        self.__world_entity = WorldEntity(position.x, position.y, 1, 1, "player.png")


    def best_move(self) -> Tuple[int, int]:
        # TODO
        pass

    def step(self, action: Tuple[int, int], reward: float, new_state: Tuple[int, int]):
        # TODO
        pass

    def is_dead(self):
        # Acceder au world dimesion...
        # il faut être entre 0 et max -1 sur les deux coordonnées
        if not 0 < self._position.x < self.__world.width:
            return False
        if not 0 < self._position.y < self.__world.height:
            return False
        collisions = get_collisions(
            self.__world_entity,
            (self._position.x, self._position.y),
            self.__world.get_world_line_entity((self._position.x, self._position.y)),
            self.__world.get_world_entity((self._position.x, self._position.y)),
            self.__world.scaling
        )
        if collisions.len() > 0:
            return False

        if not is_in_safe_zone_on_water(
                self.__world_entity,
                (self._position.x, self._position.y),
                self.__world.get_world_entity((self._position.x, self._position.y)),
                self.__world.scaling
            ):
            return False

        # Get Collsion et is_safe_zone_on_water
        return True


    # Je pense pas que ça soit le role du player de connaitre son sprite
    @property
    def sprite(self) -> Sprite:
        self.__world_entity.sprite

    def world_entity(self) -> WorldEntity:
        self.__world_entity

    @property
    def state(self) -> Tuple[int, int]:
        return self._position.x, self._position.y

    @property
    def position(self) -> Position:
        return self._position

