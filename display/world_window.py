import arcade.color
from arcade import Sprite

from ai.Model import Model
from conf.config import *
from game.game import Game


class WorldWindow(arcade.Window):
    def __init__(self, game: Game, env, model: Model):
        super().__init__(
            int(game.world.width / WORLD_SCALING * SPRITE_SIZE),
            int(game.world.height / WORLD_SCALING * SPRITE_SIZE),
            'REINFORCED FROG',
            update_rate=1 / 60
        )
        self.__height = int(game.world.height / WORLD_SCALING * SPRITE_SIZE)
        self.__width = int(game.world.width / WORLD_SCALING * SPRITE_SIZE)
        self.__debug = 0
        self.__players_sprites = None
        self.__world_sprites = None
        self.__entities_sprites = None
        self.__random = random
        self.__game = game
        self.__env = env
        self.__model = model

    def __rand(self, r: int):
        return self.__random.randrange(r, step=1)

    def __get_environment_sprite(self, state: tuple, world_entity: WorldEntity) -> Sprite:
        sprite = world_entity.sprite
        sprite.left, sprite.top = self.__get_xy_state(state)
        return sprite

    def __get_entity_sprite(self, state: tuple, world_entity: WorldEntity) -> Sprite:
        sprite = world_entity.sprite
        sprite.left, sprite.center_y = self.__get_xy_state((state[0] + WORLD_SCALING // 2, state[1]))
        return sprite

    def __get_xy_state(self, state: tuple) -> tuple:
        return (
            (state[1]) / WORLD_SCALING * SPRITE_SIZE,
            (self.__game.world.height - state[0]) / WORLD_SCALING * SPRITE_SIZE
        )

    def setup(self):
        self.setup_world_states()
        self.setup_players_states()
        self.setup_world_entities_state()

    def setup_world_entities_state(self):
        self.__entities_sprites = arcade.SpriteList()
        for state in self.__game.world.world_entities_states.keys():
            world_entity: WorldEntity = self.__game.world.get_world_entity(state)
            if world_entity is not None:
                sprite = self.__get_entity_sprite(state, world_entity)
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
            sprite.center_x, sprite.center_y = (
                self.__get_xy_state((player.state[0] + WORLD_SCALING // 2, player.state[1] + WORLD_SCALING // 2)))
            self.__players_sprites.append(sprite)

    def __draw_debug(self):
        self.__players_sprites = arcade.SpriteList()
        for player in self.__game.players:
            state = self.__get_xy_state(player.state)
            arcade.draw_lrtb_rectangle_outline(state[0],
                                               state[0] + SPRITE_SIZE,
                                               state[1],
                                               state[1] - SPRITE_SIZE,
                                               arcade.color.BLUE, 5)
        for entity_state in self.__game.world.world_entities_states:
            state = self.__get_xy_state(entity_state)
            entity: WorldEntity = self.__game.world.get_world_entity(entity_state)
            arcade.draw_lrtb_rectangle_outline(state[0],
                                               state[0] + entity.width * SPRITE_SIZE,
                                               state[1],
                                               state[1] - entity.height * SPRITE_SIZE,
                                               arcade.color.RED, 5)

    def __draw_collisions_debug(self):
        for index_line, line in enumerate(self.__game.world.world_entity_matrix):
            if index_line < WORLD_HEIGHT:
                for index_col, entity in enumerate(line):
                    if index_col < WORLD_WIDTH:
                        if entity in FORBIDDEN_STATES:
                            x, y = self.__get_xy_state((index_line, index_col))
                            arcade.draw_lrtb_rectangle_filled(x, x + 1, y,
                                                              y - 1,
                                                              arcade.color.BLUE)

    def on_draw(self):
        arcade.start_render()
        self.__world_sprites.draw()
        self.__entities_sprites.draw()
        self.__players_sprites.draw()
        if self.__debug == 1:
            self.__draw_debug()
        elif self.__debug == 2:
            self.__draw_collisions_debug()
        if self.__env['ARCADE_INSIGHTS']:
            self.__draw_model_insights()

    def __draw_model_insights(self):
        arcade.draw_text(f"Model : ", 10, 815, arcade.color.WHITE, 12)
        arcade.draw_text(f"{self.__env['LEARNING_TYPE']}", 70, 815, arcade.color.WHITE, 12, bold=True)
        arcade.draw_text(f"Learning rate : {self.__env['AGENT_LEARNING_RATE']}", 10, 795, arcade.color.WHITE, 12)
        arcade.draw_text(f"Discount factor : {self.__env['AGENT_GAMMA']}", 10, 775, arcade.color.WHITE, 12)

        arcade.draw_text(f"Episodes : {self.__model.game_count}", 200, 815, arcade.color.WHITE, 12)
        arcade.draw_text(f"Win count :", 200, 795, arcade.color.WHITE, 12)
        arcade.draw_text(f"{self.__model.win_count}", 285, 795, arcade.color.APPLE_GREEN, 12, bold=True)
        arcade.draw_text(f"Loss count :", 200, 775, arcade.color.WHITE, 12)
        arcade.draw_text(f"{self.__model.loose_count}", 290, 775, arcade.color.RED, 12, bold=True)

        arcade.draw_text(f"Win average :", 350, 815, arcade.color.WHITE, 12)
        arcade.draw_text(f"{self.__model.win_rate}%", 455, 815, self.__win_rate_color(self.__model.win_rate), 12,
                         bold=True)
        if 'QLEARNING' in self.__env['LEARNING_TYPE']:
            arcade.draw_text(f"Qtable entries :", 350, 795, arcade.color.WHITE, 12)
            arcade.draw_text(f"{'{:,}'.format(self.__model.entries_count)}", 465, 795, arcade.color.WHITE, 12)

        arcade.draw_text(f"Visible lines above : {self.__env['AGENT_VISIBLE_LINES_ABOVE']}", 550, 815, arcade.color.WHITE, 12)
        arcade.draw_text(f"Visible columns arround : {self.__env['AGENT_VISIBLE_COLS_ARROUND']}", 550, 795, arcade.color.WHITE, 12)

    def __win_rate_color(self, win_rate: float):
        if win_rate < 35:
            return arcade.color.RED
        if win_rate < 75:
            return arcade.color.YELLOW
        return arcade.color.APPLE_GREEN

    def on_update(self, delta_time: float):
        self.__game.step()
        self.setup_players_states()
        self.__players_sprites.update()
        self.setup_world_entities_state()
        self.__entities_sprites.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
            self.__game.human_step(ACTION_LEFT)
        elif symbol == arcade.key.RIGHT:
            self.__game.human_step(ACTION_RIGHT)
        elif symbol == arcade.key.UP:
            self.__game.human_step(ACTION_UP)
        elif symbol == arcade.key.DOWN:
            self.__game.human_step(ACTION_DOWN)
        elif symbol == arcade.key.D:
            self.__debug = (self.__debug + 1) % 3
