"""
A module containing functions to manipulate game scores from the Google sheets
file associated with the Forest Exploration game.

Functions:
save_game --
"""

import gspread
from google.oauth2.service_account import Credentials

from game_state import GameState

_SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
_CREDS = Credentials.from_service_account_file('creds.json')
_SCOPED_CREDS = _CREDS.with_scopes(_SCOPE)
_GSPREAD_CLIENT = gspread.authorize(_SCOPED_CREDS)
_SHEET = _GSPREAD_CLIENT.open('forest_exploration')
_leaderboard = _SHEET.worksheet('leaderboard')

class Save:

    def __init__(self, name: str, records: dict):
        self.name = name
        self.score = records["score"]
        self.total_moves = records["total moves"]
        self.kills = records["kills"]
        self.health = records["health"]

    def add_to_leaderboard(self):
        _leaderboard.append_row(
            self.name,
            self.score,
            self.total_moves,
            self.kills,
            self.health
        )

def save_game(records: dict):
    name = input("\nEnter a leaderboard name:\n")
    new_save = Save(name, records)
    Save.add_to_leaderboard()

def print_leaderboard():
    rows = _leaderboard.get_all_values()[1:]
    saves = []
    for row in rows:
        print(row)
        try:
            save = _parse_row(row)
        except TypeError as e:
            print(e)
            continue
        saves.append(save)
    saves.sort(key=lambda save: save.score)
    for save in saves:
        print("-" * 80)
        print(dir(save))

def _parse_row(row: list[str]) -> Save:
    name = row[0]
    score, total_moves, kills, health = row[1:]
    records = {
        "score": score,
        "total_moves": total_moves,
        "kill": kills,
        "health": health
    }
    name_invalid = type(name) is not str
    records_invalid = any(val.isdigit() for val in records.values())
    for val in records.values():
        print(val.isdigit())
    print("name invalid:" + str(name_invalid))
    print("records_invalid:" + str(records_invalid))
    if name_invalid or records_invalid:
        raise TypeError('Cannot parse: row contains corrupted data.')
    return Save(name, records)

print_leaderboard()