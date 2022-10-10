import os

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

    game = Game(world, [agent], (112, 95), auto_start=True, debug=True)
    game.start()

    print("Agent start learning 100000 round")
    i = 100000
    while i > 0:
        if keyboard.is_pressed('q'):
            break
        player_loose, game_over = game.step()
        if player_loose:
            i -= 1
            print(f"Agent game over, {i} round left")

    best_score = sorted(agent.score_history, key=lambda score: score[1], reverse=True)[0]
    print(f"Agent best score is : {best_score}")

    window = WorldWindow(game)
    window.setup()
    arcade.run()

    agent.save(AGENT_LEARNING_FILE)
