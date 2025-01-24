from typing import Optional
from schnapsen.game import Bot, PlayerPerspective, Move, GamePhase
from schnapsen.bots.rand import RandBot
import random
from .rand import RandBot


class TwoPhaseBot(Bot):
    """
    A wrapper bot that delegates phase 1 to a RandBot and phase 2 to a MiniMax-based bot.
    """
    def __init__(self, phase_two_bot: Bot, rand: random.Random, name: Optional[str] = None) -> None:
        super().__init__(name)
        self.phase_one_bot = RandBot(rand=rand)
        self.phase_two_bot = phase_two_bot

    def get_move(self, perspective: PlayerPerspective, leader_move: Optional[Move]) -> Move:
        # Check the game phase and delegate to the appropriate bot
        if perspective.get_phase() == GamePhase.ONE:
            return self.phase_one_bot.get_move(perspective, leader_move)
        else:
            return self.phase_two_bot.get_move(perspective, leader_move)
