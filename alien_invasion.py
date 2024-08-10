import sys

import pygame

from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overall class to class to manage game assets and behaviour."""

    def __init__(self):
        """Initialize the game and create the game resource."""
        pygame.init()

        self.screen = pygame.display.set_mode((1200,800))    #surface
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height) )
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events_()
            self._update_screen()
            self.clock.tick(60)

    def _check_events_(self):
        """Responds to keypresses and mouse events"""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

    def _update_screen(self):
         """Update image on the screen, and flip to new screen."""
          # Redraw the screen during the each pass through the loop
         self.screen.fill(self.settings.bg_color)
         self.ship.blitme()
            # Make the most recently drawn screeen visible.
         pygame.display.flip()
         

if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
