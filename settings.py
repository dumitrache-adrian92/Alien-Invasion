class Settings:
    """Game's static and dynamic settings"""

    def __init__(self):
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ships_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        # Alien settings
        self.fleet_drop_speed = 10

        # Scaleability
        self.speedup_scale = 1.3
        self.score_scale = 1.5

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 8
        self.bullet_speed = 9
        self.alien_speed = 4
        self.fleet_direction = 1    # 1 represents right; -1 represents left.
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= 1.1
        self.alien_points *= self.score_scale
