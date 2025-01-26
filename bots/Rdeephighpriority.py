from typing import Optional
from schnapsen.game import Bot, PlayerPerspective, Move, GameState, GamePlayEngine, Marriage
import random

from rand import RandBot


class RdeephighpriorityBot(Bot):
    """
    Rdeep bot is a bot which performs many random rollouts of the game to decide which move to play,
    prioritizing high-value cards.
    """
    def _init_(self, num_samples: int, depth: int, rand: random.Random, name: Optional[str] = None) -> None:
        super()._init_(name)
        assert num_samples >= 1, f"we cannot work with less than one sample, got {num_samples}"
        assert depth >= 1, f"it does not make sense to use a depth < 1, got {depth}"
        self.__num_samples = num_samples
        self.__depth = depth
        self.__rand = rand

    def get_move(self, perspective: PlayerPerspective, leader_move: Optional[Move]) -> Move:
        # Define custom rank order for Schnapsen
        rank_order = {
            "ACE": 11,
            "TEN": 10,
            "KING": 4,
            "QUEEN": 3,
            "JACK": 2,
        }

        # Get the list of valid moves and sort them by rank order
        moves = perspective.valid_moves()
        moves.sort(key=lambda move: rank_order[str(move.card.rank)], reverse=True)

        best_score = float('-inf')
        best_move = None
        for move in moves:
            sum_of_scores = 0.0
            for _ in range(self.__num_samples):
                gamestate = perspective.make_assumption(leader_move=leader_move, rand=self.__rand)
                score = self.__evaluate(gamestate, perspective.get_engine(), leader_move, move)
                sum_of_scores += score
            average_score = sum_of_scores / self.__num_samples
            if average_score > best_score:
                best_score = average_score
                best_move = move
        assert best_move is not None, "We went over all the moves, selecting the one we expect to lead to the highest average score. Since there must have been at least one move at the start, this can never be None"
        return best_move


    def __evaluate(self, gamestate: GameState, engine: GamePlayEngine, leader_move: Optional[Move], my_move: Move) -> float:
        me: Bot
        leader_bot: Bot
        follower_bot: Bot

        if leader_move:
            # We know what the other bot played
            leader_bot = FirstFixedMoveThenBaseBot(RandBot(rand=self.__rand), leader_move)
            me = follower_bot = FirstFixedMoveThenBaseBot(RandBot(rand=self.__rand), my_move)
        else:
            # I am the leader bot
            me = leader_bot = FirstFixedMoveThenBaseBot(RandBot(rand=self.__rand), my_move)
            follower_bot = RandBot(self.__rand)

        new_game_state, _ = engine.play_at_most_n_tricks(game_state=gamestate, new_leader=leader_bot, new_follower=follower_bot, n=self.__depth)

        if new_game_state.leader.implementation is me:
            my_score = new_game_state.leader.score.direct_points
            opponent_score = new_game_state.follower.score.direct_points
        else:
            my_score = new_game_state.follower.score.direct_points
            opponent_score = new_game_state.leader.score.direct_points

        heuristic = my_score / (my_score + opponent_score)
        return heuristic


class FirstFixedMoveThenBaseBot(Bot):
    def _init_(self, base_bot: Bot, first_move: Move) -> None:
        self.first_move = first_move
        self.first_move_played = False
        self.base_bot = base_bot

    def get_move(self, perspective: PlayerPerspective, leader_move: Optional[Move]) -> Move:
        if not self.first_move_played:
            self.first_move_played = True
            return self.first_move
        return self.base_bot.get_move(perspective=perspective, leader_move=leader_move)