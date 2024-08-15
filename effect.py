"""
A module for the Effect class utilised in the Forest Exploration game.
"""


class Effect:
    """
    A class for effects, objects that can be passed to an entity's
    apply_effect method to affect its health.

    Public Attributes:
    name: str -- the effect name e.g 'was punched', 'got burnt'.
    value: int -- the health value the effect applies.
    """

    def __init__(self, name: str, value: int) -> None:
        """
        Constructor for the Effect class.

        Arguments:
        name: str -- the effect name e.g 'was punched', 'got burnt'.
        value: int -- the health value the effect applies. Positive integers
                      increase health, negative integers decrease health.
        """
        self.name = name
        self.value = value
