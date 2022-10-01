from arcade import Sprite

from display.entity.world_entity import WorldEntity
from game.Player import Player
from game.world import World


class Agent(Player):
    def init(self, world: World, intial_state: (int, int)):
        super().init(world, intial_state)

    def best_move(self) -> (int, int):
        super().best_move()

    def step(self, action: (int, int), reward: float, new_state: (int, int)):
        super().step(action, reward, new_state)

    @property
    def sprite(self) -> Sprite:
        return super().sprite()

    def world_entity(self) -> WorldEntity:
        return super().world_entity()

    @property
    def is_human(self) -> bool:
        return super().is_human()

    @property
    def state(self) -> (int, int):
        super().state()
