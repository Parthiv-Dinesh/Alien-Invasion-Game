class Settings:
    """ Initialize the game's static settings."""

    def __init__(self):
        """Initialize the games settings """
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        #ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        #Bullet settings
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10

        #how quickly the game speed up
        self.speedup_scale = 1.1
        # how quickly the the alien point value increase
        self.score_scale = 1.5

        self.difficulty_level = 'easy'

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throghout the game"""
        if self.difficulty_level == 'easy':
            self.ship_limit = 5
            self.bullets_allowed = 10
            self.ship_speed = 0.75
            self.bullet_speed = 1.5
            self.alien_speed = 0.5
        elif self.difficulty_level == 'medium':
            self.ship_limit = 3
            self.bullets_allowed = 3
            self.ship_speed = 1.5
            self.bullet_speed = 3.0
            self.alien_speed = 1.0
        elif self.difficulty_level == 'hard':
            self.ship_limit = 2
            self.bullets_allowed = 3
            self.ship_speed = 3
            self.bullet_speed = 6.0
            self.alien_speed = 2.0

        #fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        
        # Scoring settings
        self.alien_points = 50

    def increase_speed(self):
        """increase speed settings and alien point value"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

    def set_difficulty(self, diff_setting):
        """set difficulty level"""
        if diff_setting == 'easy':
            print("easy")
        elif diff_setting == 'medium':
            pass
        elif diff_setting == 'hard':
            pass
