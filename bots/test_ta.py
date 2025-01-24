import random
from schnapsen.game import SchnapsenGamePlayEngine, Bot
from schnapsen.bots.rdeep import RdeepBot
from schnapsen.bots.Rdeephighpriority import RdeephighpriorityBot 

def play_games(num_games: int, bot1: Bot, bot2: Bot) -> tuple[int, int]:
    engine = SchnapsenGamePlayEngine()
    bot1_wins = 0
    bot2_wins = 0

    for i in range(num_games):
        if i % 2 == 0:
            winner, _ = engine.play_game(bot1, bot2, rng=random.Random(i))
        else:
            winner, _ = engine.play_game(bot2, bot1, rng=random.Random(i))

        if winner is bot1:
            bot1_wins += 1
        else:
            bot2_wins += 1

        print(f"Game {i + 1}/{num_games}: Winner - {'Bot1' if winner is bot1 else 'Bot2'}")

    return bot1_wins, bot2_wins

# Set up the bots
random_seed = 42
num_samples = 100
depth = 5

rand = random.Random(random_seed)
bot1 = RdeepBot(num_samples=num_samples, depth=depth, rand=rand, name="RdeepBot")
bot2 = RdeephighpriorityBot(num_samples=num_samples, depth=depth, rand=rand, name="RdeephighpriorityBot")

# Play games
num_games = 100
bot1_wins, bot2_wins = play_games(num_games, bot1, bot2)

# Display results
print("\nRESULTS:")
print(f"RdeepBot wins: {bot1_wins}")
print(f"Rdeephighpriority wins: {bot2_wins}")
print(f"Winning percentage for RdeepBot: {bot1_wins / num_games * 100:.2f}%")
print(f"Winning percentage for Rdeephighpriority: {bot2_wins / num_games * 100:.2f}%")
random_seed = 42
bot1 = MinimaxhighpriorityBot(name="MinimaxhighpriorityBot")
bot2 = MiniMaxBot(name="MiniMaxBot")

# Play games
num_games = 100  # Number of games to play
bot1_wins, bot2_wins = play_games(num_games, bot1, bot2)

# Display results
print("\nRESULTS:")
print(f"MiniMaxHighPriorityBot wins: {bot1_wins}")
print(f"MiniMaxBot wins: {bot2_wins}")
print(f"Winning percentage for MiniMaxHighPriorityBot: {bot1_wins / num_games * 100:.2f}%")
print(f"Winning percentage for MiniMaxBot: {bot2_wins / num_games * 100:.2f}%")
def play_games(num_games: int, bot1: Bot, bot2: Bot) -> tuple[int, int]:
    """
    Plays a series of games between two bots and returns the number of wins for each bot.

    :param num_games: The number of games to play
    :param bot1: The first bot
    :param bot2: The second bot
    :return: A tuple containing the number of wins for bot1 and bot2
    """
    engine = SchnapsenGamePlayEngine()
    bot1_wins = 0
    bot2_wins = 0

    for i in range(num_games):
        if i % 2 == 0:
            # Bot1 starts as the leader in even games
            winner, _ = engine.play_game(bot1, bot2, rng=random.Random(i))
        else:
            # Bot2 starts as the leader in odd games
            winner, _ = engine.play_game(bot2, bot1, rng=random.Random(i))

        if winner is bot1:
            bot1_wins += 1
        else:
            bot2_wins += 1

        print(f"Game {i + 1}/{num_games}: Winner - {'Bot1' if winner is bot1 else 'Bot2'}")

    return bot1_wins, bot2_wins