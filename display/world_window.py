import random

from arcade import Sprite

from conf.config import *
from game.game import Game


class WorldWindow(arcade.Window):
    def __init__(self, game: Game):
        super().__init__(
            int(game.world.width / WORLD_SCALING * SPRITE_SIZE),
            int(game.world.height / WORLD_SCALING * SPRITE_SIZE),
            'REINFORCED FROG'
        )
        self.__players_sprites = None
        self.__world_sprites = None
        self.__entities_sprites = None
        self.__random = random.Random()
        self.__game = game

    def __rand(self, r: int):
        return self.__random.randrange(r, step=1)

    def __get_environment_sprite(self, state: tuple, world_entity: WorldEntity) -> Sprite:
        sprite = world_entity.sprite
        sprite.center_x, sprite.center_y = self.__get_xy_state(state)
        return sprite

    def __get_xy_state(self, state: tuple) -> tuple:
        return (
            (state[1] + 0.5) / WORLD_SCALING * SPRITE_SIZE,
            (self.__game.world.height - state[0] - 0.5) / WORLD_SCALING * SPRITE_SIZE
        )

    def setup(self):
        self.setup_world_states()
        self.setup_players_states()
        self.setup_world_entities_state()

    def setup_world_entities_state(self):
        self.__entities_sprites = arcade.SpriteList()
        for state in self.__game.world.world_entities_states:
            world_entity: WorldEntity = self.__game.world.get_world_entity(state)
            if world_entity is not None:
                sprite = self.__get_environment_sprite(state, world_entity)
                self.__entities_sprites.append(sprite)

    def setup_world_states(self):
        self.__world_sprites = arcade.SpriteList()
        for state in self.__game.world.world_states:
            world_entity: WorldEntity = self.__game.world.get_world_line_entity(state)
            if world_entity is not None:
                sprite = self.__get_environment_sprite(state, world_entity)
                self.__world_sprites.append(sprite)

    def setup_players_states(self):
        self.__players_sprites = arcade.SpriteList()
        for player in self.__game.players:
            sprite = player.sprite
            sprite.center_x, sprite.center_y = self.__get_xy_state(player.state)
            self.__players_sprites.append(sprite)

    def on_draw(self):
        arcade.start_render()
        self.__world_sprites.draw()
        self.__entities_sprites.draw()
        self.__players_sprites.draw()

    def on_update(self, delta_time: float):
        self.__game.step()
        self.setup_players_states()
        self.__players_sprites.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
            self.__game.human_step(ACTION_MOVES[ACTION_LEFT])
        elif symbol == arcade.key.RIGHT:
            self.__game.human_step(ACTION_MOVES[ACTION_RIGHT])
        elif symbol == arcade.key.UP:
            self.__game.human_step(ACTION_MOVES[ACTION_UP])
        elif symbol == arcade.key.DOWN:
            self.__game.human_step(ACTION_MOVES[ACTION_DOWN])
