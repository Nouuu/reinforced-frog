import arcade

from conf.config import WORLD, ENTITIES
from display.world_window import WorldWindow
from game.world import World

if __name__ == '__main__':
    world = World(WORLD, ENTITIES)

    window = WorldWindow(world)
    window.setup()
    arcade.run()
