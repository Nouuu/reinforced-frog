from typing import Dict


class Model:
    def load(self, filename: str):
        pass

    def save(self, qtable_filename: str, score_filename: str):
        pass

    def get_state_actions(self, state: [str]) -> Dict[str, float]:
        pass

    def update_state(self, state: [str], max_q: float, reward: float, action: str):
        pass

    def print_stats(self, time_elapsed: int):
        pass

    def save_score(self, score: float):
        pass
