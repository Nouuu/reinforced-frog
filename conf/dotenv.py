from typing import Dict

from dotenv import dotenv_values


def load_env() -> Dict[str, str | float | int | bool]:
    env = dict(dotenv_values(".env"))
    env['AGENT_LEARNING_FILE'] = env['AGENT_LEARNING_FILE']
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
