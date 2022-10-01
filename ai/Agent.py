from arcade import Sprite

from conf.config import ACTION_MOVES, FROG_IA_TOKEN, ENTITIES
from display.entity.world_entity import WorldEntity
from game.Player import Player
from game.world import World


class Agent(Player):

    def __init__(self,
                 alpha: float = 1,
                 gamma: float = 0.8,
                 ):
        self.__alpha = alpha
        self.__gamma = gamma
        self.__state = (0, 0)
        self.__qtable = {}
        self.__score = 0

    def init(self, world: World, intial_state: (int, int)):
        self.__state = intial_state
        self.__init_qtable(world)

    def __init_qtable(self, world):
        for x in range(world.width):
            for y in range(world.height):
                state = (y, x)
                self.__qtable[state] = {}
                for action in ACTION_MOVES:
                    self.__qtable[state][action] = 0

    def best_move(self) -> str:
        actions = self.__qtable[self.__state]
        action = max(actions, key=actions.get)
        return action

    def step(self, action: str, reward: float, new_state: (int, int)):
        max_q = max(self.__qtable[new_state].values())
        self.__qtable[self.__state][action] += \
            self.__alpha * (reward + self.__gamma * max_q - self.__qtable[self.__state][action])
        self.__state = new_state
        self.__score += reward

    @property
    def sprite(self) -> Sprite:
        return ENTITIES[FROG_IA_TOKEN].sprite

    @property
    def world_entity(self) -> WorldEntity:
        return ENTITIES[FROG_IA_TOKEN]

    @property
    def is_human(self) -> bool:
        return False

    @property
    def state(self) -> (int, int):
        return self.__state
