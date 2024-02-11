import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600  # Screen dimensions
FPS = 60  # Frames per second

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        # Load the image for the player character
        self.image = pygame.image.load('human.png')  # Replace 'human.png' with the actual image file
        self.rect = self.image.get_rect()  # Get the rectangle of the image
        self.rect.center = (100, HEIGHT - 50)  # Initial position of the player
        self.speed = 5  # Movement speed
        self.jump_height = -15  # Jump height
        self.gravity = 1  # Gravity
        self.velocity = pygame.Vector2(0, 0)  # Player's velocity
        self.health = 100  # Player's health
        self.lives = 3  # Player's lives

    def update(self):
        # Update player's position based on keyboard input
        keys = pygame.key.get_pressed()
        self.velocity.x = 0

        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed

        self.velocity.y += self.gravity
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Keep player within screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        # Prevent player from falling off the screen
        if self.rect.top > HEIGHT:
            self.rect.y = HEIGHT - self.rect.height
            self.health -= 10

    def jump(self):
        # Make the player jump
        self.velocity.y = self.jump_height

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load the image for enemies
        self.image = pygame.image.load('animal.png')  # Replace 'animal.png' with the actual image file
        self.rect = self.image.get_rect()  # Get the rectangle of the image
        self.rect.x = x  # Initial x position
        self.rect.y = y  # Initial y position
        self.speed = 3  # Movement speed

    def update(self):
        # Move the enemy towards the left and respawn if it goes off the screen
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = WIDTH

# Projectile Class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Create a red rectangular projectile
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()  # Get the rectangle of the image
        self.rect.x = x  # Initial x position
        self.rect.y = y  # Initial y position
        self.speed = 10  # Movement speed

    def update(self):
        # Move the projectile towards the right and remove it if it goes off the screen
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()  # Remove the projectile from the sprite group

# Collectible Class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Create a green rectangular collectible
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 0))  # Green color for collectible
        self.rect = self.image.get_rect()  # Get the rectangle of the image
        self.rect.x = x  # Initial x position
        self.rect.y = y  # Initial y position

# Initialize Game
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window
pygame.display.set_caption("Animal vs Human Game")  # Set the window title
clock = pygame.time.Clock()  # Create a clock object to control the frame rate

all_sprites = pygame.sprite.Group()  # Group to hold all sprites
enemies = pygame.sprite.Group()  # Group to hold enemy sprites
projectiles = pygame.sprite.Group()  # Group to hold projectile sprites
collectibles = pygame.sprite.Group()  # Group to hold collectible sprites

player = Player()  # Create the player object
all_sprites.add(player)  # Add player to the sprite group

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()  # Trigger player jump when SPACE key is pressed
            elif event.key == pygame.K_q:
                # Create a projectile when Q key is pressed
                projectile = Projectile(player.rect.right, player.rect.centery)
                all_sprites.add(projectile)
               
# Spawn Enemies
    if pygame.time.get_ticks() % 100 == 0:
        enemy = Enemy(WIDTH, HEIGHT - 50)
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Update
    all_sprites.update()
    hits = pygame.sprite.groupcollide(enemies, projectiles, True, True)
    for hit in hits:
        # You can add scoring logic here
        enemy = Enemy(WIDTH, HEIGHT - 50)
        all_sprites.add(enemy)
        enemies.add(enemy)

    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        player.health -= 10
        if player.health <= 0:
            player.lives -= 1
            player.health = 100
            player.rect.center = (100, HEIGHT - 50)

    hits = pygame.sprite.spritecollide(player, collectibles, True)
    for hit in hits:
        # You can add collectible logic here (health boost, extra life, etc.)
        pass

    # Draw
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    # Display health and lives
    font = pygame.font.Font(None, 36)
    health_text = font.render(f'Health: {player.health}', True, WHITE)
    lives_text = font.render(f'Lives: {player.lives}', True, WHITE)
    screen.blit(health_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    pygame.display.flip()
    clock.tick(FPS)

    # Game Over
    if player.lives <= 0:
        running = False
        print("Game Over")

pygame.quit()
sys.exit()
