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
    """
    It returns the set of all entities that the given entity is colliding with

    :param entity: WorldEntity - the entity we're checking for collisions
    :type entity: WorldEntity
    :param state: the current state of the entity
    :type state: tuple
    :param world_entity_matrix: a 2D matrix of strings representing the world
    :type world_entity_matrix: list[list[str]]
    :param scaling: The scaling of the world entity
    :type scaling: int
    :return: A set of the world entities that the entity is colliding with.
    """
    y = max(0, min(state[0], len(world_entity_matrix) - 1))
    entity_min_x = max(0, state[1])
    entity_max_x = min(state[1] + entity.width * scaling, len(world_entity_matrix[0]) - 1)
    return set(world_entity_matrix[y][entity_min_x:entity_max_x])


def is_in_safe_zone_on_water(collisions: [tuple]) -> bool:
    """
    If the water is not in the collisions list, and if the list contains at least one of the authorised states, then the
    player is in a safe zone

    :param collisions: [tuple]
    :type collisions: [tuple]
    :return: A boolean value.
    """
    return WATER_TOKEN not in collisions and any(token in collisions for token in WATER_AUTHORISED_STATES)


def is_win_state(collisions: [tuple]) -> bool:
    """
    > If any of the tokens in the collisions list are in the WIN_STATES list, return True, otherwise return False

    :param collisions: a list of tuples, each tuple representing a token that has collided with the player
    :type collisions: [tuple]
    :return: A boolean value.
    """
    for token in collisions:
        if token in WIN_STATES:
            return True
    return False


def slicer(a: list, lower: int, upper: int, step: int = 1) -> list:
    """
    It returns a list of elements from the list `a` starting at index `lower` and ending at index `upper` (exclusive), with
    a step size of `step`

    :param a: list
    :type a: list
    :param lower: The lower bound of the slice
    :type lower: int
    :param upper: The index of the element which is NOT in the returned list
    :type upper: int
    :param step: The number of items to skip between each item in the list, defaults to 1
    :type step: int (optional)
    :return: A list of the elements of a from lower to upper, with step as the step size.
    """
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
