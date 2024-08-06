class Entity:
    """
    A class for game entities, inherited by Player and Enemy.
    """

    def __init__(self, health, name, board, sick = False, hostile = False):
        self.name = name
        self.health = health
        self.alive = True
        self.board = board
        self.sick = sick
        self.searched = False
        self.hostile = hostile

    def affect_health(self, effect, output_message = True):
        sickness_changed = ""
        if not self.alive:
            print(f"\nThe {self.name} is dead, so nothing happens.\n")
            return
        self.health = max(0, self.health + effect.value)
        if self.health == 0:
            self.die(effect)
            return True
        elif self.health > 2:
            sickness_changed = " Its sickness was cured." if self.sick else ""
            self.sick = False
        if not output_message:
            return False
        target_text = "on yourself" if self.name == "player" else f"on {self.name}"
        effect_text = f"restoring {effect.value} health" if effect.value >= 0 else f"dealing {abs(effect.value)} damage"
        print(f"\n{effect.name.capitalize()} {target_text} {effect_text}!{sickness_changed}\n")
        return False
    
    def die(self, effect):
        print(f'\nThe {self.name} died! It ran out of health when {effect.name} causing {abs(effect.value)} damage!\n')
        self.board.records["kills"] += 1
        self.alive = False
    
    def print_status(self):
        sick_status = " It looks sick and weak." if self.sick == True else ""
        if self.health == 0:
            print(f"\n{self.name.capitalize()} is dead.\n")
        else:
            print(f"\n{self.name.capitalize()} has {self.health} health.{sick_status}\n")
    
    def indefinite(self):
        vowels = ("a", "e", "i", "o", "u")
        if self.name[0] in vowels:
            return "an"
        return "a"

    def detailed_name(self, indefinite = False):
        article = self.indefinite() + " " if indefinite else ""
        dead_string = f"{article}{self.name}" if self.alive else f"{article}dead {self.name}"
        sick_string = " (it looks sick and weak) " if self.sick else ""        
        searched_string = ""
        if not self.alive and self.hostile:
            searched_string = " (searched)" if self.searched else " (not searched)"
        hostile_string = " (hostile)" if self.hostile and self.alive else ""
        return f"{dead_string}{hostile_string}{sick_string}{searched_string}"
    