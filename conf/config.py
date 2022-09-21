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

WORLD = """
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
        }

    @property
    def get_rewards(self):
        return self.__rewards

    def get_reward(self, token):
        return self.__rewards[token]


# ARCADE

def get_sprite_resources(name: str, sprite_size: float = 0.5):
    return arcade.Sprite(f":resources:images/{name}.png", sprite_size)


def get_sprite_local(name: str, sprite_size: float = 0.5):
    return arcade.Sprite(f"../assets/sprite/{name}.png", sprite_size)


SPRITE_SIZE = 64

CAR_SPRITE = [get_sprite_local("car_1"), get_sprite_local("car_2")]
TRUCK_SPRITE = [
    {
        'FRONT': get_sprite_local("truck_head"),
        'BACK': get_sprite_local("truck_tail")
    }
]
EXIT_SPRITE = [get_sprite_local('grass')]
FROG_SPRITE = [get_sprite_local('frog')]
ROAD_SPRITE = [get_sprite_resources('topdown_tanks/tileGrass_roadEast')]
START_SPRITE = [get_sprite_local('grass')]
TURTLE_SPRITE = [get_sprite_local('turtle')]
WALL_SPRITE = [get_sprite_resources('tiles/stoneCenter')]
WATER_SPRITE = [get_sprite_resources('tiles/water')]
WOOD_SPRITE = [get_sprite_local('wood')]
