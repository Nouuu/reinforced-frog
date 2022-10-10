from arcade import Sprite

from display.entity.world_entity import WorldEntity
from game.world import World


class Player:
    def init(self, world: World, intial_state: (int, int), initial_environment: bytes):
        pass

    def best_move(self) -> str:
        pass

    def step(self, action: str, reward: float, new_state: (int, int), environment: bytes):
        pass

    def save_score(self):
        pass

    @property
    def sprite(self) -> Sprite:
        pass

    @property
    def world_entity(self) -> WorldEntity:
        pass

    @property
    def is_human(self) -> bool:
        pass

    @property
    def state(self) -> (int, int):
        pass
