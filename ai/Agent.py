import pickle
from typing import Dict

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
        self.__current_environment = b''
        self.__qtable: Dict[bytes, Dict[str, float]] = {}
        self.__score = 0
        self.__score_history = []
        self.__world_height = 0
        self.__world_width = 0
        self.__qtable_load_count = 0

    def init(self, world: World, intial_state: (int, int), initial_environment: bytes):
        self.__state = intial_state
        self.__current_environment = initial_environment
        self.__world_height = world.height
        self.__world_width = world.width
        self.__score = 0

    def save_score(self):
        self.__score_history.append([self.__state, self.__score])

    def get_qtable_state(self, environment: bytes, _state: (int, int)) -> Dict[str, float]:
        if environment not in self.__qtable:
            self.__qtable[environment] = {}
            self.__qtable[environment] = {action: 0 for action in ACTION_MOVES}
        return self.__qtable[environment]

    def best_move(self) -> str:
        actions = self.get_qtable_state(self.__current_environment, self.__state)
        action = max(actions, key=actions.get)
        return action

    def step(self, action: str, reward: float, new_state: (int, int), new_environment: bytes):
        max_q = max(self.get_qtable_state(new_environment, new_state).values())
        self.get_qtable_state(self.__current_environment, self.__state)[action] += \
            self.__alpha * (
                reward + self.__gamma * max_q - self.get_qtable_state(self.__current_environment, self.__state)[
                action])
        self.__state = new_state
        self.__current_environment = new_environment
        self.__score += reward

    def save(self, filename: str):
        print(f'Qtable entries : {len(self.__qtable)}')
        if self.__qtable_load_count is not None:
            print(f'New states since previous load: {len(self.__qtable) - self.__qtable_load_count}')
        with open(filename, 'wb') as file:
            pickle.dump(self.__qtable, file)

    def load(self, filename: str):
        with open(filename, 'rb') as file:
            self.__qtable = pickle.load(file)
            self.__qtable_load_count = len(self.__qtable)

    def set_qtable(self, qtable: Dict[bytes, Dict[str, float]]):
        self.__qtable = qtable

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

    @property
    def score(self) -> int:
        return self.__score

    @property
    def score_history(self):
        return self.__score_history
