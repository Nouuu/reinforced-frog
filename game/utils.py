from typing import Dict, Tuple, Set

from display.entity.world_entity import WorldEntity


def get_positions(state: tuple, entity: WorldEntity, scaling: int) -> Set[tuple]:
    positions = set()
    for y in range((scaling * entity.height // 2 + scaling * entity.height % 2)):
        for x in range((scaling * entity.width // 2 + scaling * entity.width % 2)):
            positions.add((state[0] + y, state[1] + x))
            positions.add((state[0] - y, state[1] + x))
            positions.add((state[0] + y, state[1] - x))
            positions.add((state[0] - y, state[1] - x))
    return positions


def get_collisions(entity: WorldEntity, state: tuple, world_entity_matrix: list[list[str]], scaling: int) -> [tuple]:
    collisions = set()
    entity_min_x = state[1] - entity.width * scaling // 2
    entity_max_x = state[1] + entity.width * scaling // 2
    for i in range(entity_min_x, entity_max_x):
        collisions.add(world_entity_matrix[state[0]][i])
    return collisions


def is_in_safe_zone_on_water(entity: WorldEntity, entity_state: tuple, world_entities: Dict[tuple, WorldEntity],
                             scaling: int) -> bool:
    state_positions = get_positions(entity_state, entity, scaling)

    entities_positions = set()
    for entity_state in world_entities.keys():
        for state in get_positions(entity_state, world_entities[entity_state], scaling):
            entities_positions.add(state)

    for pos in state_positions:
        if pos not in entities_positions:
            return False
    return True


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
