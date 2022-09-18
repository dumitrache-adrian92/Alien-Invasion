import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Manages bullets fired by the ship"""

    def __init__(self, ai_game):
        super().__init__()
        # Move over some stuff so we can access it in our methods
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Rectangle creation
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """Changes bullet location as it travels across the screen"""
        self.y -= self.settings.bullet_speed # decimal position
        self.rect.y =self.y # rect position

    def draw_bullet(self):
        """Draws the bullet to the screen at its current rect"""
        pygame.draw.rect(self.screen, self.color, self.rect)