import lzma
import pickle
import shutil
from typing import Dict

from sklearn.neural_network import MLPRegressor

from ai.Model import Model
from ai.utils import state_to_vector
from conf.config import ACTIONS, ACTIONS_INDEX


class DeepQtable(Model):

    def __init__(self, score_history_packets: int, visible_lines_above: int,
                 visible_cols_arround: int, agent_width: int, reward_divisor: int, alpha: float = 0.01,
                 gamma: float = 0.1):
        self.__mlp: MLPRegressor = None
        self.__visible_lines = visible_lines_above + 2
        self.__visible_cols = visible_cols_arround * 2 + agent_width
        self.__state_size = self.__visible_lines * self.__visible_cols
        self.__action_size = len(ACTIONS)  # U,D,L,R,N
        self.__alpha = alpha
        self.__gamma = gamma
        self.__reward_divisor = reward_divisor
        self.__score_history_packets = score_history_packets
        self.__score_history = []
        self.__score_history_temp = []
        self.__temp_qvector = []
        self.__current_state_vector = []
        self.__current_state_qvector = []
        self.__step_count = 0
        self.__win_count = 0
        self.__loose_count = 0
        self.__state_vector_association = {}
        self.__init_mlp()

    def __init_mlp(self):
        self.__mlp = MLPRegressor(
            hidden_layer_sizes=1000,
            activation='tanh',
            solver='sgd',
            learning_rate_init=self.__alpha,
            max_iter=1,
            warm_start=True
        )

        self.__mlp.fit([[0] * self.__state_size], [[0] * self.__action_size])

    def load(self, filename: str):
        print(f'Loading model from {filename}...')
        with lzma.LZMAFile(filename, 'rb') as uncompressed:
            self.__mlp = pickle.load(uncompressed)
        print('Model loaded')

    def save(self, qtable_filename: str, score_filename: str):
        print(f'Saving model to {qtable_filename}...')
        with lzma.open(qtable_filename + ".tmp", 'wb') as file:
            pickle.dump(self.__mlp, file)
        shutil.move(qtable_filename + ".tmp", qtable_filename)
        with open(score_filename, 'a+') as file:
            history = "\n".join(map(str, self.__score_history))
            file.write(f'{history}\n')
            self.__score_history = []
        print('Model saved')

    def get_state_actions(self, state: [str]) -> Dict[str, float]:

        self.__current_state_vector = self.__get_vector_state(state)
        actions = self.__mlp.predict([self.__current_state_vector])[0]
        self.__current_state_qvector = actions
        return {ACTIONS[i]: value for i, value in enumerate(actions)}

    def update_state(self, state: [str], max_q: float, reward: float, action: str):

        action_effect = reward / self.__reward_divisor + self.__gamma * max_q

        self.__current_state_qvector[ACTIONS_INDEX[action]] = action_effect  # / self.__reward_divisor
        self.__temp_qvector.append((self.__current_state_vector, self.__current_state_qvector))
        if len(self.__temp_qvector) >= 10000:
            self.__mlp.fit([x[0] for x in self.__temp_qvector], [x[1] for x in self.__temp_qvector])
            self.__temp_qvector = []

        # self.__mlp.fit([state_to_vector(state)], [qvector])
        self.__increment_step_count()

    def __get_vector_state(self, state: [str]) -> [float]:
        state_str = "".join(state)
        if state_str not in self.__state_vector_association:
            self.__state_vector_association[state_str] = state_to_vector(state_str)
        return self.__state_vector_association[state_str]

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

    def save_score(self, score: float):
        self.__score_history_temp.append(score)
        if score > 0:
            self.__win_count += 1
        else:
            self.__loose_count += 1
        if len(self.__score_history_temp) >= self.__score_history_packets:
            self.__score_history.append(sum(self.__score_history_temp) / len(self.__score_history_temp))
            self.__score_history_temp = []

    def __increment_step_count(self):
        self.__step_count += 1

    def __win_average(self) -> float:
        if self.__win_count + self.__loose_count == 0:
            return 0
        return float(self.__win_count) / (self.__win_count + self.__loose_count)

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
