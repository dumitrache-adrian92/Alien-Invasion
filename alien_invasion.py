#!/usr/bin/env python3

from curses import start_color
from re import L
import sys
from time import sleep
import json

import pygame

from bullet import Bullet
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


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

        # Stats
        self.stats = GameStats(self)
        # Ship
        self.ship = Ship(self)
        # Bullets
        self.bullets = pygame.sprite.Group()
        # Aliens
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # Start screen shit
        self.play_button = Button(self, "Play")
        # Scoreboard
        self.sb = Scoreboard(self)
        self.clock = pygame.time.Clock()

    def run_game(self):
        while True:
            # Check for input
            self._check_events()

            # Update game objects accordingly if the hasn't ended
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            # Draw the screen
            self._update_screen()

            self.clock.tick(60)

    def _check_events(self):
        """Watch and react to keyboard and mouse input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._dump_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Responds to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._dump_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            self._check_play_button("lol")
        elif event.key == pygame.K_p:
            self._check_play_button("lol")

    def _check_keyup_events(self, event):
        """Responds to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, pos):
        """Start a new game when a player clicks play"""
        game_started = pos == "lol" or self.play_button.rect.collidepoint(pos)
        if game_started and not self.stats.game_active:
            # Reset game settings
            self.settings.init_dynamic_settings()
            pygame.mouse.set_visible(False)

            self.stats.reset_stats()
            self.stats.game_active = True

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

    def _fire_bullet(self):
        """Create bullet and add it to the group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """All actions related to bullet updating"""
        self.bullets.update()

        # Remove bullets that are out of bounds from memory
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Check for collisions and keep it for points
        self._check_collisions()

    def _check_collisions(self):
        """Check for any collisions and refresh the fleet if empty"""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self._new_level()

    def _new_level(self):
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()
        self.stats.level += 1
        self.sb.prep_level()

    def _check_bottom(self):
        """Checks if aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _create_fleet(self):
        """Creates the alien fleet"""
        alien = Alien(self)
        a_width, a_height = alien.rect.size
        ship_height = self.ship.rect.height

        # Horizontal and vertical space dedicated to aliens
        x_space = self.settings.screen_width - 2 * a_width
        y_space = self.settings.screen_height - (3 * a_height) - ship_height
        # How many aliens we can fit in this space
        alien_total_x = x_space // (2 * a_width)
        alien_total_y = y_space // (2 * a_height)

        # Create screen full of aliens
        for j in range(alien_total_y):
            for i in range(alien_total_x):
                self._create_alien(i, j)

    def _create_alien(self, i, j):
        """Creates alien at i, j coordinates"""
        alien = Alien(self)
        width, height = alien.rect.size
        # Determine x
        alien.x = width + 2 * width * i
        alien.y = height + 2 * height * j
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Update images on screen and flip to the new screen"""
        # Redraw the screen every step
        self.screen.fill(self.settings.bg_color)
        self.ship.draw()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        # And then make it visible
        pygame.display.flip()

    def _dump_high_score(self):
        with open("high_score.json", "w") as f:
            json.dump(self.stats.high_score, f)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
