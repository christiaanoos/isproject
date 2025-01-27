from typing import Optional
from schnapsen.game import (
    Bot,
    Move,
    PlayerPerspective,
    GamePhase,
    SchnapsenTrickScorer,
    Marriage,
)
import random


class RandhighpriorityBot(Bot):
    """
    A random bot with high card priority. The bot chooses a move randomly,
    but prioritizes high-value cards in its decision-making.
    """

    def __init__(self, name: Optional[str] = "RandhighpriorityBot") -> None:
        super().__init__(name)

    def get_move(self, perspective: PlayerPerspective, leader_move: Optional[Move]) -> Move:
        """
        Decide the next move to play.
        - Prioritizes moves involving high-value cards or marriages.
        - If multiple moves have the same priority, chooses randomly among them.

        Args:
            perspective (PlayerPerspective): The current player's perspective.
            leader_move (Optional[Move]): The move played by the leader, or None if the bot is the leader.

        Returns:
            Move: The selected move to play.
        """
        valid_moves = perspective.valid_moves()
        scorer = SchnapsenTrickScorer()

        # Sort moves based on value, prioritizing marriages and high-value cards
        sorted_moves = sorted(
            valid_moves,
            key=lambda move: self._calculate_move_priority(move, scorer),
            reverse=True
        )

        # Randomly choose among the top-priority moves
        top_priority = self._calculate_move_priority(sorted_moves[0], scorer)
        top_moves = [move for move in sorted_moves if self._calculate_move_priority(move, scorer) == top_priority]

        # Return a randomly chosen move from the top-priority list
        return random.choice(top_moves)

    def _calculate_move_priority(self, move: Move, scorer: SchnapsenTrickScorer) -> int:
        """
        Calculate the priority of a move.
        - For a regular move, priority is based on the card's rank value.
        - For a marriage, priority is the combined value of the King and Queen.

        Args:
            move (Move): The move to evaluate.
            scorer (SchnapsenTrickScorer): The trick scorer for determining card values.

        Returns:
            int: The priority value of the move.
        """
        if isinstance(move, Marriage):
            # Marriage priority is the sum of the King and Queen's values
            return scorer.rank_to_points("King") + scorer.rank_to_points("Queen")
        else:
            # Regular card priority is based on its rank value
            return scorer.rank_to_points(move.card.rank)
