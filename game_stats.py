class GameStats:
    """Tracks statistics for the game"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.game_active = True
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.settings.ships_limit