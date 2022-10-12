from typing import Dict, List, Tuple

from conf.config import ACTION_MOVES, WORLD_SCALING
from game.Player import Player
from game.utils import is_in_safe_zone_on_water
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
        current_env = self.__world.get_current_environment(
            self.__player_init_state,
            int(self.__env['AGENT_VISIBLE_LINES_ABOVE']),
            int(self.__env['AGENT_VISIBLE_COLS_ARROUND'])
        )
        player.init(
            self.__world,
            self.__player_init_state,
            current_env
        )

    def step(self) -> Tuple[bool, bool]:
        self.__i += 1
        self.__world.update_entities()
        game_over = False
        for player in self.__players:
            self.__water_entity_move(player)
            action = player.best_move()
            reward, new_state, environment, is_game_over = self.__world.step(
                player.state, ACTION_MOVES[action],
                player.world_entity
            )
            player.step(action, reward, new_state, environment)
            if self.__i % 100 == 0 and not player.is_human and self.__debug:
                print(
                    f"Score : {round(player.score, 4)}, \tlast state : {new_state}, q : {player.get_qtable_state(environment, new_state)}")

            game_over = game_over or is_game_over
            if is_game_over:
                if self.__debug:
                    print(f"Score : {round(player.score, 4)},\t\tlast state : {new_state}")
                player.save_score()
                if self.__auto_start:
                    self.init_player(player)
                else:
                    self.__game_over(player)

        return game_over, len(self.__players) > 0  # Return if there is still player in game and if the game is over

    def human_step(self, action: Tuple[int, int]):
        for player in filter(lambda player_f: player_f.is_human, self.__players):
            reward, new_state, environment, is_game_over = self.__world.step(player.state, action, player.world_entity)
            player.step(action, reward, new_state, environment)
            if is_game_over:
                self.init_player(player)

    def __water_entity_move(self, player):
        if is_in_safe_zone_on_water(player.world_entity, player.state, self.__world.world_entities_states,
                                    WORLD_SCALING):
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
