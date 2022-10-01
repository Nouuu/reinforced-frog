from conf.config import *


class World:
    def __init__(self,
                 width: int,
                 height: int,
                 scaling: int,
                 world: [WorldEntity],
                 world_entities: {tuple: WorldEntity}):
        self.__setup_world(width, height, scaling)
        self.__parse_world_lines(world)
        self.__parse_world_entities(world_entities)

    def __setup_world(self, width: int, height: int, scaling: int):
        self.__world_states: {(int, int): WorldEntity} = {}
        self.__world_entities_states: {(int, int): WorldEntity} = {}
        self.__rows = height
        self.__cols = width
        self.__scaling = scaling

    def __parse_world_lines(self, world: [WorldEntity]):
        for row in range(self.__scaling // 2, self.__rows, self.__scaling):
            for col in range(self.__scaling // 2, self.__cols, self.__scaling):
                state = (row, col)
                self.__world_states[state] = world[row // self.__scaling]

    def __parse_world_entities(self, world: {tuple: WorldEntity}):
        for state in world.keys():
            self.__world_entities_states[state] = world[state]

    def __is_forbidden_state(self, new_state) -> bool:
        return new_state not in self.__world_states

    def print(self):
        pass
        # print('Player position: {}'.format(self.__player_state))
        # print('Player collisions :')
        # print('From ground :\n-------------------')
        # for state in get_collisions(self.__player, self.__player_state, self.__world_states,
        #                             self.__world_entities_states,
        #                             self.__scaling):
        #     if state in self.__world_states:
        #         print(state, '->', self.__world_states[state].token)
        #
        # print('-------------------\nFrom entities :')
        # for state in get_collisions(self.__player, self.__player_state, self.__world_states,
        #                             self.__world_entities_states,
        #                             self.__scaling):
        #     if state in self.__world_entities_states:
        #         print(state, '->', self.__world_entities_states[state].token)
        #
        # print('-------------------\nIs in safe zone :')
        # print(
        #     is_in_safe_zone_on_water(self.__player, self.__player_state, self.__world_entities_states, self.__scaling))

    def get_world_line_entity(self, state: (int, int)) -> WorldEntity | None:
        if state in self.__world_states:
            return self.__world_states[state]
        return None

    def get_world_entity(self, state: (int, int)) -> WorldEntity | None:
        if state in self.__world_entities_states:
            return self.__world_entities_states[state]
        return None

    def step(self, state: (int, int), action: (int, int)) -> (float, (int, int)):
        new_state = (state[0] + action[0], state[1] + action[1])
        if self.__is_forbidden_state(new_state):
            return -1, state
        return 0, new_state

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
