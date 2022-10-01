from arcade import Sprite

from display.entity.world_entity import WorldEntity
from game.Position import Position
from game.utils import get_collisions
from game.world import World


class Player:
    # Est ce le fait d'^être mort ne doit pas être dans le state
    def __init__(self, world: World, intial_state: (int, int)):
        x, y = intial_state
        self.__world = world
        self.__position = Position(x, y)
        self.__world_entity = WorldEntity(self.__position.x, self.__position.y, 1, 1, "player.png")


    def best_move(self) -> (int, int):
        pass

    def step(self, action: (int, int), reward: float, new_state: (int, int)):
        pass

    def is_dead(self):
        # Acceder au world dimesion...
        # il faut être entre 0 et max -1 sur les deux coordonnées
        if not 0 < self.__position.x < self.__world.width:
            return False
        if not 0 < self.__position.y < self.__world.height:
            return False
        collisions = get_collisions(
            self.__world_entity,
            (self.__position.x, self.__position.y),
            self.__world.get_world_line_entity((self.__position.x, self.__position.y)),
            self.__world.get_world_entity((self.__position.x, self.__position.y)),
            self.__world.scaling
        )
        if collisions.len() > 0:
            return False
        # TODO
        # Get Collsion et is_safe_zone_on_water
        return True


    # Je pense pas que ça soit le role du player de connaitre son sprite
    @property
    def sprite(self) -> Sprite:
        pass

    def world_entity(self) -> WorldEntity:
        pass

    @property
    def is_human(self) -> bool:
        pass

    @property
    def state(self) -> (int, int):
        pass

    @property
    def position(self) -> Position:
        return self.__position

