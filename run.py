import math
import os
import game_board
import player
import utility

def parse_move(move, board, player):
    if "use" in move:
        pass
    else:
        board.parse_move(move, player)

def main():
    board = game_board.GameBoard(5)
    player = Player(30, 0, [])
    board.introduce(player)
    player.print_status()
    while player.alive:
        move = player.get_move()
        parse_move(move, board, player)
main()