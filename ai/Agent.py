from arcade import Sprite

from ai.Qtable import Qtable
from conf.config import FROG_IA_TOKEN, ENTITIES, random, ACTIONS
from display.entity.world_entity import WorldEntity
from game.Player import Player
from game.world import World


class Agent(Player):

    def __init__(self,
                 qtable: Qtable,
                 exploration_rate: float = 0.1,
                 learning: bool = True,
                 ):
        self.__qtable = qtable
        self.__state = (0, 0)
        self.__current_environment = b''
        self.__score = 0
        self.__world_height = 0
        self.__world_width = 0
        self.__exploration_rate = exploration_rate
        self.__learning = learning

    def init(self, world: World, intial_state: (int, int), initial_environment: bytes):
        self.__state = intial_state
        self.__current_environment = initial_environment
        self.__world_height = world.height
        self.__world_width = world.width
        self.__score = 0

    def save_score(self):
        self.__qtable.save_score(self.__score)

    def best_move(self) -> str:
        if random.random() < self.__exploration_rate:
            return random.choice(ACTIONS)
        actions = self.__qtable.get_qtable_state(self.__current_environment)
        action = max(actions, key=actions.get)
        return action

    def step(self, action: str, reward: float, new_state: (int, int), new_environment: bytes):
        if self.__learning:
            max_q = max(self.__qtable.get_qtable_state(new_environment).values())
            self.__qtable.update_qtable_state(
                self.__current_environment,
                max_q,
                reward,
                action
            )
        self.__state = new_state
        self.__current_environment = new_environment
        self.__score += reward

    def update_state(self, new_state, new_environment):
        self.__state = new_state
        self.__current_environment = new_environment

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
