from typing import Optional
from schnapsen.game import (
    Bot,
    Move,
    PlayerPerspective,
    GamePhase,
    GameState,
    FollowerPerspective,
    LeaderPerspective,
    GamePlayEngine,
    SchnapsenTrickScorer,
    Marriage,
)

class OneFixedMoveBot(Bot):
    """
    A helper bot that plays one fixed move.
    Once it plays the move, it cannot play another.
    """
    def __init__(self, move: Move) -> None:
        self.first_move: Optional[Move] = move  # Stores the fixed move

    def get_move(self, perspective: PlayerPerspective, leader_move: Optional[Move]) -> Move:
        # Ensure it has a move to play
        assert self.first_move, "This bot can only play one move; after that, it ends."
        move = self.first_move
        self.first_move = None  # Clear the move after it is played
        return move

class MinimaxhighpriorityBot(Bot):
    """
    A bot playing the minimax strategy in the second phase of the game.
    It cannot be used for the first phase. What you can do is delegate from your own bot to this one in the second phase.
    """

    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name)

    def get_move(self, perspective: PlayerPerspective, leader_move: Optional[Move]) -> Move:
        assert (perspective.get_phase() == GamePhase.TWO), "MiniMaxBot can only work in the second phase of the game."
        _, move = self.value(
            perspective.get_state_in_phase_two(),
            perspective.get_engine(),
            leader_move=leader_move,
            maximizing=True,
        )
        return move

    def value(
        self,
        state: GameState,
        engine: GamePlayEngine,
        leader_move: Optional[Move],
        maximizing: bool,
    ) -> tuple[float, Move]:
        """Get the score and the corresponding move which either maximizes or minimizes the objective."""

        my_perspective: PlayerPerspective
        if leader_move is None:
            # we are the leader
            my_perspective = LeaderPerspective(state, engine)
        else:
            my_perspective = FollowerPerspective(state, engine, leader_move)
        valid_moves = my_perspective.valid_moves()

        scorer = SchnapsenTrickScorer()

        # Sort moves based on card value, handling Marriage moves separately
        sorted_moves = sorted(
            valid_moves,
            key=lambda move: (
                scorer.rank_to_points(move.card.rank)  # Regular moves
                if not isinstance(move, Marriage) else  # If it's a Marriage
                (scorer.rank_to_points("King") + scorer.rank_to_points("Queen"))  # Marriage value
            ),
            reverse=True
        )

        best_value = float("-inf") if maximizing else float("inf")
        best_move: Optional[Move] = None
        for move in sorted_moves:
            leader: Bot
            follower: Bot
            if leader_move is None:
                # we are leader, call self to get the follower to play
                value, _ = self.value(
                    state=state,
                    engine=engine,
                    leader_move=move,
                    maximizing=not maximizing,
                )
            else:
                # We are the follower. We need to complete the trick and then call self to play the next trick
                leader = OneFixedMoveBot(leader_move)
                follower = OneFixedMoveBot(move)
                new_game_state = engine.play_one_trick(game_state=state, new_leader=leader, new_follower=follower)
                winning_info = SchnapsenTrickScorer().declare_winner(new_game_state)
                if winning_info:
                    winner = winning_info[0].implementation
                    points = winning_info[1]
                    follower_wins = winner == follower

                    if not follower_wins:
                        points = -points
                    if not maximizing:
                        points = -points
                    value = points
                else:
                    # play the next round by doing a recursive call
                    leader_stayed = leader == new_game_state.leader.implementation

                    if leader_stayed:
                        # At the next step, the leader is our opponent
                        next_maximizing = not maximizing
                    else:
                        # At the next step we will have become the leader
                        next_maximizing = maximizing
                    value, _ = self.value(new_game_state, engine, None, next_maximizing)
            if maximizing and value > best_value:
                best_move = move
                best_value = value
            elif not maximizing and value < best_value:
                best_move = move
                best_value = value
        assert best_move, "We are sure the best_move can no longer be None."
        return best_value, best_move
