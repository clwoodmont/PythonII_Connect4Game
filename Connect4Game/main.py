import Connect4Game
import DanielBatyrevAI as DanielAI
import copy
import func_timeout
import ShmulyStudentAI as ShmulyAI
import YosefBirnbaumAI as YosefAI

# List of AI competitors to play against each other
competitor_list = [ShmulyAI.NotRandomStrategy(), YosefAI.AI_strategy()]

# Maximum wait time (in seconds) for an AI to make its move
MAX_WAIT_TIME = 1

# List to keep track of the winners for each game
winners = []

# Default random move strategy as a fallback
random_choice = DanielAI.RandomStrategy()

# Simulate 1000 games between the AI competitors
for game_nr in range(1000):
    print(game_nr + 1)  # Print the current game number
    tie = False  # Initialize tie status for the game

    # Initialize a new game
    game = Connect4Game.Connect4Game()

    # Play the game until a winner is found or it's a tie
    while game.winner is None:
        # Create a safety copy of the game state for the AI
        game_safety_copy = copy.deepcopy(game)

        try:
            # Get the AI's move within the time limit
            move = func_timeout.func_timeout(
                MAX_WAIT_TIME, competitor_list[game.current_player - 1].strategy, [game_safety_copy]
            )
        except func_timeout.FunctionTimedOut:
            # If the AI times out, fallback to a random move
            print(f'time out limit exceeded: {competitor_list[game.current_player - 1].name} performs random move')
            move = random_choice.strategy(game_safety_copy)

        # Make the move in the game
        game.make_move(move)

        # Check if the board is full (tie condition)
        if 0 == sum(map(game.is_valid_move, range(7))):
            tie = True
            break

    # Record the result of the game
    if tie:
        winners.append("tie")
    else:
        winners.append(competitor_list[game.current_player - 1].name)

    # Reverse the competitor list for the next game
    competitor_list.reverse()

# Print final results after all games
print("started ln 36")

# Create a dictionary to count the wins for each competitor and ties
results_summary = {}
for item in winners:
    results_summary[item] = results_summary.get(item, 0) + 1

# Display the summary of results
print(results_summary)
