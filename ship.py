import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Ship management"""

    def __init__(self, ai_game):
        """Initialization and starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Import the image
        self.image = pygame.image.load('images/ship.bmp').convert_alpha()
        self.rect = self.image.get_rect()

        # Initial position of the ship
        self.rect.midbottom = self.screen_rect.midbottom

        # Movement flags
        self.moving_right = False
        self.moving_left = False

        # Separate horizontal position so we cand do subpixel movement
        self.x = float(self.rect.x)

    def update(self):
        """Update the position of the ship according to the movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def draw(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
