import random

from arcade import Sprite

from conf.config import *
from game.world import World, NewWorld


class WorldWindow(arcade.Window):
    def __init__(self, world: World):
        super().__init__(
            world.width * SPRITE_SIZE,
            world.height * SPRITE_SIZE,
            'REINFORCED FROG'
        )
        self.__world_sprites = None
        self.__entities_sprites = None
        self.__random = random.Random()
        self.__world = world

    def __rand(self, r: int):
        return self.__random.randrange(r, step=1)

    def __get_environment_sprite(self, state: tuple, world_entity: WorldEntity) -> Sprite:
        sprite = world_entity.sprite
        sprite.center_x = (state[1] * WORLD_SCALING + (world_entity.width / 2)) * SPRITE_SIZE / WORLD_SCALING
        sprite.center_y = (self.__world.height - state[0] - (world_entity.height / 2)) * SPRITE_SIZE
        return sprite

    def setup(self):
        self.__world_sprites = arcade.SpriteList()
        self.__entities_sprites = arcade.SpriteList()

        for state in self.__world.world_states:
            token = self.__world.get_world_token(state)
            world_entity = WORLD_ENTITIES[token]
            if world_entity is not None:
                sprite = self.__get_environment_sprite(state, world_entity)
                self.__world_sprites.append(sprite)

    def on_draw(self):
        arcade.start_render()
        self.__world_sprites.draw()
        self.__entities_sprites.draw()


class NewWorldWindow(arcade.Window):
    def __init__(self, world: NewWorld):
        super().__init__(
            int(world.width / WORLD_SCALING * SPRITE_SIZE),
            int(world.height / WORLD_SCALING * SPRITE_SIZE),
            'REINFORCED FROG'
        )
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

        for state in self.__world.world_states:
            world_entity: WorldEntity = self.__world.get_world_line_entity(state)
            if world_entity is not None:
                sprite = self.__get_environment_sprite(state, world_entity)
                self.__world_sprites.append(sprite)

        for state in self.__world.world_entities_states:
            world_entity: WorldEntity = self.__world.get_world_entity(state)
            if world_entity is not None:
                sprite = self.__get_environment_sprite(state, world_entity)
                self.__entities_sprites.append(sprite)

    def on_draw(self):
        arcade.start_render()
        self.__world_sprites.draw()
        self.__entities_sprites.draw()
