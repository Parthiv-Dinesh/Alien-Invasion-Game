import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import ScoreBoard
from button import Button
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

        #create an instance to store game statistics
        #and  create a scoreboard.
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start Alien Invasion in an active state.
        self.game_active = False

        # Make the play button.
        self.play_button = Button(self, "Play")

    def _create_fleet(self):
         """create the fleet of aliens."""
         # create alien and keep adding aliens untill there is no room left.
         # spacing between aliens is one alien width and one alien height
         alien = Alien(self)
         alien_width, alien_height = alien.rect.size

         current_x, current_y = alien_width, alien_height
         while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x <(self.settings.screen_width - 2 * alien_width):
               self._create_alien(current_x, current_y)
               current_x += 2 * alien_width

            # Finished a row; reset x value, increment y value
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self,x_position, y_position):
              """create an alien and place it in fleet """
              new_alien = Alien(self)
              new_alien.x = x_position
              new_alien.rect.x = x_position
              new_alien.rect.y = y_position
              self.aliens.add(new_alien)

    def _check_fleet_edges(self):
         """Respond appropriately if any aliens have reached an edges."""
         for alien in self.aliens.sprites():
              if alien.check_edges():
                   self._change_fleet_direction()
                   break
     
    def _change_fleet_direction(self):
         """Drop the entire fleet and change the fleet's direction."""
         for alien in self.aliens.sprites():
              alien.rect.y += self.settings.fleet_drop_speed
         self.settings.fleet_direction *= -1
              

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events_()

            if self.game_active:
             self.ship.update()
             self._update_bullets()
             self._update_aliens()

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

            self._check_bullet_alien_collisions()
            

    def _check_bullet_alien_collisions(self):
         """Respond to bullet-alien_collisions."""
         #Remove any bullets and aliens that have collided.
         collisions = pygame.sprite.groupcollide(
                 self.bullets, self.aliens, True, True)
         
         if collisions:
              self.stats.score += self.settings.alien_points
              self.sb.prep_score()
         
         if not self.aliens:
               # Destroy the existing bullets and create new fleet.
                 self.bullets.empty()
                 self._create_fleet()
                 self.settings.increase_speed()


    def _update_aliens(self):
         """check if the fleet is at an edge, the update the positions."""
         self._check_fleet_edges()
         self.aliens.update()

         # Look for alien-ship collisions.
         if pygame.sprite.spritecollideany(self.ship, self.aliens):
              self._ship_hit()

          #look for aliens hitting the bottom of the screen.
         self._check_aliens_bottom()

    def _ship_hit(self):
         """Responds to the ship being hit by an alien."""
         if self.stats.ships_left > 0 :

          #Decrement ships_left
          self.stats.ships_left -= 1

          #Get rid of any remaining bullets and aliens.
          self.bullets.empty()
          self.aliens.empty()

          # Create a new fleet and the center the ship.
          self._create_fleet()
          self.ship.center_ship()
          #pause
          sleep(0.5)
         else:
              self.game_active = False
              pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
         """check if any aliens have reached the bottom of the screen."""
         for alien in self.aliens.sprites():
              if alien.rect.bottom >= self.settings.screen_height:
                   # Treat this the same as if ship got hit.
                   self._ship_hit()
                   break
            

    def _check_events_(self):
        """Responds to keypresses and mouse events"""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                     self._check_keyup_events(event)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                     mouse_pos = pygame.mouse.get_pos()
                     self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
         """Start a new game when the player clicks Play."""
         button_clicked = self.play_button.rect.collidepoint(mouse_pos)
         if button_clicked and not self.game_active:
              
              self._start_game()

    def _start_game(self):
              """start a new game"""
              
              #Reset the game settings
              self.settings.initialize_dynamic_settings()

              # Restart the game statistics.
              self.stats.reset_stats()
              self.game_active = True

              # Get rid of any remaining bullets and aliens.
              self.bullets.empty()
              self.aliens.empty()

              # Create a new fleet and centeer the ship.
              self._create_fleet()
              self.ship.center_ship()

              # Hide the mouse cursor.
              pygame.mouse.set_visible(False)
                     
                          

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
          elif (event.key == pygame.K_p) and (not self.game_active):
               self._start_game()

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

         # Draw the score information.
         self.sb.show_score()

         # Draw the play button if the game is inactive
         if not self.game_active:
              self.play_button.draw_button()
     
         pygame.display.flip()
         

if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
