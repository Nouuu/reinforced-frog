from conf.config import WATER_TOKEN, WATER_AUTHORISED_STATES
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
    collisions = set()
    entity_min_x = state[1]
    entity_max_x = min(state[1] + entity.width * scaling, len(world_entity_matrix[0]))
    for i in range(entity_min_x, entity_max_x):
        collisions.add(world_entity_matrix[state[0]][i])
    return collisions


def is_in_safe_zone_on_water(entity: WorldEntity, entity_state: tuple, world_entity_matrix: list[list[str]],
                             scaling: int) -> bool:
    collisions = get_collisions(entity, entity_state, world_entity_matrix, scaling)
    return not WATER_TOKEN in collisions and any(token in collisions for token in WATER_AUTHORISED_STATES)

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
