import json

class GameStats:
    """Tracks statistics for the game"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.game_active = False
        try:
            with open("high_score.json", "r") as f:
                self.high_score = json.load(f)
        except FileNotFoundError:
            self.high_score = 0
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.settings.ships_limit
        self.score = 0
        self.level = 1