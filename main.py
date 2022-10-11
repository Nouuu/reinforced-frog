import os
import time

import arcade
import keyboard

from ai.Agent import Agent
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
        world_lines=WORLD_LINES,
        env=env)

    player = HumanPlayer()
    agent = Agent(env['AGENT_LEARNING_RATE'], env['AGENT_GAMMA'])

    if os.path.exists(env['AGENT_LEARNING_FILE']):
        agent.load(env['AGENT_LEARNING_FILE'])

    players = [agent]
    if not env['LEARNING_MODE']:
        players.append(player)

    game = Game(world, players, (112, 95), auto_start=True, debug=False, env=env)
    game.start()

    if env['LEARNING_MODE']:
        second_left = int(time.perf_counter()) + env['LEARNING_TIME'] * 60
        print(f"Agent start learning...\n{int(second_left - time.perf_counter()) // 60 + 1} minutes left")
        while time.perf_counter() < second_left:
            if keyboard.is_pressed('q'):
                break
            player_loose, game_over = game.step()
            # decrease second_left each second
            if int(second_left - time.perf_counter()) % 60 == 0:
                second_left -= 1
                print(f"{int(second_left - time.perf_counter()) // 60 + 1} minutes left")
            if player_loose:
                pass
                # print(f"Agent game over, {i} round left")

        best_score = sorted(agent.score_history, key=lambda score: score[1], reverse=True)[0]
        print(f"Agent best score is : {best_score}")
    else:
        window = WorldWindow(game)
        window.setup()
        arcade.run()

    agent.save(env['AGENT_LEARNING_FILE'])
