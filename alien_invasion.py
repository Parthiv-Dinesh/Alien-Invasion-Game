import sys

import pygame

class AlienInvasion:
    """Overall class to class to manage game assets and behaviour."""

    def __init__(self):
        """Initialize the game and create the game resource."""
        pygame.init()

        self.screen = pygame.display.set_mode((1200,800))    #surface
        pygame.display.set_caption("Alien Invasion")
        self.clock = pygame.time.Clock()

        #set the background  color
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            # Watch the keyword and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Redraw the screen durin the each pass through the loop
            self.screen.fill(self.bg_color)
            # Make the most recently drawn screeen visible.
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
