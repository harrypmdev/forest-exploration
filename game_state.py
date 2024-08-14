"""
A module for the GameState class utilised
in the Forest Exploration game.
"""

from utility import border


class GameState:
    """
    A class for the game's key variables.

    Public Instance Attributes:
    amulet_generated: bool -- whether the amulet has been generated yet.
    game_won: bool -- whether or not the game has been won
    records: dict -- a record of player achievements.
    item_probabilites: dict -- a dictionary of items and their relative
                               generation probability
    amulet_probability: float -- keeps track of the probability of amulet
                                 generation throughout a game (0 is never,
                                 1 is definitely).

    Public Methods:
    update_amulet_gen: None -- Update probability of amulet generating
                               based on amount of areas visited.
    update_kill_records: None -- Update record of total kills
                                 and score in accordance.
    update_score: None -- Update score and print score message.
    win: None -- Print the win message and set the game_won attribute
                 to True.
    """

    def __init__(self):
        self.amulet_generated = False
        self.game_won = False
        self.records = {
            "total moves": 0,
            "kills": 0,
            "score": 0,
        }
        self.amulet_probability = 0

    def update_amulet_gen(self, board_size: int, num_of_visited: int) -> None:
        """Update probability of amulet generating based on amount of areas visited."""
        percent_visited = (1 / (board_size * board_size)) * num_of_visited
        self.amulet_probability = (not self.amulet_generated) * percent_visited

    def update_kill_records(self) -> None:
        self.update_score(10)
        self.records["kills"] += 1

    def update_score(self, score) -> None:
        print(f"Score +{str(score)}!")
        self.records["score"] += score

    @border
    def win(self, final_health: int) -> None:
        self.game_won = True
        print(
            f"You win! You finished the game with a score total of {self.records["score"]} and {final_health} health."
        )
        print(
            f"You moved a total of {self.records["total moves"]} times. You killed {self.records["kills"]} creatures."
        )
