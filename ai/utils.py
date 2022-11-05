import os
import pickle
from typing import Set, Dict

from ai.Qtable import Qtable
from conf.config import ACTIONS, ACTIONS_INDEX


def get_qtable_files(directory: str) -> Set[str]:
    return {os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith('.data')}


def merge_qtables(qtable_files: Set[str]) -> Dict[bytes, Dict[str, float]]:
    qtable = {}
    for filename in qtable_files:
        with open(filename, 'rb') as file:
            current_qtable: Dict[bytes, Dict[str, float]] = pickle.load(file)
            for key, value in current_qtable.items():
                if key not in qtable:
                    qtable[key] = value
                else:
                    for action, qvalue in value.items():
                        if qvalue == 0:
                            pass
                        if qtable[key][action] == 0:
                            qtable[key][action] = qvalue
                        else:
                            qtable[key][action] = (qtable[key][action] + qvalue) / 2
    return qtable


def state_to_vector(state: str) -> [float]:
    """
    It converts a string into a list of floats, where each float is the ASCII value of the character divided by 255

    :param state: The current state of the game
    :type state: str
    :return: A list of floats, where each float is the ASCII value of a character in the state string, divided by 255.
    """
    return list(map(lambda char: float(ord(char)) / 255, [char for char in state]))


def qtable_to_ml_model(qtable: Qtable) -> ([[float]], [[float]]):
    ml_vectors = []
    ml_qvalues = []
    print('Converting qtable to ml model...')
    print('Getting all states...')
    states = get_all_states(qtable.qtable)
    print(f'Found {len(states)} states, converting to vectors...')
    for state in states:
        vector = state_to_vector(state)
        actions = qtable.get_state_actions(state)
        actions_array = [0.] * len(ACTIONS)
        for action, qvalue in actions.items():
            actions_array[ACTIONS_INDEX[action]] = qvalue
        ml_vectors.append(vector)
        ml_qvalues.append(actions_array)

    return ml_vectors, ml_qvalues


def get_all_states(qtable: dict) -> [str]:
    states = []
    for key, value in qtable.items():
        if len(key) > 1:
            for state in get_all_states(qtable[key]):
                states.append(key + state)
        else:
            return ['']
    return states
