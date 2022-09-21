# WORLD
import arcade

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

WORLD = """
XEEEEEX
XTWOOWX
XWWOTWX
XRCRRCX
XZZRZZX
XGGSGGX
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


ROAD_SPRITES = [get_sprite_resources('topdown_tanks/tileGrass_roadEast', 1)]
GROUND_SPRITES = [get_sprite_resources('topdown_tanks/tileGrass_roadEast', 1)]
WATER_SPRITES = [get_sprite_resources('tiles/water')]
EXIT_SPRITES = [get_sprite_local('grass', 2)]
START_SPRITES = [get_sprite_local('grass', 2)]
WALL_SPRITES = [get_sprite_resources('tiles/stoneCenter')]

FROG_SPRITES = [get_sprite_local('frog')]
CAR_SPRITES = {
    'SPRITES': [get_sprite_local("car_1"), get_sprite_local("car_2")],
    'BACKGROUNDS': ROAD_SPRITES
}

TRUCK_SPRITES = {
    'SPRITES': [{
        'FRONT': get_sprite_local("truck_head"),
        'BACK': get_sprite_local("truck_tail"),
    }],
    'BACKGROUNDS': ROAD_SPRITES
}

TURTLE_SPRITES = {
    'SPRITES': [get_sprite_local("turtle", 0.1)],
    'BACKGROUNDS': WATER_SPRITES
}

WOOD_SPRITES = {
    'SPRITES': [get_sprite_local("wood", 0.15)],
    'BACKGROUNDS': WATER_SPRITES
}
