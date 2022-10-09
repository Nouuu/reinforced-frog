import arcade

from ai.Agent import Agent
from conf.config import WORLD_WIDTH, WORLD_HEIGHT, WORLD_SCALING, WORLD_LINES, WORLD_ENTITIES
from display.world_window import WorldWindow
from game.HumanPlayer import HumanPlayer
from game.game import Game
from game.world import World

if __name__ == '__main__':
    world = World(
        width=WORLD_WIDTH,
        height=WORLD_HEIGHT,
        scaling=WORLD_SCALING,
        world=WORLD_LINES,
        world_entities=WORLD_ENTITIES)

    player = HumanPlayer()
    agent = Agent()

    game = Game(world, [player, agent], (13, 50))
    game.start()

    window = WorldWindow(game)
    window.setup()
    arcade.run()
