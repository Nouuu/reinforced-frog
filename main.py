import os
import time

import arcade
import keyboard as keyboard

from ai.Agent import Agent
from conf.config import WORLD_WIDTH, WORLD_HEIGHT, WORLD_SCALING, WORLD_LINES, AGENT_LEARNING_RATE, \
    AGENT_GAMMA, AGENT_LEARNING_FILE
from display.world_window import WorldWindow
from game.HumanPlayer import HumanPlayer
from game.game import Game
from game.world import World

if __name__ == '__main__':
    world = World(
        width=WORLD_WIDTH,
        height=WORLD_HEIGHT,
        scaling=WORLD_SCALING,
        world_lines=WORLD_LINES)

    player = HumanPlayer()
    agent = Agent(AGENT_LEARNING_RATE, AGENT_GAMMA)

    if os.path.exists(AGENT_LEARNING_FILE):
        agent.load(AGENT_LEARNING_FILE)

    game = Game(world, [agent], (112, 95), auto_start=True, debug=False)
    game.start()

    second_left = int(time.perf_counter()) + 10 * 60
    print(f"Agent start learning...\n{int(second_left - time.perf_counter()) // 60} minutes left")
    while time.perf_counter() < second_left:
        if keyboard.is_pressed('q'):
            break
        player_loose, game_over = game.step()
        # decrease second_left each second
        if int(second_left - time.perf_counter()) % 60 == 0:
            second_left -= 1
            print(f"{int(second_left - time.perf_counter()) // 60} minutes left")
        if player_loose:
            pass
            # print(f"Agent game over, {i} round left")

    best_score = sorted(agent.score_history, key=lambda score: score[1], reverse=True)[0]
    print(f"Agent best score is : {best_score}")

    window = WorldWindow(game)
    window.setup()
    arcade.run()

    agent.save(AGENT_LEARNING_FILE)
