import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to class to manage game assets and behaviour."""

    def __init__(self):
        """Initialize the game and create the game resource."""
        pygame.init()

        self.screen = pygame.display.set_mode((1200,800))    #surface
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height) )
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def _create_fleet(self):
         """create the fleet of aliens."""
         # create alien and keep adding aliens untill there is no room left.
         # spacing between aliens is one alien width
         alien = Alien(self)
         alien_width = alien.rect.width

         current_x = alien_width
         while current_x <(self.settings.screen_width - 2 * alien_width):
              self._create_alien(current_x)
              current_x += 2 * alien_width

    def _create_alien(self,x_position):
              """create an alien and place it in row """
              new_alien = Alien(self)
              new_alien.x = x_position
              new_alien.rect.x = x_position
              self.aliens.add(new_alien)
              

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events_()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)


    def _update_bullets(self):
            """Update position of bullets and get rid of old bullets"""
            #Update bullets position
            self.bullets.update()

            #Get rid of bullets that disappeared.
            for bullet in self.bullets.copy():
                 if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            

    def _check_events_(self):
        """Responds to keypresses and mouse events"""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                     self._check_keyup_events(event)
                          

    def _check_keydown_events(self,event):
          """Respond to keypress"""
          if event.key == pygame.K_RIGHT:
                 self.ship.moving_right = True
          elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
          elif event.key == pygame.K_q:
               sys.exit()
          elif event.key == pygame.K_SPACE:
               self._fire_bullet()

    def _check_keyup_events(self,event):
           """respond to key release."""
           if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
           elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False

    def _fire_bullet(self):
         """Create a new bullet and add it to the bullet group."""
         if len(self.bullets) < self.settings.bullets_allowed:
              
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    

    def _update_screen(self):
         """Update image on the screen, and flip to new screen."""
          # Redraw the screen during the each pass through the loop
         self.screen.fill(self.settings.bg_color)
         for bullet in self.bullets.sprites():
              bullet.draw_bullet()

         self.ship.blitme()
         self.aliens.draw(self.screen)
            # Make the most recently drawn screeen visible.
         pygame.display.flip()
         

if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
