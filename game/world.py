from typing import Tuple, List, Dict
from conf.config import WorldEntity
from game.Position import Position
from game.utils import get_positions


class World:
    def __init__(
        self,
        width: int,
        height: int,
        scaling: int,
        world: List[WorldEntity],
        world_entities: {Tuple[int, int]: WorldEntity}
    ):
        self.__setup_world(width, height, scaling)
        self.__parse_world_lines(world)
        self.__parse_world_entities(world_entities)

    def __setup_world(self, width: int, height: int, scaling: int):
        self.__world_states: Dict[Tuple[int, int]: WorldEntity] = {}
        self.__world_entities_states: Dict[Tuple[int, int]: WorldEntity] = {}
        self.__rows = height
        self.__cols = width
        self.__scaling = scaling

    def __parse_world_lines(self, world: List[WorldEntity]):
        for row in range(self.__scaling // 2, self.__rows, self.__scaling):
            for col in range(self.__scaling // 2, self.__cols, self.__scaling):
                state = (row, col)
                self.__world_states[state] = world[row // self.__scaling]

    def __parse_world_entities(self, world: {Tuple[int, int]: WorldEntity}):
        for state in world.keys():
            self.__world_entities_states[state] = world[state]

    def __is_forbidden_state(self, new_state, world_entity: WorldEntity) -> bool:
        for state in get_positions(new_state, world_entity, self.__scaling):
            if not 0 <= state[0] <= self.__rows or not 0 <= state[1] <= self.__cols:
                return True
        return False

    def get_world_line_entity(self, state: Tuple[int, int]) -> WorldEntity | None:
        if state in self.__world_states:
            return self.__world_states[state]
        return None

    def get_world_entity(self, state: Tuple[int, int]) -> WorldEntity | None:
        if state in self.__world_entities_states:
            return self.__world_entities_states[state]
        return None

    def step(self, state: Tuple[int, int], action: Tuple[int, int], world_entity: WorldEntity) -> Tuple[float, Tuple[int, int]]:
        new_state = (state[0] + action[0] * self.__scaling, state[1] + action[1] * self.__scaling // 3)
        if self.__is_forbidden_state(new_state, world_entity):
            return -self.__cols * self.__rows, state
        return -1, new_state

    def is_on_water(self, position: Position):
        # access line, know if lt's water, if it's water check if there is an entity
        print(self.__world_states)

    @property
    def world_states(self):
        return list(self.__world_states.keys())

    @property
    def world_entities_states(self):
        return list(self.__world_entities_states.keys())

    @property
    def height(self):
        return self.__rows

    @property
    def width(self):
        return self.__cols

    @property
    def scailing(self):
        return self.__scaling

