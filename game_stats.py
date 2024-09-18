class GameStats:
    """Track statistic for alien invasion."""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit