from arcade import Sprite

from ai.Model import Model
from conf.config import FROG_IA_TOKEN, ENTITIES, random, ACTIONS
from display.entity.world_entity import WorldEntity
from game.Player import Player
from game.world import World


class Agent(Player):

    def __init__(self,
                 model: Model,
                 exploration_rate: float = 0.1,
                 exploration_decay: float = 0.999,
                 learning: bool = True,
                 ):
        self.__model = model
        self.__state = (0, 0)
        self.__current_environment = b''
        self.__score = 0
        self.__world_height = 0
        self.__world_width = 0
        self.__exploration_rate = exploration_rate
        self.__exploration_decay = exploration_decay
        self.__learning = learning

    def init(self, world: World, intial_state: (int, int), initial_environment: [str]):
        self.__state = intial_state
        self.__current_environment = initial_environment
        self.__world_height = world.height
        self.__world_width = world.width
        self.__score = 0

    def save_score(self):
        self.__model.save_score(self.__score)

    def best_move(self, environment: [str]) -> str:
        self.__current_environment = environment
        if self.__exploration_rate > 0.0005 and random.random() < self.__exploration_rate:
            self.__exploration_rate *= self.__exploration_decay
            return random.choice(ACTIONS)
        actions = self.__model.get_state_actions(self.__current_environment)
        action = max(actions, key=actions.get)
        return action

    def step(self, action: str, reward: float, new_state: (int, int), new_environment: [str]):
        if self.__learning:
            max_q = max(self.__model.get_state_actions(new_environment).values())
            self.__model.update_state(
                self.__current_environment,
                max_q,
                reward,
                action
            )
        self.update_state(new_state, new_environment, reward)

    def update_state(self, new_state, new_environment, reward=0.):
        self.__state = new_state
        self.__current_environment = new_environment
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

    @property
    def score(self) -> int:
        return self.__score
