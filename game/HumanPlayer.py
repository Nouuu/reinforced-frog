from arcade import Sprite

from conf.config import ACTION_NONE, ENTITIES, FROG_TOKEN, ACTION_MOVES, ACTION_DOWN
from display.entity.world_entity import WorldEntity
from game.Player import Player
from game.world import World


class HumanPlayer(Player):
    def __init__(self):
        self.__state = (0, 0)
        pass

    def init(self, world: World, intial_state: (int, int)):
        self.__state = intial_state
        pass

    def best_move(self) -> (int, int):
        return ACTION_MOVES[ACTION_NONE]

    def step(self, action: (int, int), reward: float, new_state: (int, int)):
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
