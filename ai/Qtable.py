import lzma
import pickle
import shutil
from typing import Dict

from ai.Model import Model
from conf.config import ACTION_MOVES

lzma_filters = [
    {"id": lzma.FILTER_DELTA, "dist": 5},
    {"id": lzma.FILTER_LZMA2, "preset": 7 | lzma.PRESET_EXTREME},
]


class Qtable(Model):
    def __init__(self, alpha: float, gamma: float, score_history_packets: int, visible_lines_above: int):
        self.__visible_lines = visible_lines_above + 2
        self.__qtable = {}
        self.__alpha = alpha
        self.__gamma = gamma
        self.__qtable_load_count = 0
        self.__score_history_packets = score_history_packets
        self.__score_history = []
        self.__score_history_temp = []
        self.__step_count = 0
        self.__win_count = 0
        self.__loose_count = 0

    def load(self, filename: str):
        print(f'Loading Qtable from {filename}...')
        with lzma.LZMAFile(filename, "rb") as uncompressed:
            self.__qtable = pickle.load(uncompressed)
            self.__qtable_load_count = self.__qtable_count(self.__qtable, self.__visible_lines)
        print(f'Qtable loaded, {self.__qtable_load_count} entries')

    def save(self, qtable_filename: str, score_filename: str):
        print(f'Qtable entries : {self.__qtable_count(self.__qtable, self.__visible_lines)}')
        if self.__qtable_load_count is not None:
            self.__qtable_clear_empty(self.__qtable, self.__visible_lines)
            print(
                f'New states since previous save: '
                f'{self.__qtable_count(self.__qtable, self.__visible_lines) - self.__qtable_load_count}\n'
                f'Saving stable...')
            self.__qtable_load_count = self.__qtable_count(self.__qtable, self.__visible_lines)
        with lzma.open(qtable_filename + ".tmp", 'wb') as file:
            pickle.dump(self.__qtable, file)
        shutil.move(qtable_filename + ".tmp", qtable_filename)
        with open(score_filename, 'a+') as file:
            history = "\n".join(map(str, self.__score_history))
            file.write(f'{history}\n')
            self.__score_history = []
        print("Qtable saved")

    def get_state_actions(self, state: [str]) -> Dict[str, float]:
        return self.__get_state_actions(self.__qtable, state, self.__visible_lines)

    def __get_state_actions(self, qtable: dict, state: [str], visible_lines_above: int) -> Dict[str, float]:
        for i in range(visible_lines_above):
            if environment[i] not in qtable:
                qtable[environment[i]] = {}
            qtable = qtable[environment[i]]
        if len(qtable) <= 0:
            for action in ACTION_MOVES:
                qtable[action] = 0
        return qtable

    def update_state(self, state: [str], max_q: float,
                     reward: float,
                     action: str):
        qtable = self.get_state_actions(state)
        qtable[action] = (1 - self.__alpha) * qtable[action] + self.__alpha * (reward + self.__gamma * max_q)
        self.__increment_step_count()

    def print_stats(self, time_elapsed: int):
        print("--------------------------------")
        print(
            f"Agent win average is : {round(self.__win_average() * 100, 3)}% "
            f"({self.__win_count} wins /"
            f" {self.__loose_count} looses)")
        print(f"Speed : {round(self.__step_count / time_elapsed, 1)} step/s")
        print("--------------------------------")
        self.__win_count = 0
        self.__loose_count = 0

    def __increment_step_count(self):
        self.__step_count += 1

    def save_score(self, score: float):
        self.__score_history_temp.append(score)
        if score > 0:
            self.__win_count += 1
        else:
            self.__loose_count += 1
        if len(self.__score_history_temp) >= self.__score_history_packets:
            self.__score_history.append(sum(self.__score_history_temp) / len(self.__score_history_temp))
            self.__score_history_temp = []

    def __win_average(self) -> float:
        if self.__win_count + self.__loose_count == 0:
            return 0
        return float(self.__win_count) / (self.__win_count + self.__loose_count)

    def __qtable_count(self, qtable: dict, line_above: int) -> int:
        if line_above == 1:
            return len(qtable)
        return sum([self.__qtable_count(qtable[key], line_above - 1) for key in qtable.keys()])

    def __qtable_clear_empty(self, qtable: dict, line_above: int):
        if line_above == 1:
            to_delete = []
            for key, state in qtable.items():
                if all(action == 0 for action in state.values()):
                    to_delete.append(key)
            for key in to_delete:
                qtable.pop(key)
            return
        [self.__qtable_clear_empty(qtable[key], line_above - 1) for key in qtable.keys()]
