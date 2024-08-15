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
_data = _leaderboard.get_all_values()
print(_data)

def save_game(game_state: GameState):
    pass
