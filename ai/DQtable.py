from typing import Dict

from ai.Model import Model


class DeepQtable(Model):

    def __init__(self, alpha: float, gamma: float, score_history_packets: int, visible_lines_above: int,
                 visible_cols_arround: int, agent_width: int):
        self.__visible_lines = visible_lines_above + 2
        self.__visible_cols = visible_cols_arround * 2 + agent_width
        self.__state_size = self.__visible_lines * self.__visible_cols
        self.__action_size = 5  # U,D,L,R,N
        self.__alpha = alpha
        self.__gamma = gamma
        self.__qtable_history_packets = score_history_packets
        self.__score_history = []
        self.__score_history_temp = []
        self.__step_count = 0
        self.__win_count = 0
        self.__loose_count = 0

    def load(self, filename: str):
        super().load(filename)

    def save(self, qtable_filename: str, score_filename: str):
        super().save(qtable_filename, score_filename)

    def get_state_actions(self, state: [str]) -> Dict[str, float]:
        return super().get_state_actions(state)

    def update_state(self, state: [str], max_q: float, reward: float, action: str):
        super().update_state(state, max_q, reward, action)

    def print_stats(self, time_elapsed: int):
        super().print_stats(time_elapsed)

    def save_score(self, score: float):
        super().save_score(score)
