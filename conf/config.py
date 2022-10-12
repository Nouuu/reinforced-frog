# WORLD
import arcade

from display.entity.world_entity import WorldEntity
from display.entity.world_line import WorldLine

CAR_TOKEN = 'C'
TRUCK_TOKEN = 'Z'
TURTLE_TOKEN = 'T'
REVERSED_CAR_TOKEN = 'RC'
REVERSED_TRUCK_TOKEN = 'RZ'
REVERSED_TURTLE_TOKEN = 'RT'
EXIT_TOKEN = 'E'
FROG_TOKEN = 'F'
FROG_IA_TOKEN = 'FIA'
ROAD_TOKEN = 'R'
START_TOKEN = 'S'
WALL_TOKEN = 'X'
WATER_TOKEN = 'W'
WOOD_TOKEN = 'O'
GROUND_TOKEN = 'G'
EMPTY_TOKEN = ' '

# ACTIONS
ACTION_UP = 'U'
ACTION_DOWN = 'D'
ACTION_LEFT = 'L'
ACTION_RIGHT = 'R'
ACTION_NONE = 'N'
ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT, ACTION_NONE]

ACTION_MOVES = {
    ACTION_NONE: (0, 0),
    ACTION_UP: (-1, 0),
    ACTION_DOWN: (1, 0),
    ACTION_LEFT: (0, -1),
    ACTION_RIGHT: (0, 1)
}

# LINE DIRECTIONS

DIRECTION_LEFT = -1
DIRECTION_RIGHT = 1
DIRECTION_NONE = 0

# REWARDS & STATES

REWARD_DEFAULT = -1
FORBIDDEN_STATES = [WALL_TOKEN, CAR_TOKEN, TRUCK_TOKEN, WATER_TOKEN, REVERSED_CAR_TOKEN, REVERSED_TRUCK_TOKEN]
WIN_STATES = [EXIT_TOKEN]


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

SCALE = 1
SPRITE_SIZE = 64 * SCALE


def get_sprite_resources(name: str, sprite_size: float = 0.5):
    return arcade.Sprite(f":resources:images/{name}.png", sprite_size * SCALE)


def get_sprite_local(name: str, sprite_size: float = 0.5):
    return arcade.Sprite(f"assets/sprite/{name}.png", sprite_size * SCALE)


# WORLD ENTITIES

ENTITIES: {str: WorldEntity} = {
    CAR_TOKEN: WorldEntity(1, 1, CAR_TOKEN, get_sprite_local("car_1", 0.65)),
    TRUCK_TOKEN: WorldEntity(2, 1, TRUCK_TOKEN, get_sprite_local("truck", 0.32)),
    TURTLE_TOKEN: WorldEntity(1, 1, TURTLE_TOKEN, get_sprite_local("turtle", 0.2)),
    REVERSED_CAR_TOKEN: WorldEntity(1, 1, REVERSED_CAR_TOKEN, get_sprite_local("car_1_reversed", 0.65)),
    REVERSED_TRUCK_TOKEN: WorldEntity(2, 1, REVERSED_TRUCK_TOKEN, get_sprite_local("truck_reversed", 0.32)),
    REVERSED_TURTLE_TOKEN: WorldEntity(1, 1, REVERSED_TURTLE_TOKEN, get_sprite_local("turtle_reversed", 0.2)),
    EXIT_TOKEN: WorldEntity(1, 1, EXIT_TOKEN, get_sprite_local('grass', 2)),
    FROG_TOKEN: WorldEntity(1, 1, FROG_TOKEN, get_sprite_local('frog', 0.12)),
    FROG_IA_TOKEN: WorldEntity(1, 1, FROG_IA_TOKEN, get_sprite_local('frog_ia', 0.12)),
    GROUND_TOKEN: WorldEntity(1, 1, GROUND_TOKEN, get_sprite_resources('tiles/stoneCenter')),
    ROAD_TOKEN: WorldEntity(1, 1, ROAD_TOKEN, get_sprite_resources('topdown_tanks/tileGrass_roadEast', 1)),
    START_TOKEN: WorldEntity(1, 1, START_TOKEN, get_sprite_local('grass', 2)),
    WALL_TOKEN: WorldEntity(1, 1, WALL_TOKEN, get_sprite_resources('tiles/stoneCenter')),
    WATER_TOKEN: WorldEntity(1, 1, WATER_TOKEN, get_sprite_resources('tiles/water')),
    WOOD_TOKEN: WorldEntity(1, 1, WOOD_TOKEN, get_sprite_local("wood", 0.21)),
}

