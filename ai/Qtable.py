import pickle
from typing import Dict

from conf.config import ACTION_MOVES


class Qtable:
    def __init__(self, alpha: float, gamma: float):
        self.__qtable: Dict[bytes, Dict[str, float]] = {}
        self.__alpha = alpha
        self.__gamma = gamma
        self.__qtable_load_count = 0
        self.__last_history_index = 0
        self.__score_history = []
        self.__step_count = 0

    def load(self, filename: str):
        with open(filename, 'rb') as file:
            (self.__qtable, self.__score_history) = pickle.load(file)
            self.__qtable_load_count = len(self.__qtable)
            self.__last_history_index = len(self.__score_history)

    def save(self, filename: str):
        print(f'Qtable entries : {len(self.__qtable)}')
        if self.__qtable_load_count is not None:
            print(f'New states since previous save: {len(self.__qtable) - self.__qtable_load_count}')
            self.__qtable_load_count = len(self.__qtable)
        with open(filename, 'wb') as file:
            pickle.dump((self.__qtable, self.__score_history), file)

    def set_qtable(self, qtable: Dict[bytes, Dict[str, float]]):
        self.__qtable = qtable

    def get_qtable_state(self, environment: bytes) -> Dict[str, float]:
        if environment not in self.__qtable:
            self.__qtable[environment] = {}
            self.__qtable[environment] = {action: 0 for action in ACTION_MOVES}
        return self.__qtable[environment]

    def update_qtable_state(self, environment: bytes, max_q: float, reward: float,
                            action: str):
        self.get_qtable_state(environment)[action] += \
            self.__alpha * (reward + self.__gamma * max_q - self.get_qtable_state(environment)[action])

    def print_stats(self, time_elapsed: int):
        print("--------------------------------")
        print(
            f"Agent win average is : {round(self.win_average(self.__last_history_index) * 100, 3)}% "
            f"({self.win_count(self.__last_history_index)} wins /"
            f" {self.loose_count(self.__last_history_index)} looses)")
        print(f"Speed : {round(self.step_count / time_elapsed, 1)} step/s")
        print("--------------------------------")
        self.__last_history_index = len(self.__score_history)

    def increment_step_count(self):
        self.__step_count += 1

    def save_score(self, score: float):
        self.__score_history.append(score)

    def win_average(self, start_index: int) -> float:
        return self.win_count(start_index) / len(self.__score_history[start_index:])

    def loose_count(self, start_index: int) -> int:
        return sum(map(lambda score: score < 0, self.__score_history[start_index:]))

    def win_count(self, start_index: int) -> int:
        return sum(map(lambda score: score >= 0, self.__score_history[start_index:]))

    def best_score(self) -> float:
        return max(self.__score_history)

    @property
    def score_history(self):
        return self.__score_history

    @property
    def step_count(self) -> int:
        return self.__step_count
