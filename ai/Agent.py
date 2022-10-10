import pickle

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
        self.__qtable: {bytes: {(int, int): float}} = {}
        self.__score = 0
        self.__score_history = []
        self.__world_height = 0
        self.__world_width = 0

    def init(self, world: World, intial_state: (int, int), initial_environment: bytes):
        self.__state = intial_state
        self.__current_environment = initial_environment
        self.__world_height = world.height
        self.__world_width = world.width
        self.__score = 0

    def save_score(self):
        self.__score_history.append(self.__score)

    def __get_qtable_state(self, environment: bytes) -> {(int, int): float}:
        if environment not in self.__qtable:
            self.__qtable[environment] = {}
            for x in range(self.__world_width):
                for y in range(self.__world_height):
                    state = (y, x)
                    self.__qtable[environment][state] = {}
                    for action in ACTION_MOVES:
                        self.__qtable[environment][state][action] = 0
        return self.__qtable[environment]

    def best_move(self) -> str:
        actions = self.__get_qtable_state(self.__current_environment)[self.__state]
        action = max(actions, key=actions.get)
        return action

    def step(self, action: str, reward: float, new_state: (int, int), environment: bytes):
        max_q = max(self.__get_qtable_state(environment)[new_state].values())
        self.__get_qtable_state(self.__current_environment)[self.__state][action] += \
            self.__alpha * (reward + self.__gamma * max_q - self.__get_qtable_state(environment)[self.__state][action])
        self.__state = new_state
        self.__current_environment = environment
        self.__score += reward

    def save(self, filename: str):
        print(f'Qtable entries : {len(self.__qtable)} -> {self.__qtable.keys()}')
        with open(filename, 'wb') as file:
            pickle.dump((self.__qtable, self.__score_history), file)

    def load(self, filename: str):
        with open(filename, 'rb') as file:
            (self.__qtable, self.__score_history) = pickle.load(file)

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
