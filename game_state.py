from utility import border

class GameState:
    """
    A class for the game's key variables.

    Instance Attributes:
    amulet_generated: bool -- whether the amulet has been generated yet.
    game_won: bool -- whether or not the game has been won
    records: dict -- a record of player achievements.

    """
    ITEMS = (
        (HealthItem, ("tomahawk", "A one-time use weapon that deals 7 damage.", -7, 1, True))
        (HealthItem, ("potion", "A potion that heals 10 health.", 10))
        (HealthItem, ("berries", "A tasty food. Heals 3 health.", 3))
        (HealthItem, ("sword", "A sword that will last for a short while.", -4, 5, True))
        (HealthItem, ("katana", "A super deadly sword that deals 10 damage.", -10, 7, True))
        (HealthItem, ("axe", "A weak but durable weapon. Deals 3 damage.", -3, 15, True))
        (Amulet, ("amulet", "Could it be... the amulet of power? There's only one way to find out.")) 
    )

    def __init__(self):
        self.amulet_generated = False
        self.game_won = False
        self.records = {
            "total moves": 0,
            "kills": 0,
            "final_score": 0,
            "final_health": 0
        }
        self.item_probabilites = {
            "tomahawk": 0.01,
            "potion": 0.05,
            "berries": 0.05,
            "sword": 0.05,
            "katana": 0.05,
            "axe": 0.05,
            "amulet": 0
        }

    def update_amulet_generation_probability(self, board_size: int, num_of_visited_locations: int) -> None:
        """ Update probability of amulet generating based on amount of areas visited. """
        for ItemType, item_args in self.ITEMS:
            item_name = item_args[1]
            if item_name == "amulet":
                self.item_probabilites[item_name] = int(not amulet_generated) * (1 / (board_size*board_size)) * num_of_visited_locations

    @border
    def win(self):
        print(f"You win! You finished the game with a score total of {self.records["final_score"]} and {self.records["final_health"]} health.")
        print(f"You moved a total of {self.records["total moves"]} times. You killed {self.records["kills"]} creatures.")