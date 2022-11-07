from typing import Tuple, List

from arcade import Sprite

from conf.config import ACTION_NONE, ENTITIES, FROG_TOKEN
from display.entity.world_entity import WorldEntity
from game.Player import Player
from game.world import World


class HumanPlayer(Player):
    def __init__(self):
        self.__state = (0, 0)
        pass

    def init(self, world: World, intial_state: Tuple[int, int], _initial_environment: bytes):
        self.__state = intial_state
        pass

    def best_move(self, environment) -> str:
        return ACTION_NONE

    def step(self, action: str, reward: float, new_state: Tuple[int, int], _environment: List[str]):
        self.__state = new_state

    def update_state(self, new_state, new_environment):
        self.__state = new_state

    @property
    def sprite(self) -> Sprite:
        return ENTITIES[FROG_TOKEN].sprite

    @property
    def world_entity(self) -> WorldEntity:
        return ENTITIES[FROG_TOKEN]

    @property
    def is_human(self):
        return True

    @property
    def state(self):
        return self.__state
