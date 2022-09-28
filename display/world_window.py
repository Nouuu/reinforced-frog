import random

from arcade import Sprite

from conf.config import *
from game.world import World


class WorldWindow(arcade.Window):
    def __init__(self, world: World):
        super().__init__(
            int(world.width / WORLD_SCALING * SPRITE_SIZE),
            int(world.height / WORLD_SCALING * SPRITE_SIZE),
            'REINFORCED FROG'
        )
        self.__player_sprite = None
        self.__world_sprites = None
        self.__entities_sprites = None
        self.__random = random.Random()
        self.__world = world

    def __rand(self, r: int):
        return self.__random.randrange(r, step=1)

    def __get_environment_sprite(self, state: tuple, world_entity: WorldEntity) -> Sprite:
        sprite = world_entity.sprite
        sprite.center_x, sprite.center_y = self.__get_xy_state(state)
        return sprite

    def __get_xy_state(self, state: tuple) -> tuple:
        return (
            (state[1] + 0.5) / WORLD_SCALING * SPRITE_SIZE,
            (self.__world.height - state[0] - 0.5) / WORLD_SCALING * SPRITE_SIZE
        )

    def setup(self):
        self.__world_sprites = arcade.SpriteList()
        self.__entities_sprites = arcade.SpriteList()
        self.__player_sprite = self.__get_environment_sprite(self.__world.player_state, self.__world.player)

        self.setup_world_states()
        self.setup_world_entities_state()

    def setup_world_entities_state(self):
        for state in self.__world.world_entities_states:
            world_entity: WorldEntity = self.__world.get_world_entity(state)
            if world_entity is not None:
                sprite = self.__get_environment_sprite(state, world_entity)
                self.__entities_sprites.append(sprite)

    def setup_world_states(self):
        for state in self.__world.world_states:
            world_entity: WorldEntity = self.__world.get_world_line_entity(state)
            if world_entity is not None:
                sprite = self.__get_environment_sprite(state, world_entity)
                self.__world_sprites.append(sprite)

    def on_draw(self):
        arcade.start_render()
        self.__world_sprites.draw()
        self.__entities_sprites.draw()
        self.__player_sprite.draw()
