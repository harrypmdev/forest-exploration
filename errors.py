"""
A module for exceptions potentially produced in the running of the Forest Exploration game.


Exception:
GameError -- an exception to be raised when improper user input is passed to the Parser
              method parse_move.
LeaderboardError -- an exception to be raised if an issue arises using the leaderboard Google sheet.
"""


class GameError(Exception):
    """
    An exception to be raised when improper user input is
    passed to the Parser method parse_move.
    """

    pass


class LeaderboardError(Exception):
    """
    An exception to be raised when an issue arises saving to or retrieving
    data from the leaderboard Google sheet using the Google API.
    """

    pass
