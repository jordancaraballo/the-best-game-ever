# Import Python's random module for random numbers
import random

# Import pygame-ce and alias it as pg for convenience
import pygame as pg

# Game constants
WIDTH, HEIGHT = 640, 360       # Screen dimensions in pixels
FPS = 60                       # Frames per second
PLAYER_SPEED = 280             # Player movement speed in pixels per second
ENEMY_SPAWN_EVERY = 0.7        # Time between enemy spawns (in seconds)


# -------------------------
# Player class
# -------------------------
class Player(pg.sprite.Sprite):       # Inherits from pygame's Sprite class
    def __init__(self, pos):
        super().__init__()            # Call parent constructor
        # Create a 32x32 transparent surface for the player
        self.image = pg.Surface((32, 32), pg.SRCALPHA)
        # Draw a rounded rectangle to represent the player
        pg.draw.rect(self.image, (80, 200, 255), self.image.get_rect(), border_radius=6)
        # Get a rect (for positioning) and center it at the given position
        self.rect = self.image.get_rect(center=pos)
        # Store position as a Vector2 for smoother movement
        self.pos = pg.Vector2(self.rect.center)

    def update(self, dt):
        # Check which keys are currently held down
        keys = pg.key.get_pressed()
        # Create a movement vector from arrow/WASD keys
        move = pg.Vector2(
            (keys[pg.K_RIGHT] or keys[pg.K_d]) - (keys[pg.K_LEFT] or keys[pg.K_a]),
            (keys[pg.K_DOWN] or keys[pg.K_s]) - (keys[pg.K_UP] or keys[pg.K_w]),
        )
        # If moving diagonally, normalize so speed is consistent
        if move.length_squared():
            move = move.normalize()
        # Apply movement scaled by PLAYER_SPEED and delta time
        self.pos += move * PLAYER_SPEED * dt
        # Clamp position so the player stays inside the screen
        self.pos.x = max(16, min(WIDTH - 16, self.pos.x))
        self.pos.y = max(16, min(HEIGHT - 16, self.pos.y))
        # Update the rect's center so it matches the new position
        self.rect.center = self.pos

# -------------------------
# Enemy class
# -------------------------
class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()  # Call parent constructor
        # Random width/height for the enemy rectangle
        w, h = random.randint(16, 50), random.randint(16, 50)
        # Create surface for the enemy with transparency
        self.image = pg.Surface((w, h), pg.SRCALPHA)
        # Draw the enemy as a red rounded rectangle
        pg.draw.rect(self.image, (255, 80, 100), self.image.get_rect(), border_radius=4)
        # Randomly choose a side to spawn from
        side = random.choice(["left", "right", "top", "bottom"])
        # Random speed for the enemy
        speed = random.randint(90, 180)

        # Set spawn position and velocity based on chosen side
        if side == "left":
            self.pos = pg.Vector2(-w, random.uniform(0, HEIGHT))
            self.vel = pg.Vector2(speed, 0)
        elif side == "right":
            self.pos = pg.Vector2(WIDTH + w, random.uniform(0, HEIGHT))
            self.vel = pg.Vector2(-speed, 0)
        elif side == "top":
            self.pos = pg.Vector2(random.uniform(0, WIDTH), -h)
            self.vel = pg.Vector2(0, speed)
        else:  # bottom
            self.pos = pg.Vector2(random.uniform(0, WIDTH), HEIGHT + h)
            self.vel = pg.Vector2(0, -speed)

        # Set the rectangle for positioning
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt):
        # Move enemy based on velocity and delta time
        self.pos += self.vel * dt
        # Update rect position
        self.rect.center = self.pos
        # If enemy goes off screen far enough, remove it from all groups
        if (self.rect.right < -60 or self.rect.left > WIDTH + 60 or
            self.rect.bottom < -60 or self.rect.top > HEIGHT + 60):
            self.kill()


# -------------------------
# Main game loop
# -------------------------
def main():

    pg.init()  # Initialize all pygame modules

    # Create the game window
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Dodge the Blocks (pygame-ce)")
    clock = pg.time.Clock()  # To control FPS
    font = pg.font.Font(None, 32)  # Default font, size 32

    # Sprite groups
    all_sprites = pg.sprite.Group()  # Holds all sprites
    enemies = pg.sprite.Group()      # Holds only enemies

    # Create player in the center of the screen
    player = Player((WIDTH // 2, HEIGHT // 2))
    all_sprites.add(player)

    # Game state variables
    timer = 0.0      # Tracks time between enemy spawns
    elapsed = 0.0    # Tracks total survival time
    running = True   # Main loop flag
    alive = True     # Player alive flag

    # Main game loop
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        elapsed += dt  # Increment survival time

        # Event handling
        for e in pg.event.get():
            if e.type == pg.QUIT:  # Window closed
                running = False
            if alive and e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                running = False
            if not alive and e.type == pg.KEYDOWN and e.key == pg.K_r:
                return main()  # Restart game by calling main again

        # Game logic (only if player is alive)
        if alive:
            timer += dt
            # Spawn enemy if enough time has passed
            if timer >= ENEMY_SPAWN_EVERY:
                timer = 0.0
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)

            # Update all sprites
            all_sprites.update(dt)
            # Check collision between player and enemies
            if pg.sprite.spritecollide(player, enemies, dokill=False):
                alive = False  # Player dies

        # Drawing
        screen.fill((20, 20, 28))  # Dark background
        all_sprites.draw(screen)   # Draw all sprites

        # Draw UI text
        if alive:
            msg = f"Time: {elapsed:.1f}s   Enemies: {len(enemies)}"
        else:
            msg = f"You crashed! Survived {elapsed:.1f}s. Press R to retry."
        screen.blit(font.render(msg, True, "white"), (10, 10))

        pg.display.flip()  # Update the display

    pg.quit()  # Clean up and close pygame


# Run the game if this script is the main program
if __name__ == "__main__":
    main()
