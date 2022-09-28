import arcade

from conf.config import WORLD_WIDTH, WORLD_HEIGHT, WORLD_SCALING, WORLD_LINES, WORLD_ENTITIES, FROG_TOKEN, ENTITIES
from display.world_window import WorldWindow
from game.world import World

if __name__ == '__main__':
    world = World(
        width=WORLD_WIDTH,
        height=WORLD_HEIGHT,
        scaling=WORLD_SCALING,
        world=WORLD_LINES,
        world_entities=WORLD_ENTITIES,
        player=((13, 50), ENTITIES[FROG_TOKEN])
    )

    world.print()

    window = WorldWindow(world)
    window.setup()
    arcade.run()
