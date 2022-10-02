from typing import Tuple
from arcade import Sprite

from conf.config import ACTION_NONE, ENTITIES, FROG_TOKEN, ACTION_MOVES, ACTION_DOWN
from display.entity.world_entity import WorldEntity
from game.Player import Player
from game.Position import Position
from game.world import World


class HumanPlayer(Player):
    def __init__(self):
        self._position = Position(0, 0)

    def init(self, _world: World, position: Position):
        self._position = position

    def best_move(self) -> Tuple[int, int]:
        return ACTION_MOVES[ACTION_NONE]

    def step(self, action: Tuple[int, int], reward: float, new_position: Tuple[int, int]):
        self._position = Position(new_position[0], new_position[1])

    @property
    def sprite(self) -> Sprite:
        return ENTITIES[FROG_TOKEN].sprite

    @property
    def world_entity(self) -> WorldEntity:
        return ENTITIES[FROG_TOKEN]

    @property
    def state(self) -> Tuple[int, int]:
        return self._position.x, self._position.y
