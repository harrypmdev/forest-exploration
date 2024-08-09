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
        self.item_field = _generate_items()

    def _generate_items(self) -> dict:
        """ 
        Generate the list of items the can be spawned in this game. 
        Returns a dictionary of items and their generation probability.
        """
        items = {}
        items[(HealthItem, ("potion", "A potion that heals 10 health.", 10))] = 0.05
        items[(HealthItem, ("berries", "A tasty food. Heals 3 health.", 3))] = 0.05
        items[(HealthItem, ("tomahawk", "A one-time use weapon that deals 7 damage.", -7, 1, True))] = 0.1
        items[(HealthItem, ("sword", "A sword that will last for a short while.", -4, 5, True))] = 0.05
        items[(HealthItem, ("katana", "A super deadly sword that deals 10 damage.", -10, 7, True))] = 0.05
        items[(HealthItem, ("axe", "A weak but durable weapon. Deals 3 damage.", -3, 15, True))] = 0.05
        items[(Amulet, ("amulet", "Could it be... the amulet of power? There's only one way to find out."))] = 0
        return items

    @border
    def win(self):
        print(f"You win! You finished the game with a score total of {self.records["final_score"]} and {self.records["final_health"]} health.")
        print(f"You moved a total of {self.records["total moves"]} times. You killed {self.records["kills"]} creatures.")