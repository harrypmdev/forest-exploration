from utility import border

class GameState:
    """
    A class for the game's key variables.

    Instance Attributes:
    amulet_generated: bool -- whether the amulet has been generated yet.
    game_won: bool -- whether or not the game has been won
    records: dict -- a record of player achievements.

    """

    def __init__(self):
        self.amulet_generated = False
        self.game_won = False
        self.records = {
            "total moves": 0,
            "kills": 0,
            "final_score": 0,
            "final_health": 0
        }

    @border
    def win(self):
        print(f"You win! You finished the game with a score total of {self.records["final_score"]} and {self.records["final_health"]} health.")
        print(f"You moved a total of {self.records["total moves"]} times. You killed {self.records["kills"]} creatures.")