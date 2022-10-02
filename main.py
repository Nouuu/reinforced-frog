import arcade

from conf.config import WORLD_WIDTH, WORLD_HEIGHT, WORLD_SCALING, WORLD_LINES, FROG_TOKEN, ENTITIES
from display.world_window import WorldWindow
from game.HumanPlayer import HumanPlayer
from game.Position import Position
from game.game import Game
from game.world import World

if __name__ == '__main__':
    world = World(
        width=WORLD_WIDTH,
        height=WORLD_HEIGHT,
        scaling=WORLD_SCALING,
        world_lines=WORLD_LINES,
        player=((13, 50), ENTITIES[FROG_TOKEN])
    )

    player = HumanPlayer()

    position = Position(13, 50)
    game = Game(world, [player], position)
    game.start()

    window = WorldWindow(game)
    window.setup()
    arcade.run()
