import random
from typing import Optional
from schnapsen.game import Bot, PlayerPerspective, Move

class HighValueRandBot(Bot):
    """This bot prioritizes high-value cards while making moves.

    Args:
        rand (random.Random): The random number generator used to make the choice of cards
        name (Optional[str]): The optional name of this bot
    """
    def __init__(self, rand: random.Random, name: Optional[str] = None) -> None:
        super().__init__(name)
        self.rng = rand

    def get_move(
        self,
        perspective: PlayerPerspective,
        leader_move: Optional[Move],
    ) -> Move:
        # Retrieve all valid moves
        moves: list[Move] = perspective.valid_moves()

        # Sort moves based on card value in descending order
        # Assuming Move.card.value gives the value of the card
        sorted_moves = sorted(moves, key=lambda move: move.card.value, reverse=True)

        # Introduce some randomness: prioritize high-value moves but occasionally pick a lower one
        if self.rng.random() < 0.8:  # 80% chance to pick the highest value move
            move = sorted_moves[0]
        else:
            move = self.rng.choice(sorted_moves)

        return move

    def __repr__(self) -> str:
        return f"HighValueRandBot(name={self.name})"
