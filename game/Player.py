from typing import Tuple, Dict, List

from arcade import Sprite

from display.entity.world_entity import WorldEntity
from game.world import World


class Player:
    def init(self, world: World, intial_state: Tuple[int, int], _initial_environment: bytes):
        pass

    def best_move(self, environment: [str]) -> str:
        pass

    def step(self, action: str, reward: float, new_state: Tuple[int, int], _environment: List[str]):
        pass

    def save_score(self):
        pass

    def update_state(self, new_state, new_environment):
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
    def score(self) -> int:
        pass

    @property
    def state(self) -> Tuple[int, int]:
        pass
