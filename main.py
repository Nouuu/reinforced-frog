import os
import time

import arcade

from ai.Agent import Agent
from ai.qtable import get_qtable_files, merge_qtables
from conf.config import WORLD_WIDTH, WORLD_HEIGHT, WORLD_SCALING, WORLD_LINES
from conf.dotenv import load_env
from display.world_window import WorldWindow
from game.HumanPlayer import HumanPlayer
from game.game import Game
from game.world import World

if __name__ == '__main__':

    env = load_env()
    world = World(
        width=WORLD_WIDTH,
        height=WORLD_HEIGHT,
        scaling=WORLD_SCALING,
        world_lines=WORLD_LINES[env['WORLD_TYPE']],
        env=env)

    player = HumanPlayer()
    agent = Agent(float(env['AGENT_LEARNING_RATE']), float(env['AGENT_GAMMA']), float(env['EXPLORE_RATE']))

    if os.path.exists(env['AGENT_LEARNING_FILE']):
        agent.load(env['AGENT_LEARNING_FILE'])
    qtable_files = get_qtable_files('qtable')
    if len(qtable_files) > 1:
        print('Merging qtables...')
        agent.set_qtable(merge_qtables(qtable_files))

    players = [agent]
    if not env['LEARNING_MODE']:
        players.append(player)

    game = Game(world, players, (108, 90), auto_start=True, debug=env['AGENT_DEBUG'], env=env)
    game.start()

    if env['LEARNING_MODE']:
        second_left = int(time.perf_counter()) + int(env['LEARNING_TIME']) * 60
        start_time = time.perf_counter()
        print(f"Agent start learning...\n{int(second_left - time.perf_counter()) // 60 + 1} minutes left")
        while time.perf_counter() < second_left:
            # if keyboard.is_pressed('q'):
            #     break
            player_loose, game_over = game.step()
            if int(second_left - time.perf_counter()) % 60 == 0:
                second_left -= 1
                print(f"{int(second_left - time.perf_counter()) // 60 + 1} minutes left")
                print(
                    f"---\nAgent win average is : {round(agent.win_average() * 100, 3)}% ({agent.win_count()} wins / {agent.loose_count()} looses)")
                print(f"Speed : {round(agent.step_count / int(time.perf_counter() - start_time), 1)} step/s")
                agent.save(env['AGENT_LEARNING_FILE'])
                print("---")
    else:
        window = WorldWindow(game)
        window.setup()
        arcade.run()

    print(
        f"---\nAgent win average is : {round(agent.win_average() * 100, 3)}% ({agent.win_count()} wins / {agent.loose_count()} looses)")
    agent.save(env['AGENT_LEARNING_FILE'])
    print("---")
