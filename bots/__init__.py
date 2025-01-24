"""Create a bot in a separate .py and import them here, so that one can simply import
it by from schnapsen.bots import MyBot.
"""
from .rand import RandBot
from .alphabeta import AlphaBetaBot
from .rdeep import RdeepBot
from .ml_bot import MLDataBot, MLPlayingBot, train_ML_model
from .gui.guibot import SchnapsenServer
from .minimax import MiniMaxBot
from .bully_bot import BullyBot
from .Minimaxhighpriority import MinimaxhighpriorityBot
from .Rdeephighpriority import RdeephighpriorityBot
from .TwoPhaseBot import TwoPhaseBot


__all__ = ["RandBot", "TwoPhaseBot", "AlphaBetaBot", "RdeepBot", "MLDataBot", "MLPlayingBot", "train_ML_model", "SchnapsenServer", "MiniMaxBot", "MinimaxhighpriorityBot", "BullyBot", "RdeephighpriorityBot"]
