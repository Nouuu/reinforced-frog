import lzma
import pickle
import shutil
from typing import Dict

from ai.Model import Model
from ai.graph_exporter import rate
from conf.config import ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT, ACTION_NONE

lzma_filters = [
    {"id": lzma.FILTER_DELTA, "dist": 5},
    {"id": lzma.FILTER_LZMA2, "preset": 7 | lzma.PRESET_EXTREME},
]


class MultiQtable(Model):
    def __init__(self, alpha: float, gamma: float, score_history_packets: int, visible_lines_above: int):
        self.__visible_lines_above = visible_lines_above
        self.__qtable = {"UP": {}, "CENTER": {}, "DOWN": {}}
        self.__alpha = alpha
        self.__gamma = gamma
        self.__qtable_load_count = 0
        self.__score_history_packets = score_history_packets
        self.__score_history = []
        self.__score_history_temp = []
        self.__step_count = 0
        self.__win_count = 0
        self.__loose_count = 0
        self.__count = 0

    def load(self, filename: str):
        print(f'Loading Qtable from {filename}...')
        with lzma.LZMAFile(filename, "rb") as uncompressed:
            self.__qtable = pickle.load(uncompressed)
            self.__qtable_load_count = self.__qtable_count()
            self.__count = self.__qtable_load_count
        print(f'Qtable loaded, {self.__qtable_load_count} entries')

    def save(self, qtable_filename: str, score_filename: str):
        print(f'Qtable entries : {self.__qtable_count()}')
        if self.__qtable_load_count is not None:
            self.__qtable_clear_empty()
            print(
                f'New states since previous save: '
                f'{self.__qtable_count() - self.__qtable_load_count}\n'
                f'Saving stable...')
            self.__qtable_load_count = self.__qtable_count()
            self.__count = self.__qtable_load_count
        with lzma.open(qtable_filename + ".tmp", 'wb') as file:
            pickle.dump(self.__qtable, file)
        shutil.move(qtable_filename + ".tmp", qtable_filename)
        with open(score_filename, 'a+') as file:
            history = "\n".join(map(str, self.__score_history))
            file.write(f'{history}\n')
            self.__score_history = []
        print("Qtable saved")

    def get_state_actions(self, state: [str]) -> Dict[str, float]:
        actions = {}
        up_state = "\n".join(state[:self.__visible_lines_above])
        center_state = "\n".join(state[self.__visible_lines_above:self.__visible_lines_above + 1])
        down_state = "\n".join(state[self.__visible_lines_above + 1:self.__visible_lines_above + 2])
        if up_state not in self.__qtable["UP"]:
            self.__qtable["UP"][up_state] = {ACTION_UP: 0}
        up = self.__qtable["UP"][up_state]
        if center_state not in self.__qtable["CENTER"]:
            self.__qtable["CENTER"][center_state] = {
                ACTION_LEFT: 0, ACTION_RIGHT: 0, ACTION_NONE: 0}
        center = self.__qtable["CENTER"][center_state]
        if down_state not in self.__qtable["DOWN"]:
            self.__qtable["DOWN"][down_state] = {
                ACTION_DOWN: 0}
        down = self.__qtable["DOWN"][down_state]
        actions.update(up)
        actions.update(center)
        actions.update(down)
        return actions

    def update_state(self, state: [str], max_q: float,
                     reward: float,
                     action: str):
        qtable = self.get_state_actions(state)
        up_state = "\n".join(state[:self.__visible_lines_above])
        center_state = "\n".join(state[self.__visible_lines_above:self.__visible_lines_above + 1])
        down_state = "\n".join(state[self.__visible_lines_above + 1:self.__visible_lines_above + 2])
        if action == ACTION_UP:
            self.__qtable["UP"][up_state][action] = (1 - self.__alpha) * qtable[action] + self.__alpha * (reward + self.__gamma * max_q)
        elif action == ACTION_DOWN:
            self.__qtable["DOWN"][down_state][action] = (1 - self.__alpha) * qtable[action] + self.__alpha * (reward + self.__gamma * max_q)
        else:
            self.__qtable["CENTER"][center_state][action] = (1 - self.__alpha) * qtable[action] + self.__alpha * (reward + self.__gamma * max_q)

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
            self.__score_history.append(rate(self.__score_history_temp))
            self.__score_history_temp = []

    def __win_average(self) -> float:
        if self.__win_count + self.__loose_count == 0:
            return 0
        return float(self.__win_count) / (self.__win_count + self.__loose_count)

    def __qtable_count(self) -> int:
        return sum([len(qtable) for qtable in self.__qtable])

    def __qtable_clear_empty(self):
        to_delete = []
        for key, state in self.__qtable.items():
            if all(action == 0 for action in state.values()):
                to_delete.append(key)
        for key in to_delete:
            self.__qtable.pop(key)

    @property
    def win_rate(self) -> float:
        return round(self.__win_average() * 100, 2)

    @property
    def game_count(self) -> int:
        return self.__win_count + self.__loose_count

    @property
    def win_count(self) -> int:
        return self.__win_count

    @property
    def loose_count(self) -> int:
        return self.__loose_count

    @property
    def entries_count(self) -> int:
        return self.__count
