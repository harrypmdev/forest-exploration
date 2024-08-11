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
            "score": 0,
            "final_health": 0,
        }
        self.item_probabilites = {
            "tomahawk": 0.05,
            "potion": 0.06,
            "berries": 0.08,
            "sword": 0.04,
            "katana": 0.04,
            "axe": 0.05,
            "amulet": 0
        }

    def update_amulet_generation_probability(self, board_size: int, num_of_visited: int) -> None:
        """ Update probability of amulet generating based on amount of areas visited. """
        percent_visited = (1 / (board_size*board_size)) * num_of_visited
        amulet_probability = (not self.amulet_generated) * percent_visited
        self.item_probabilites["amulet"] = amulet_probability
    
    def update_kill_records(self):
        self.update_score(10)
        self.records["kills"] += 1

    def update_score(self, score):
        print(f"Score +{str(score)}!")
        self.records["score"] += score

    @border
    def win(self):
        self.game_won = True
        print(f"You win! You finished the game with a score total of {self.records["score"]} and {self.records["final_health"]} health.")
        print(f"You moved a total of {self.records["total moves"]} times. You killed {self.records["kills"]} creatures.")