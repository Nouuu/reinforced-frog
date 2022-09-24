import arcade

from conf.config import WORLD_WIDTH, WORLD_HEIGHT, WORLD_SCALING, WORLD_LINES
from display.world_window import NewWorldWindow
from game.world import NewWorld

if __name__ == '__main__':
    world = NewWorld(
        width=WORLD_WIDTH,
        height=WORLD_HEIGHT,
        scaling=WORLD_SCALING,
        world=WORLD_LINES
    )

    world.print()

    window = NewWorldWindow(world)
    window.setup()
    arcade.run()
