import sys
import pygame
from bullet import Bullet
from settings import Settings
from ship import Ship
from bullet import Bullet


class AlienInvasion:
    """The main class that deals with the management of resources and
    general behaviour"""

    def __init__(self):
        """Initialize pygame, set up the game window and game resources"""
        pygame.init()
        self.settings = Settings()

        # Display
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Alien Invasion")

        # Ship
        self.ship = Ship(self)

        # Bullets
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        while True:
            # Check for input
            self._check_events()

            # Update game objects accordingly
            self.ship.update()
            self._update_bullets()

            # Draw the screen
            self._update_screen()

    def _check_events(self):
        """Watch and react to keyboard and mouse input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Responds to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Responds to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create bullet and add it to the group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        # Remove bullets that are out of bounds from memory
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """Update images on screen and flip to the new screen"""
        # Redraw the screen every step
        self.screen.fill(self.settings.bg_color)
        self.ship.draw()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # And then make it visible
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
