def get_positions(state: tuple, scaling: int) -> [tuple]:
    positions = set()
    for i in range(scaling//2 + scaling % 2):
        for j in range(scaling//2 + scaling % 2):
            positions.add((state[0] + i, state[1] + j))
            positions.add((state[0] - i, state[1] + j))
            positions.add((state[0] + i, state[1] - j))
            positions.add((state[0] - i, state[1] - j))
    return positions


def get_collisions(state: tuple, world_state: [tuple], entities_state: [tuple], scaling: int) -> [tuple]:
    collisions = set()
    state_positions = get_positions(state, scaling)

    for entity in world_state:
        entity_positions = get_positions(entity, scaling)
        if any([any([pos in entity_positions for pos in state_positions])]):
            collisions.add(entity)
    for entity in entities_state:
        entity_positions = get_positions(entity, scaling)
        if any([any([pos in entity_positions for pos in state_positions])]):
            collisions.add(entity)

    return collisions