# LINE ENTITIES

ROAD_ENTITIES: [WorldEntity] = [ENTITIES[TRUCK_TOKEN], ENTITIES[CAR_TOKEN]]
REVERSED_ROAD_ENTITIES: [WorldEntity] = [ENTITIES[REVERSED_TRUCK_TOKEN], ENTITIES[REVERSED_CAR_TOKEN]]
WATER_TUR_ENTITIES: [WorldEntity] = [ENTITIES[TURTLE_TOKEN]]
REVERSED_WATER_TUR_ENTITIES: [WorldEntity] = [ENTITIES[REVERSED_TURTLE_TOKEN]]
WATER_WOOD_ENTITIES: [WorldEntity] = [ENTITIES[WOOD_TOKEN]]
NO_ENTITIES: [WorldEntity] = []

# WORLD

WORLD_WIDTH = 180
WORLD_HEIGHT = 117
WORLD_SCALING = 9

# WORLD LINES

WORLD_LINES: [WorldLine] = [  # y

    WorldLine(WORLD_WIDTH, WORLD_SCALING, ENTITIES[EXIT_TOKEN], 0, 0, DIRECTION_NONE, 0, NO_ENTITIES),
    WorldLine(WORLD_WIDTH, WORLD_SCALING, ENTITIES[WATER_TOKEN], 0, 3, DIRECTION_LEFT, 0.045,
              REVERSED_WATER_TUR_ENTITIES),
    WorldLine(WORLD_WIDTH, WORLD_SCALING, ENTITIES[WATER_TOKEN], 0, 2, DIRECTION_LEFT, 0.045, WATER_WOOD_ENTITIES),
    WorldLine(WORLD_WIDTH, WORLD_SCALING, ENTITIES[WATER_TOKEN], 0, 1, DIRECTION_RIGHT, 0.045, WATER_WOOD_ENTITIES),
    WorldLine(WORLD_WIDTH, WORLD_SCALING, ENTITIES[WATER_TOKEN], 0, 3, DIRECTION_RIGHT, 0.045, WATER_TUR_ENTITIES),
    WorldLine(WORLD_WIDTH, WORLD_SCALING, ENTITIES[GROUND_TOKEN], 0, 0, DIRECTION_NONE, 0, NO_ENTITIES),
    WorldLine(WORLD_WIDTH, WORLD_SCALING, ENTITIES[ROAD_TOKEN], 5, 1, DIRECTION_RIGHT, 0.02, ROAD_ENTITIES),
    WorldLine(WORLD_WIDTH, WORLD_SCALING, ENTITIES[ROAD_TOKEN], 5, 2, DIRECTION_LEFT, 0.02, REVERSED_ROAD_ENTITIES),
    WorldLine(WORLD_WIDTH, WORLD_SCALING, ENTITIES[GROUND_TOKEN], 0, 0, DIRECTION_NONE, 0, NO_ENTITIES),
    WorldLine(WORLD_WIDTH, WORLD_SCALING, ENTITIES[ROAD_TOKEN], 5, 2, DIRECTION_RIGHT, 0.02, ROAD_ENTITIES),
    WorldLine(WORLD_WIDTH, WORLD_SCALING, ENTITIES[ROAD_TOKEN], 5, 1, DIRECTION_LEFT, 0.02, REVERSED_ROAD_ENTITIES),
    WorldLine(WORLD_WIDTH, WORLD_SCALING, ENTITIES[ROAD_TOKEN], 5, 2, DIRECTION_RIGHT, 0.02, ROAD_ENTITIES),
    WorldLine(WORLD_WIDTH, WORLD_SCALING, ENTITIES[GROUND_TOKEN], 0, 0, DIRECTION_NONE, 0, NO_ENTITIES),
]

WORLD_ENTITIES = {
    (13, 18): ENTITIES[TURTLE_TOKEN],
    (13, 30): ENTITIES[TURTLE_TOKEN],
    (13, 50): ENTITIES[WOOD_TOKEN],
    (13, 59): ENTITIES[WOOD_TOKEN],
    (31, 4): ENTITIES[TRUCK_TOKEN],
    (31, 15): ENTITIES[CAR_TOKEN],
    (31, 24): ENTITIES[CAR_TOKEN],
    (31, 60): ENTITIES[REVERSED_CAR_TOKEN],
    (40, 20): ENTITIES[TRUCK_TOKEN],
    (40, 70): ENTITIES[CAR_TOKEN],
    (49, 50): ENTITIES[CAR_TOKEN],
}
