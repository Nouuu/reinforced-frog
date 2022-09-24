# WORLD
import arcade

from display.entity.world_entity import WorldEntity

CAR_TOKEN = 'C'
TRUCK_TOKEN = 'Z'
EXIT_TOKEN = 'E'
FROG_TOKEN = 'F'
ROAD_TOKEN = 'R'
START_TOKEN = 'S'
TURTLE_TOKEN = 'T'
WALL_TOKEN = 'X'
WATER_TOKEN = 'W'
WOOD_TOKEN = 'O'
GROUND_TOKEN = 'G'
EMPTY_TOKEN = ' '

WORLD = """
G..G..G..G..G..G..G..
.....................
.....................
W..W..W..W..W..W..W..
.....................
.....................
R..R..R..R..R..R..R..
.....................
.....................
G..G..G..G..G..G..G..
.....................
.....................
"""

ENTITIES = """
.....................
.....................
.....................
T.........O.......O..
.....................
.....................
Z.......C......Z....
.....................
.....................
.....................
.....................
.....................
"""
# ACTIONS
ACTION_UP = 'U'
ACTION_DOWN = 'D'
ACTION_LEFT = 'L'
ACTION_RIGHT = 'R'
ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]

ACTION_MOVES = {ACTION_UP: (-1, 0),
                ACTION_DOWN: (1, 0),
                ACTION_LEFT: (0, -1),
                ACTION_RIGHT: (0, 1)}

# REWARDS & STATES

REWARD_DEFAULT = -1
FORBIDDEN_STATES = [WALL_TOKEN, CAR_TOKEN, TRUCK_TOKEN, WATER_TOKEN]


class Rewards:
    def __init__(self, maze_size: int):
        self.__rewards = {
            CAR_TOKEN: -2 * maze_size,
            TRUCK_TOKEN: -2 * maze_size,
            EXIT_TOKEN: maze_size,
            ROAD_TOKEN: REWARD_DEFAULT,
            START_TOKEN: REWARD_DEFAULT,
            TURTLE_TOKEN: REWARD_DEFAULT,
            WALL_TOKEN: -2 * maze_size,
            WATER_TOKEN: -2 * maze_size,
            WOOD_TOKEN: REWARD_DEFAULT,
            GROUND_TOKEN: REWARD_DEFAULT,
        }

    @property
    def get_rewards(self):
        return self.__rewards

    def get_reward(self, token):
        return self.__rewards[token]


# ARCADE

SCALE = 2
SPRITE_SIZE = 64 * SCALE


def get_sprite_resources(name: str, sprite_size: float = 0.5):
    return arcade.Sprite(f":resources:images/{name}.png", sprite_size * SCALE)


def get_sprite_local(name: str, sprite_size: float = 0.5):
    return arcade.Sprite(f"assets/sprite/{name}.png", sprite_size * SCALE)


# WORLD ENTITIES

WORLD_ENTITIES: {str: WorldEntity} = {
    CAR_TOKEN: WorldEntity(3, 3, CAR_TOKEN, get_sprite_local("car_1")),
    EXIT_TOKEN: WorldEntity(3, 3, EXIT_TOKEN, get_sprite_local('grass', 2)),
    FROG_TOKEN: WorldEntity(3, 3, FROG_TOKEN, get_sprite_local('frog')),
    GROUND_TOKEN: WorldEntity(3, 3, GROUND_TOKEN, get_sprite_resources('tiles/stoneCenter')),
    ROAD_TOKEN: WorldEntity(3, 3, ROAD_TOKEN, get_sprite_resources('topdown_tanks/tileGrass_roadEast', 1)),
    START_TOKEN: WorldEntity(3, 3, START_TOKEN, get_sprite_local('grass', 2)),
    TRUCK_TOKEN: WorldEntity(4, 3, TRUCK_TOKEN, get_sprite_local("truck")),
    TURTLE_TOKEN: WorldEntity(3, 3, TURTLE_TOKEN, get_sprite_local("turtle", 0.1)),
    WALL_TOKEN: WorldEntity(3, 3, WALL_TOKEN, get_sprite_resources('tiles/stoneCenter')),
    WATER_TOKEN: WorldEntity(3, 3, WATER_TOKEN, get_sprite_resources('tiles/water')),
    WOOD_TOKEN: WorldEntity(3, 3, WOOD_TOKEN, get_sprite_local("wood", 0.15)),
}

# WORLD

WORLD_WIDTH = 24
WORLD_HEIGHT = 18
WORLD_SCALING = 3

WORLD_LINES = {  # y
    1: WORLD_ENTITIES[GROUND_TOKEN],
    4: WORLD_ENTITIES[WATER_TOKEN],
    7: WORLD_ENTITIES[GROUND_TOKEN],
    10: WORLD_ENTITIES[ROAD_TOKEN],
    13: WORLD_ENTITIES[ROAD_TOKEN],
    16: WORLD_ENTITIES[GROUND_TOKEN],
}

WORLD_ENTITIES = {
    (4, 2): WORLD_ENTITIES[TURTLE_TOKEN],
    (4, 5): WORLD_ENTITIES[TURTLE_TOKEN],
    (4, 15): WORLD_ENTITIES[TURTLE_TOKEN],
    (10, 0): WORLD_ENTITIES[TRUCK_TOKEN],
    (10, 6): WORLD_ENTITIES[CAR_TOKEN],
    (10, 18): WORLD_ENTITIES[CAR_TOKEN],
    (10, 24): WORLD_ENTITIES[CAR_TOKEN],
    (13, 5): WORLD_ENTITIES[TRUCK_TOKEN],
    (13, 10): WORLD_ENTITIES[CAR_TOKEN],
    (13, 15): WORLD_ENTITIES[CAR_TOKEN],
}
