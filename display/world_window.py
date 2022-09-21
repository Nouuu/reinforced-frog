import copy
import random

from conf.config import *
from game.world import World


class WorldWindow(arcade.Window):
    def __init__(self, world: World):
        super().__init__(
            world.width * SPRITE_SIZE,
            world.height * SPRITE_SIZE,
            'REINFORCED FROG'
        )
        self.__sprites = None
        self.__random = random.Random()
        self.__world = world

    def __rand(self, range: int):
        return self.__random.randrange(range, step=1)

    def __get_environment_sprite(self, state: tuple, sprites: []):
        sprite = copy.deepcopy(sprites[self.__rand(len(sprites))])
        sprite.center_x = (state[1] + 0.5) * SPRITE_SIZE
        sprite.center_y = (self.__world.height - state[0] - 0.5) * SPRITE_SIZE
        return sprite

    def __get_truck_sprite(self, state: tuple):
        previous_state = (state[0], state[1] - 1)
        if self.__world.get_token(previous_state) == TRUCK_TOKEN:
            sprite = copy.deepcopy(TRUCK_SPRITES['SPRITES'][self.__rand(len(TRUCK_SPRITES['SPRITES']))]['FRONT'])
        else:
            sprite = copy.deepcopy(TRUCK_SPRITES['SPRITES'][self.__rand(len(TRUCK_SPRITES['SPRITES']))]['BACK'])
        sprite.center_x = (state[1] + 0.5) * SPRITE_SIZE
        sprite.center_y = (self.__world.height - state[0] - 0.5) * SPRITE_SIZE
        return sprite

    def __get_truck_background_sprite(self, state: tuple):
        return self.__get_environment_sprite(state, TRUCK_SPRITES['BACKGROUNDS'])

    def setup(self):
        self.__sprites = arcade.SpriteList()

        for state in self.__world.states:
            token = self.__world.get_token(state)
            if token == ROAD_TOKEN:
                self.__sprites.append(self.__get_environment_sprite(state, ROAD_SPRITES))
            elif token == GROUND_TOKEN:
                self.__sprites.append(self.__get_environment_sprite(state, GROUND_SPRITES))
            elif token == WATER_TOKEN:
                self.__sprites.append(self.__get_environment_sprite(state, WATER_SPRITES))
            elif token == START_TOKEN:
                self.__sprites.append(self.__get_environment_sprite(state, START_SPRITES))
            elif token == EXIT_TOKEN:
                self.__sprites.append(self.__get_environment_sprite(state, EXIT_SPRITES))
            elif token == WALL_TOKEN:
                self.__sprites.append(self.__get_environment_sprite(state, WALL_SPRITES))
            elif token == CAR_TOKEN:
                self.__sprites.append(self.__get_environment_sprite(state, CAR_SPRITES['BACKGROUNDS']))
                self.__sprites.append(self.__get_environment_sprite(state, CAR_SPRITES['SPRITES']))
            elif token == TURTLE_TOKEN:
                self.__sprites.append(self.__get_environment_sprite(state, TURTLE_SPRITES['BACKGROUNDS']))
                self.__sprites.append(self.__get_environment_sprite(state, TURTLE_SPRITES['SPRITES']))
            elif token == WOOD_TOKEN:
                self.__sprites.append(self.__get_environment_sprite(state, WOOD_SPRITES['BACKGROUNDS']))
                self.__sprites.append(self.__get_environment_sprite(state, WOOD_SPRITES['SPRITES']))
            elif token == TRUCK_TOKEN:
                self.__sprites.append(self.__get_truck_background_sprite(state))
                self.__sprites.append(self.__get_truck_sprite(state))

    def on_draw(self):
        arcade.start_render()
        self.__sprites.draw()
