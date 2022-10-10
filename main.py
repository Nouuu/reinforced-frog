import os

import arcade

from ai.Agent import Agent
from conf.config import WORLD_WIDTH, WORLD_HEIGHT, WORLD_SCALING, WORLD_LINES, WORLD_ENTITIES, AGENT_LEARNING_RATE, \
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

    game = Game(world, [player, agent], (59, 50))
    game.start()

    window = WorldWindow(game)
    window.setup()
    arcade.run()

    agent.save(AGENT_LEARNING_FILE)
