from typing import Dict, List, Tuple

from conf.config import ACTION_MOVES, WORLD_SCALING, random
from game.Player import Player
from game.utils import is_in_safe_zone_on_water, get_collisions
from game.world import World


class Game:
    def __init__(self, world: World, players: List[Player], player_init_state: Tuple[int, int],
                 env: Dict[str, str | float | int | bool], auto_start: bool = True, debug: bool = False):
        self.__env = env
        self.__world = world
        self.__players = players
        self.__player_init_state = player_init_state
        self.__auto_start = auto_start
        self.__debug = debug
        self.__i = 0

    def start(self):
        for player in self.__players:
            self.init_player(player)

    def init_player(self, player):
        self.__i = 0
        init_state = (self.__player_init_state[0],
                      random.randint(0 + self.__world.scaling, self.__world.width - 1 - self.__world.scaling))
        current_env = self.__world.get_current_environment(
            init_state,
            int(self.__env['AGENT_VISIBLE_LINES_ABOVE']),
            int(self.__env['AGENT_VISIBLE_COLS_ARROUND'])
        )
        player.init(
            self.__world,
            init_state,
            current_env
        )

    def step(self):
        self.__i += 1
        self.__world.update_entities()
        for player in self.__players:

            self.__water_entity_move(player)
            current_environment = self.__world.get_current_environment(
                player.state,
                self.__env['AGENT_VISIBLE_LINES_ABOVE'],
                self.__env['AGENT_VISIBLE_COLS_ARROUND']
            )
            action = player.best_move(current_environment)
            reward, new_state, new_environment, is_game_over = self.__world.step(
                player.state, ACTION_MOVES[action],
                player.world_entity)
            player.step(action, reward, new_state, new_environment)
            if is_game_over:
                if self.__debug:
                    print(
                        f"{'WIN' if player.score > 0 else 'LOSE'} ! "
                        f"Score : {round(player.score, 4)},\t\tlast state : {new_state}")
                player.save_score()
                if self.__auto_start:
                    self.init_player(player)
                else:
                    self.__game_over(player)

    def human_step(self, action: str):
        for player in filter(lambda player_f: player_f.is_human, self.__players):
            reward, new_state, environment, current_environment, is_game_over = self.__world.step(player.state,
                                                                                                  ACTION_MOVES[action],
                                                                                                  player.world_entity)
            player.step(action, reward, new_state, current_environment, environment)
            if is_game_over:
                self.init_player(player)

    def __water_entity_move(self, player):
        collisions = get_collisions(player.world_entity, player.state, self.__world.world_entity_matrix,
                                    WORLD_SCALING)
        if is_in_safe_zone_on_water(collisions):
            new_state = (player.state[0], player.state[1] + self.__world.get_world_line(player.state).move_factor)
            player.update_state(new_state,
                                self.__world.get_current_environment(new_state, self.__env['AGENT_VISIBLE_LINES_ABOVE'],
                                                                     self.__env['AGENT_VISIBLE_COLS_ARROUND']))

    def __game_over(self, player: Player):
        self.__players.remove(player)

    @property
    def world(self):
        return self.__world

    @property
    def players(self):
        return self.__players
