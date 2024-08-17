"""A module for the GameState class utilised in the Forest Exploration game."""

from resources.utility import border


class GameState:
    """A class for the game's key variables.

    Public Instance Attributes:
    game_won: bool -- whether or not the game has been won
    records: dict -- a record of player achievements.
    amulet_generated: bool -- whether the amulet has been generated yet.
    amulet_probability: float -- the probability of amulet generation throughout
                                a game (0 is never, 1 is definitely).

    Public Methods:
    update_amulet_gen -- update probability of amulet generating based on
                         amount of areas visited.
    update_kill_records -- update record of total kills and score in accordance.
    update_score -- update score and print score message.
    win -- print the win message and set the game_won attribute to True.
    """

    def __init__(self) -> None:
        """Constructor for GameState class."""
        self.game_won = False
        self.records = {
            "score": 0,
            "total moves": 0,
            "kills": 0,
        }
        self.amulet_generated = False
        self.amulet_probability = 0

    def update_amulet_gen(self, board_size: int, num_of_visited: int) -> None:
        """Update probability of amulet generating based on amount of areas visited."""
        percent_visited = (1 / (board_size * board_size)) * num_of_visited
        self.amulet_probability = (not self.amulet_generated) * percent_visited

    def update_kill_records(self) -> None:
        """Update the game state's 'kills'.
        Gives the player 10 points and prints a message informing them.
        """
        self.update_score(10)
        self.records["kills"] += 1

    def update_score(self, score: int) -> None:
        """Update the game state's score by the given argument.
        Prints a message informing the player.

        Arguments:
        score: int -- the points which should be added to the current score.
        """
        print(f"Score +{score}!")
        self.records["score"] += score

    @border
    def win(self, final_health: int) -> None:
        """Print the game's win message and set game_won attribute to True.

        Arguments:
        final_health: int -- the final health of the player at the time
                             the game was won.
        """
        self.game_won = True
        print(
            f"You win! You finished the game with a score total of {self.records["score"]} and {final_health} health."
        )
        print(
            f"You moved a total of {self.records["total moves"]} time(s). You killed {self.records["kills"]} creature(s)."
        )
