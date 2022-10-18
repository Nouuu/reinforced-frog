import lzma
import pickle
import shutil
from typing import Dict

from conf.config import ACTION_MOVES

lzma_filters = [
    {"id": lzma.FILTER_DELTA, "dist": 5},
    {"id": lzma.FILTER_LZMA2, "preset": 7 | lzma.PRESET_EXTREME},
]


class Qtable:
    def __init__(self, alpha: float, gamma: float, qtable_history_packets: int, visible_lines_above: int):
        self.__visible_lines_above = visible_lines_above + 2
        self.__qtable = {}
        self.__alpha = alpha
        self.__gamma = gamma
        self.__qtable_load_count = 0
        self.__qtable_history_packets = qtable_history_packets
        self.__score_history = []
        self.__score_history_temp = []
        self.__step_count = 0
        self.__win_count = 0
        self.__loose_count = 0

    def load(self, filename: str):
        with lzma.LZMAFile(filename, "rb") as uncompressed:
            self.__qtable = pickle.load(uncompressed)
            self.__qtable_load_count = self.qtable_count(self.__qtable, self.__visible_lines_above)

    def save(self, qtable_filename: str, score_filename: str):
        print(f'Qtable entries : {self.qtable_count(self.__qtable, self.__visible_lines_above)}')
        if self.__qtable_load_count is not None:
            self.qtable_clear_empty(self.__qtable, self.__visible_lines_above)
            print(
                f'New states since previous save: '
                f'{self.qtable_count(self.__qtable, self.__visible_lines_above) - self.__qtable_load_count}\n'
                f'Saving stable...')
            self.__qtable_load_count = self.qtable_count(self.__qtable, self.__visible_lines_above)
        with lzma.open(qtable_filename + ".tmp", 'wb') as file:
            pickle.dump(self.__qtable, file)
        shutil.move(qtable_filename + ".tmp", qtable_filename)
        with open(score_filename, 'a+') as file:
            history = "\n".join(map(str, self.__score_history))
            file.write(f'{history}\n')
            self.__score_history = []
        print("Qtable saved")

    def set_qtable(self, qtable: dict):
        self.__qtable = qtable

    def get_qtable_state(self, qtable: dict, environment: [str], visible_lines_above: int) -> Dict[str, float]:
        if visible_lines_above == 0:
            if len(qtable) == 0:
                for action in ACTION_MOVES:
                    qtable[action] = 0
                # qtable = {action: 0 for action in ACTION_MOVES}
            return qtable
        elif environment[0] not in qtable:
            qtable[environment[0]] = {}
        return self.get_qtable_state(qtable[environment[0]], environment[1:], visible_lines_above - 1)

    def update_qtable_state(self, environment: [str], max_q: float,
                            reward: float,
                            action: str):
        qtable = self.get_qtable_state(self.__qtable, environment, self.__visible_lines_above)
        qtable[action] += self.__alpha * (reward + self.__gamma * max_q - qtable[action])
        self.increment_step_count()

    def print_stats(self, time_elapsed: int):
        print("--------------------------------")
        print(
            f"Agent win average is : {round(self.win_average() * 100, 3)}% "
            f"({self.__win_count} wins /"
            f" {self.__loose_count} looses)")
        print(f"Speed : {round(self.step_count / time_elapsed, 1)} step/s")
        print("--------------------------------")
        self.__win_count = 0
        self.__loose_count = 0

    def increment_step_count(self):
        self.__step_count += 1

    def save_score(self, score: float):
        self.__score_history_temp.append(score)
        if score > 0:
            self.__win_count += 1
        else:
            self.__loose_count += 1
        if len(self.__score_history_temp) >= self.__qtable_history_packets:
            self.__score_history.append(sum(self.__score_history_temp) / len(self.__score_history_temp))
            self.__score_history_temp = []

    def win_average(self) -> float:
        if self.__win_count + self.__loose_count == 0:
            return 0
        return float(self.__win_count) / (self.__win_count + self.__loose_count)

    def loose_count(self) -> int:
        return self.__loose_count

    def win_count(self) -> int:
        return self.__win_count

    def best_score(self) -> float:
        return max(self.__score_history)

    def qtable_count(self, qtable: dict, line_above: int) -> int:
        if line_above == 1:
            return len(qtable)
        return sum([self.qtable_count(qtable[key], line_above - 1) for key in qtable.keys()])

    def qtable_clear_empty(self, qtable: dict, line_above: int):
        if line_above == 1:
            to_delete = []
            for key, state in qtable.items():
                if all(action == 0 for action in state.values()):
                    to_delete.append(key)
            for key in to_delete:
                qtable.pop(key)
            return
        [self.qtable_clear_empty(qtable[key], line_above - 1) for key in qtable.keys()]

    @property
    def score_history(self):
        return self.__score_history

    @property
    def step_count(self) -> int:
        return self.__step_count

    @property
    def visible_lines_above(self) -> int:
        return self.__visible_lines_above

    @property
    def qtable(self) -> {}:
        return self.__qtable
