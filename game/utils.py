import itertools

from conf.config import WATER_TOKEN, WATER_AUTHORISED_STATES, WIN_STATES
from display.entity.world_entity import WorldEntity


# def get_positions(state: tuple, entity: WorldEntity, scaling: int) -> Set[tuple]:
#     positions = set()
#     for y in range((scaling * entity.height // 2 + scaling * entity.height % 2)):
#         for x in range((scaling * entity.width // 2 + scaling * entity.width % 2)):
#             positions.add((state[0] + y, state[1] + x))
#             positions.add((state[0] - y, state[1] + x))
#             positions.add((state[0] + y, state[1] - x))
#             positions.add((state[0] - y, state[1] - x))
#     return positions


def get_collisions(entity: WorldEntity, state: tuple, world_entity_matrix: list[list[str]], scaling: int) -> [tuple]:
    y = max(0, min(state[0], len(world_entity_matrix) - 1))
    entity_min_x = max(0, state[1])
    entity_max_x = min(state[1] + entity.width * scaling, len(world_entity_matrix[0]) - 1)
    return set(world_entity_matrix[y][entity_min_x:entity_max_x])


def is_in_safe_zone_on_water(collisions: [tuple]) -> bool:
    return WATER_TOKEN not in collisions and any(token in collisions for token in WATER_AUTHORISED_STATES)


def is_win_state(collisions: [tuple]) -> bool:
    for token in collisions:
        if token in WIN_STATES:
            return True
    return False


def slicer(a: list, lower: int, upper: int, step: int = 1) -> list:
    if lower < 0:
        lower += len(a)
    if upper < 0:
        upper += len(a)
    if upper < lower:
        return itertools.chain(a[lower::step], a[:upper:step])
    return a[lower:upper:step]

# def filter_states(states: Dict[Tuple[int, int], WorldEntity],
#                   scaling: int,
#                   min_line: int,
#                   max_line: int,
#                   min_col: int,
#                   max_col: int
#                   ) -> Dict[Tuple[int, int], WorldEntity]:
#     filtered_states = {}
#     for state in states.keys():
#         for position in get_positions(state, states[state], scaling):
#             if min_line <= position[0] < max_line and min_col <= position[1] < max_col:
#                 filtered_states[position] = states[state]
#     return filtered_states
