import os
from typing import Dict

from dotenv import dotenv_values


def load_env() -> Dict[str, str | float | int | bool]:
    env = dict(dotenv_values(".env"))
    if 'AGENT_LEARNING_RATE' not in env:
        env['AGENT_LEARNING_RATE'] = os.getenv('AGENT_LEARNING_RATE', 0.6)
    if 'AGENT_GAMMA' not in env:
        env['AGENT_GAMMA'] = os.getenv('AGENT_GAMMA', 0.8)
    if 'AGENT_LEARNING_FILE' not in env:
        env['AGENT_LEARNING_FILE'] = os.getenv('AGENT_LEARNING_FILE', 'qtable/qtable.data')
    if 'AGENT_VISIBLE_LINES_ABOVE' not in env:
        env['AGENT_VISIBLE_LINES_ABOVE'] = os.getenv('AGENT_VISIBLE_LINES_ABOVE', 2)
    if 'AGENT_VISIBLE_COLS_ARROUND' not in env:
        env['AGENT_VISIBLE_COLS_ARROUND'] = os.getenv('AGENT_VISIBLE_COLS_ARROUND', 20)
    if 'AGENT_QTABLE_HISTORY' not in env:
        env['AGENT_QTABLE_HISTORY'] = os.getenv('AGENT_QTABLE_HISTORY', 2)
    if 'LEARNING_TIME' not in env:
        env['LEARNING_TIME'] = os.getenv('LEARNING_TIME', 10)
    if 'LEARNING_MODE' not in env:
        env['LEARNING_MODE'] = os.getenv('LEARNING_MODE', 'true')
    if 'AGENT_DEBUG' not in env:
        env['AGENT_DEBUG'] = os.getenv('AGENT_DEBUG', 'false')

    env['AGENT_LEARNING_RATE'] = float(env['AGENT_LEARNING_RATE'])
    env['AGENT_GAMMA'] = float(env['AGENT_GAMMA'])
    env['AGENT_VISIBLE_LINES_ABOVE'] = int(env['AGENT_VISIBLE_LINES_ABOVE'])
    env['AGENT_VISIBLE_COLS_ARROUND'] = int(env['AGENT_VISIBLE_COLS_ARROUND'])
    env['AGENT_QTABLE_HISTORY'] = int(env['AGENT_QTABLE_HISTORY'])
    env['LEARNING_TIME'] = int(env['LEARNING_TIME'])
    env['LEARNING_MODE'] = env['LEARNING_MODE'].lower() == 'true'
    env['AGENT_DEBUG'] = env['AGENT_DEBUG'].lower() == 'true'
    print(env)
    return env