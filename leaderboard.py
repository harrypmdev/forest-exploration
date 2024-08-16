"""
A module containing functions to manipulate game scores from the leaderboard
Google sheets file associated with the Forest Exploration game.

Functions:
save_game -- save a game to the leaderboard.
print_leaderboard -- print the leaderboard.
"""

from collections import OrderedDict

import gspread
from google.oauth2.service_account import Credentials

from errors import LeaderboardError


_SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]
_CREDS = Credentials.from_service_account_file("creds.json")
_SCOPED_CREDS = _CREDS.with_scopes(_SCOPE)
_GSPREAD_CLIENT = gspread.authorize(_SCOPED_CREDS)
_SHEET = _GSPREAD_CLIENT.open("forest_exploration")
_leaderboard = _SHEET.worksheet("leaderboard")


class _Save:
    """
    A class for game saves that are read from and saved to the leaderboard.

    Public Attributes:
    records: OrderedDict -- an ordered dictionary of the information relevant
                            to the save. Holds (in this order): 'size', 'name',
                            'score', 'total moves', 'kills', 'health'.

    Public Methods:
    add_to_leaderboard -- add this save to the leaderboard spreadsheet.
    print -- print this save's information.
    """

    def __init__(self, name: str, records: dict) -> None:
        """
        Constructor for _Save class.

        Arguments:
        name: str -- the name underwhich these records are saved to the
                     leaderboard.
        records: dict -- A dictionary of information about a game. Must include
                         keys: 'size', 'score', 'total moves', 'kills', 'health'.
        """
        self.records = OrderedDict()
        self.records["size"] = records["size"]
        self.records["name"] = name
        self.records["score"] = records["score"]
        self.records["total moves"] = records["total moves"]
        self.records["kills"] = records["kills"]
        self.records["health"] = records["health"]

    def add_to_leaderboard(self) -> None:
        """Add this save to the leaderboard spreadsheet."""
        try:
            _leaderboard.append_row(list(self.records.values()))
        except Exception as exc:
            raise LeaderboardError(
                "\nError using Google API attempting to save to Google sheet."
            ) from exc

    def print(self, position: int = 1) -> None:
        """
        Print this save.

        Arguments:
        postion: int -- the position in the leaderboard this save should be
                        printed as being at. Default is 1.
        """
        size, name = list(self.records.values())[:2]
        size = f"{size}x{size}"
        pos_gap = self._get_whitespace(str(position), 3)
        name_gap = self._get_whitespace(name, 9)
        string = f"{position}{pos_gap}{size} | Name: {name}{name_gap}|"
        for key, value in list(self.records.items())[2:]:
            gap = self._get_whitespace(value, 3)
            string += f" {key.capitalize()}: {value}{gap}|"
        print(string)

    def _get_whitespace(self, string: str, desired_length: int) -> str:
        gap = desired_length - len(string)
        return " " * gap


def save_game(records: dict) -> None:
    """
    Save a game to the leaderboard.

    Arguments:
    records: dict -- A dictionary of information about a game. Must include
                     keys: 'size', 'score', 'total moves', 'kills', 'health'.

    Raises ValueError if passed an inappropriate argument, including a
    dictionary without the keys listed above.
    """
    try:
        records["size"]
        records["score"]
        records["total moves"]
        records["kills"]
        records["health"]
    except NameError:
        raise ValueError(
            "Passed value other than a dictionary or dict has incorrect keys.\n"
            "Ensure the following keys are present: 'score', 'total_moves',\n"
            "'kills', 'health'."
        )
    name = _get_name()
    new_save = _Save(name, records)
    new_save.add_to_leaderboard()


def print_leaderboard() -> None:
    """
    Print the leaderboard.
    If leaderboard is empty, prints message to explain this.
    """
    saves = _get_leaderboard_saves()
    if not saves:
        print("No scores yet saved to leaderboard.\n")
        return
    print(
        "\n═══━━━━━━━━━━────────────────── • LEADERBOARD •  ──────────────────━━━━━━━━━━═══"
    )
    position = 1
    for save in saves:
        print("-" * 80)
        save.print(position)
        position += 1
    print("")


def _get_name() -> str:
    # Return user input of 9 characters of less
    name = False
    while not name or len(name) > 9:
        name = input("\nEnter a leaderboard name of 9 characters or less:\n")
        if len(name) > 9:
            print("\nName must be 9 characters or less!")
    return name


def _get_leaderboard_saves() -> list[_Save]:
    # Get all leaderboard information in the form of a list of _Saves.
    try:
        rows = _leaderboard.get_all_values()[1:]
    except Exception as exc:
        raise LeaderboardError(
            "\nError using Google API to retrieve leaderboard data from Google sheet."
        ) from exc
    saves = []
    for row in rows:
        try:
            save = _parse_row(row)
        except TypeError:
            continue
        saves.append(save)
    saves.sort(key=lambda save: int(save.records["score"]), reverse=True)
    return saves


def _parse_row(row: list[str]) -> _Save:
    # Take a row from the leaderboard (a list of five items) and return a _Save
    # with the values from the row
    size = row[0]
    name = row[1]
    score, total_moves, kills, health = row[2:]
    records = {
        "size": size,
        "score": score,
        "total moves": total_moves,
        "kills": kills,
        "health": health,
    }
    name_invalid = type(name) is not str or len(name) > 9
    records_invalid = any(not val.isdigit() for val in records.values())
    if name_invalid or records_invalid:
        raise TypeError("Cannot parse: row contains corrupted data.")
    return _Save(name, records)
