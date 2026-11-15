"""
GameEngine: owns the board, turn state, scoreboard, and round-end logic.

You (the player) always play X and click to move. The computer always
plays O and moves automatically right after you, using a simple
random-move AI (see game/ai.py).

Controls:
    Click  - place your symbol
    R      - restart the round (scoreboard kept)
    M      - reset the whole match (scoreboard cleared)
    X / O  - choose who starts the NEXT round
"""

import pygame

from game.rules import check_winner, is_board_full
from game.renderer import board_pos_to_cell
from game import renderer
from game.ai import choose_move

HUMAN_SYMBOL = 'X'
COMPUTER_SYMBOL = 'O'


class GameEngine:
    def __init__(self):
        # Match-level state (survives round restarts)
        self.scores = {'X': 0, 'O': 0, 'draw': 0}
        self.first_player = 'X'
        # Round-level state
        self.new_round()

    # ---------- round / match control ----------

    def new_round(self):
        """Start a fresh round. Keeps scores and the first-player choice."""
        self.board = [[None] * 3 for _ in range(3)]
        self.current_player = self.first_player
        self.round_over = False
        self.winner = None   # 'X', 'O', or None (draw, only valid when round_over)
        self._maybe_take_computer_turn()   # computer opens if O starts

    def reset_match(self):
        """Clear the scoreboard and start a fresh round."""
        self.scores = {'X': 0, 'O': 0, 'draw': 0}
        self.new_round()

    # ---------- moves ----------

    def _place(self, row, col):
        """Put the current player's symbol on the board, check the result,
        and switch turns (unless the round just ended)."""
        self.board[row][col] = self.current_player
        self.check_round_end()
        if not self.round_over:
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def handle_click(self, pos):
        if self.round_over:
            return   # round ended - ignore clicks
        if self.current_player != HUMAN_SYMBOL:
            return   # not your turn
        cell = board_pos_to_cell(pos)
        if cell is None:
            return
        row, col = cell
        if self.board[row][col] is not None:
            return   # occupied cell - reject, nothing changes
        self._place(row, col)
        self._maybe_take_computer_turn()

    def _maybe_take_computer_turn(self):
        if self.round_over or self.current_player != COMPUTER_SYMBOL:
            return
        move = choose_move(self.board)
        if move is None:
            return
        self._place(*move)

    # ---------- keyboard ----------

    def handle_keydown(self, key):
        if key == pygame.K_r:
            self.new_round()          # restart round, keep scores
        elif key == pygame.K_m:
            self.reset_match()        # restart round and clear scores
        elif key == pygame.K_x:
            self.first_player = 'X'   # applies on the next round
        elif key == pygame.K_o:
            self.first_player = 'O'   # applies on the next round

    # ---------- round end ----------

    def check_round_end(self):
        winner = check_winner(self.board)   # check for a win BEFORE a draw
        if winner:
            self.round_over = True
            self.winner = winner
            self.scores[winner] += 1
        elif is_board_full(self.board):
            self.round_over = True
            self.winner = None
            self.scores['draw'] += 1

    # ---------- drawing ----------

    def draw(self, surface, font):
        renderer.draw_board(surface, self.board)

        turn_label = "Your turn (X)" if self.current_player == HUMAN_SYMBOL else "Computer's turn (O)"
        renderer.draw_text(surface, font, turn_label, (10, 15))

        s = self.scores
        renderer.draw_text(surface, font, f"X:{s['X']}  O:{s['O']}  Draws:{s['draw']}", (10, 45))
        renderer.draw_text(surface, font, f"Next round starts: {self.first_player}", (10, 72))

        if self.round_over:
            text = f"{self.winner} wins!" if self.winner else "Draw!"
            renderer.draw_banner(surface, font, f"{text} Press R for a new round.")

        renderer.draw_text(surface, font, "R:round M:match X/O:starter", (10, 530))