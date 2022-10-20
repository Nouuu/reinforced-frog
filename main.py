import os
import time

import arcade

from ai.Agent import Agent
from ai.DQtable import DeepQtable
from ai.Qtable import Qtable
from ai.graph_exporter import extract_history
from conf.config import WORLD_WIDTH, WORLD_HEIGHT, WORLD_SCALING, WORLD_LINES
from conf.dotenv import load_env
from display.world_window import WorldWindow
from game.HumanPlayer import HumanPlayer
from game.game import Game
from game.world import World


def main():
    env = load_env()
    world = World(
        width=WORLD_WIDTH,
        height=WORLD_HEIGHT,
        scaling=WORLD_SCALING,
        world_lines=WORLD_LINES[env['WORLD_TYPE']],
        env=env)

    dqtable = DeepQtable(float(env['AGENT_LEARNING_RATE']), float(env['AGENT_GAMMA']), env['QTABLE_HISTORY_PACKETS'],
                         env['AGENT_VISIBLE_LINES_ABOVE'], env['AGENT_VISIBLE_COLS_ARROUND'], 9)

    qtable = Qtable(float(env['AGENT_LEARNING_RATE']), float(env['AGENT_GAMMA']), env['QTABLE_HISTORY_PACKETS'],
                    env['AGENT_VISIBLE_LINES_ABOVE'])

    player = HumanPlayer()
    players = []

    for i in range(env['AGENT_COUNT']):
        players.append(Agent(qtable, float(env['EXPLORE_RATE'])))

    load_qtable(qtable, env)
    if not env['LEARNING_MODE']:
        players.append(player)
        pass
    game = Game(world, players, (108, 90), auto_start=True, debug=env['AGENT_DEBUG'], env=env)
    game.start()

    start_time = time.perf_counter()
    if env['LEARNING_MODE']:
        learn_mode(qtable, env, game, start_time)
    else:
        arcade_mode(game)
    if env['LEARNING_MODE']:
        save_qtable(qtable, env)
        if env['GENERATE_HISTORY_GRAPH']:
            extract_history(env['QTABLE_HISTORY_FILE'], env)


def load_qtable(qtable: Qtable, env):
    if os.path.exists(env['AGENT_LEARNING_FILE']):
        qtable.load(env['AGENT_LEARNING_FILE'])
    # qtable_files = get_qtable_files('qtable')
    # if len(qtable_files) > 1:
    #     print('Merging qtables...')
    #     qtable.set_qtable(merge_qtables(qtable_files))


def save_qtable(qtable: Qtable, env):
    qtable.save(env['AGENT_LEARNING_FILE'], env['QTABLE_HISTORY_FILE'])


def arcade_mode(game):
    window = WorldWindow(game)
    window.setup()
    arcade.run()


def learn_mode(qtable: Qtable, env, game, start_time):
    second_left = int(time.perf_counter()) + int(env['LEARNING_TIME']) * 60
    print(f"Agent start learning...\n{int(second_left - time.perf_counter()) // 60 + 1} minutes left")
    while time.perf_counter() < second_left:
        game.step()
        remove_sec = 0
        if int(second_left - time.perf_counter()) % env['LEARNING_PRINT_STATS_EVERY'] == 0:
            print(f"{int(second_left - time.perf_counter()) // 60} minutes left")
            qtable.print_stats(int(time.perf_counter() - start_time))
            remove_sec = 1
        if int(second_left - time.perf_counter()) % env['LEARNING_SAVE_QTABLE_EVERY'] == 0:
            save_time = time.perf_counter()
            save_qtable(qtable, env)
            if env['GENERATE_HISTORY_GRAPH']:
                extract_history(env['QTABLE_HISTORY_FILE'], env)
            start_time += time.perf_counter() - save_time
            second_left += time.perf_counter() - save_time
            remove_sec = 1
        second_left -= remove_sec


if __name__ == '__main__':
    main()
