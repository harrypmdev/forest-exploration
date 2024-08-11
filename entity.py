""" A module for the Entity class utilised in Forest Exploration. """

from game_state import GameState
from effect import Effect

class Entity:
    """
    A class for the game entities, which includes all living creatures.
    Inherited by Player and Enemy classes.

    Instance Attributes:
    health: int -- the health of the entity
    name: str -- the entity's name
    board: GameBoard -- the board the entity is on
    player: Player -- the player for which moves are being parsed.
    

    Public Methods:
    parse_move -- parse a raw move from the user
    """

    def __init__(self, health: int, name: str, game_state: GameState, sick: bool = False, hostile: bool = False):
        self.name = name
        self.health = health
        self.alive = True
        self.game_state = game_state
        self.sick = sick
        self.cured = False
        self.searched = False
        self.hostile = hostile

    def affect_health(self, effect: Effect) -> str:
        sickness_changed = ""
        if not self.alive:
            return f"The {self.name} is dead, so nothing happens."
        self.health = max(0, self.health + effect.value)
        if self.health == 0:
            return self._die(effect)
        elif self.health > 2 and self.sick:
            sickness_changed = " Its sickness was cured."
            self.sick = False
            self.cured = True
        target_text = "on yourself" if self.name == "player" else f"on {self.name}"
        effect_text = f"restoring {effect.value} health" if effect.value >= 0 else f"dealing {abs(effect.value)} damage"
        return f"{effect.name.capitalize()} {target_text} {effect_text}!{sickness_changed}"
    
    def detailed_name(self, indefinite = False):
        article = self._indefinite() + " " if indefinite else ""
        dead_string = f"{article}{self.name}" if self.alive else f"{article}dead {self.name}"
        sick_string = " (it looks sick and weak)" if self.sick else ""        
        searched_string = ""
        if not self.alive and self.hostile:
            searched_string = " (searched)" if self.searched else " (not searched)"
        hostile_string = " (hostile)" if self.hostile and self.alive else ""
        return f"{dead_string}{hostile_string}{sick_string}{searched_string}"

    def print_status(self):
        sick_status = " It looks sick and weak." if self.sick == True else ""
        if self.health == 0:
            print(f"\n{self.name.capitalize()} is dead.\n")
        else:
            print(f"\n{self.name.capitalize()} has {self.health} health.{sick_status}\n")
    
    def _die(self, effect):
        self.alive = False
        return (f'The {self.name} died! It ran out of health when {effect.name} causing {abs(effect.value)} damage!')
    
    def _indefinite(self):
        vowels = ("a", "e", "i", "o", "u")
        if self.name[0] in vowels:
            return "an"
        return "a"