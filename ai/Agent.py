import pickle
from typing import Dict, List

from arcade import Sprite

from conf.config import ACTION_MOVES, FROG_IA_TOKEN, ENTITIES, random, ACTIONS
from display.entity.world_entity import WorldEntity
from game.Player import Player
from game.world import World


class Agent(Player):

    def __init__(self,
                 alpha: float = 1,
                 gamma: float = 0.8,
                 exploration_rate: float = 0.1,
                 learning: bool = True,
                 ):
        self.__alpha = alpha
        self.__gamma = gamma
        self.__state = (0, 0)
        self.__current_environment = b''
        self.__qtable: Dict[bytes, Dict[str, float]] = {}
        self.__score = 0
        self.__score_history: List[int] = []
        self.__step_count = 0
        self.__world_height = 0
        self.__world_width = 0
        self.__qtable_load_count = 0
        self.__exploration_rate = exploration_rate
        self.__last_history_index = 0
        self.__learning = learning

    def init(self, world: World, intial_state: (int, int), initial_environment: bytes):
        self.__state = intial_state
        self.__current_environment = initial_environment
        self.__world_height = world.height
        self.__world_width = world.width
        self.__score = 0

    def save_score(self):
        self.__score_history.append(self.__score)

    def get_qtable_state(self, environment: bytes, _state: (int, int)) -> Dict[str, float]:
        if environment not in self.__qtable:
            self.__qtable[environment] = {}
            self.__qtable[environment] = {action: 0 for action in ACTION_MOVES}
        return self.__qtable[environment]

    def best_move(self) -> str:
        if random.random() < self.__exploration_rate:
            return random.choice(ACTIONS)
        actions = self.get_qtable_state(self.__current_environment, self.__state)
        action = max(actions, key=actions.get)
        return action

    def step(self, action: str, reward: float, new_state: (int, int), new_environment: bytes):
        if self.__learning:
            max_q = max(self.get_qtable_state(new_environment, new_state).values())
            self.get_qtable_state(self.__current_environment, self.__state)[action] += \
                self.__alpha * (
                    reward + self.__gamma * max_q - self.get_qtable_state(self.__current_environment, self.__state)[
                    action])
        self.__state = new_state
        self.__current_environment = new_environment
        self.__score += reward
        self.__step_count += 1

    def save(self, filename: str):
        print(f'Qtable entries : {len(self.__qtable)}')
        if self.__qtable_load_count is not None:
            print(f'New states since previous save: {len(self.__qtable) - self.__qtable_load_count}')
            self.__qtable_load_count = len(self.__qtable)
        with open(filename, 'wb') as file:
            pickle.dump((self.__qtable, self.__score_history), file)

    def load(self, filename: str):
        with open(filename, 'rb') as file:
            (self.__qtable, self.__score_history) = pickle.load(file)
            self.__qtable_load_count = len(self.__qtable)
            self.__last_history_index = len(self.__score_history)

    def set_qtable(self, qtable: Dict[bytes, Dict[str, float]]):
        self.__qtable = qtable

    def print_stats(self, time_elapsed: int):
        print("--------------------------------")
        print(
            f"Agent win average is : {round(self.win_average(self.__last_history_index) * 100, 3)}% "
            f"({self.win_count(self.__last_history_index)} wins / {self.loose_count(self.__last_history_index)} looses)")
        print(f"Speed : {round(self.step_count / time_elapsed, 1)} step/s")
        print("--------------------------------")
        self.__last_history_index = len(self.__score_history)

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

    def best_score(self) -> float:
        return max(self.__score_history)

    def win_average(self, start_index: int) -> float:
        return self.win_count(start_index) / len(self.__score_history[start_index:])

    def loose_count(self, start_index: int) -> int:
        return sum(map(lambda score: score < 0, self.__score_history[start_index:]))

    def win_count(self, start_index: int) -> int:
        return sum(map(lambda score: score >= 0, self.__score_history[start_index:]))

    @property
    def score_history(self):
        return self.__score_history

    @property
    def step_count(self) -> int:
        return self.__step_count
