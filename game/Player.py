from arcade import Sprite

from display.entity.world_entity import WorldEntity
from game.world import World


class Player:
    def init(self, world: World, intial_state: (int, int)):
        pass

    def best_move(self) -> (int, int):
        pass

    def step(self, action: (int, int), reward: float, new_state: (int, int)):
        pass

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
