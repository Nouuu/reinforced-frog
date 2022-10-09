from conf.config import ACTION_MOVES
from game.Player import Player
from game.world import World


class Game:
    def __init__(self, world: World, players: [Player], player_init_state: (int, int)):
        self.__world = world
        self.__players = players
        self.__player_init_state = player_init_state

    def start(self):
        for player in self.__players:
            player.init(self.__world, self.__player_init_state,
                        self.__world.get_current_environment(self.__player_init_state[0], 3))

    def step(self):
        for player in self.__players:
            action = player.best_move()
            reward, new_state, environment, is_game_over = self.__world.step(player.state, ACTION_MOVES[action],
                                                                             player.world_entity)
            player.step(action, reward, new_state, environment)

    def human_step(self, action: (int, int)):
        for player in filter(lambda player_f: player_f.is_human, self.__players):
            reward, new_state, environment, is_game_over = self.__world.step(player.state, action, player.world_entity)
            player.step(action, reward, new_state, environment)
            break

    @property
    def world(self):
        return self.__world

    @property
    def players(self):
        return self.__players
