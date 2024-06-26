import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CARTOON_FONT_PATH = 'Creepster-Regular.ttf'  # Replace with your font file path
CARTOON_FONT_SIZE = 48
GAME_FONT = pygame.font.Font(CARTOON_FONT_PATH, CARTOON_FONT_SIZE)

# Game settings
GRAVITY = 0.3
JUMP_STRENGTH = -10
OBSTACLE_SPEED = 5
GAP_SIZE = 250

# Load knight animation frames
KNIGHT_FRAMES = []
for i in range(0, 6):  # there are 6 frames
    img = pygame.image.load(f'knight{i}.png')
    img = pygame.transform.scale(img, (60, 60))  # Smaller size
    KNIGHT_FRAMES.append(img)

# Load obstacle images
DRAGON_IMG = pygame.image.load('dragon.png')
DRAGON_IMG = pygame.transform.scale(DRAGON_IMG, (200, 200))

ZOMBIE_IMG = pygame.image.load('zombie.png')
ZOMBIE_IMG = pygame.transform.scale(ZOMBIE_IMG, (50, 50))

GIANT_IMG = pygame.image.load('giant.png')
GIANT_IMG = pygame.transform.scale(GIANT_IMG, (150, 150))

GHOST_IMG = pygame.image.load('ghost.png')
GHOST_IMG = pygame.transform.scale(GHOST_IMG, (50, 50))

# Load witch frames from extracted images
WITCH_FRAMES = []
witch_frames_dir = 'c:\\Users\\yourpc\\Downloads\\knight phobia\\witch_frames'  # Adjust this path
witch_frame_files = sorted([f for f in os.listdir(witch_frames_dir) if f.startswith('witch') and f.endswith('.png')])
for frame_file in witch_frame_files:
    img = pygame.image.load(os.path.join(witch_frames_dir, frame_file))
    img = pygame.transform.scale(img, (60, 60))  # Smaller size
    WITCH_FRAMES.append(img)

# List of obstacle images
OBSTACLE_IMGS = [DRAGON_IMG, ZOMBIE_IMG, GIANT_IMG, GHOST_IMG, WITCH_FRAMES]

# Load background image
BACKGROUND_IMG = pygame.image.load('castle_background.png')
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Make start screen image semi-transparent
START_SCREEN_IMG = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
START_SCREEN_IMG.fill((0, 0, 0, 128))  # Semi-transparent black overlay
START_SCREEN_IMG.blit(BACKGROUND_IMG, (0, 0))

# Load play button image
PLAY_BUTTON_IMG = pygame.image.load('play_button.png')
PLAY_BUTTON_RECT = PLAY_BUTTON_IMG.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
GAME_NAME = "Knight Phobia"
CREATOR_TEXT = "Created by sandy25x"

class Knight:
    def __init__(self):
        self.images = KNIGHT_FRAMES
        self.rect = self.images[0].get_rect()
        self.rect.topleft = (50, SCREEN_HEIGHT // 2)  # Start from top left corner
        self.velocity = 0
        self.animation_index = 0
        self.is_alive = True
        self.score = 0
        self.high_score = self.load_high_score()  # Load high score from file

    def update(self):
        if self.is_alive:
            self.velocity += GRAVITY
            self.rect.y += self.velocity
            self.animation_index = (self.animation_index + 1) % len(self.images)

            # Check if knight goes above screen
            if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
                self.is_alive = False
                if self.score > self.high_score:
                    self.high_score = self.score
                self.score = 0  # Reset score on game over

    def jump(self):
        if self.is_alive:
            self.velocity = JUMP_STRENGTH

    def draw(self, screen):
        if self.is_alive:
            screen.blit(self.images[self.animation_index], self.rect.topleft)

    def collide(self, obstacles):
        if self.is_alive:
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle.rect):
                    self.is_alive = False
                    if self.score > self.high_score:
                        self.high_score = self.score
                    self.score = 0  # Reset score on game over
                    return True
        return False

    def load_high_score(self):
        try:
            with open('high_score.txt', 'r') as file:
                high_score_str = file.read().strip()  # Read and strip any whitespace
                if high_score_str:
                    return int(high_score_str)
                else:
                    return 0  # Return 0 if file is empty
        except FileNotFoundError:
            return 0  # Return 0 if file doesn't exist

    def save_high_score(self):
        with open('high_score.txt', 'w') as file:
            file.write(str(self.high_score))

class Obstacle:
    def __init__(self):
        self.image = random.choice(OBSTACLE_IMGS)  # Choose a single image from the list
        if isinstance(self.image, list):  # Check if it's a list (for animation frames)
            self.image = self.image[0]  # Use the first frame initially
        self.rect = self.image.get_rect()
        self.set_initial_position()
        self.animation_index = 0
        self.score_counted = False

    def set_initial_position(self):
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.choice([150, SCREEN_HEIGHT // 2, SCREEN_HEIGHT - 150])
        self.velocity = (-OBSTACLE_SPEED, 0)

    def update(self):
        self.rect.x += self.velocity[0]
        if isinstance(self.image, list):
            self.animation_index = (self.animation_index + 1) % len(self.image)

    def draw(self, screen):
        if isinstance(self.image, list):
            screen.blit(self.image[self.animation_index], self.rect.topleft)
        else:
            screen.blit(self.image, self.rect.topleft)

    def is_off_screen(self):
        return self.rect.right < 0

def draw_text(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)
    return text_rect.width

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    knight = Knight()
    obstacles = []

    background_x = 0
    game_over = False
    game_started = False
    start_screen = True

    creator_text_x = -200  # Start position for moving text

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and knight.is_alive and game_started:
                    knight.jump()
                if event.key == pygame.K_SPACE and (not game_started or not knight.is_alive) and start_screen:
                    start_screen = False
                    game_started = True
                    knight.is_alive = True
                    knight.score = 0
                    knight.rect.topleft = (50, SCREEN_HEIGHT // 2)
                    knight.velocity = 0
                    obstacles.clear()
                if event.key == pygame.K_SPACE and not knight.is_alive and not start_screen:
                    start_screen = True
                    game_started = False
                    knight.save_high_score()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game_started and start_screen and PLAY_BUTTON_RECT.collidepoint(event.pos):
                    start_screen = False
                    game_started = True
                    knight.is_alive = True
                    knight.score = 0
                    knight.rect.topleft = (50, SCREEN_HEIGHT // 2)
                    knight.velocity = 0
                    obstacles.clear()

        if game_started and knight.is_alive:
            knight.update()

            # Add new obstacles
            if len(obstacles) < 3:
                obstacles.append(Obstacle())

            for obstacle in obstacles[:]:
                obstacle.update()
                if obstacle.is_off_screen():
                    obstacles.remove(obstacle)
                if not obstacle.score_counted and obstacle.rect.right < knight.rect.left:
                    knight.score += 1
                    obstacle.score_counted = True

            knight.collide(obstacles)

        # Scroll background
        background_x -= 2
        if background_x <= -SCREEN_WIDTH:
            background_x = 0

        # Draw scrolling background
        screen.blit(BACKGROUND_IMG, (background_x, 0))
        screen.blit(BACKGROUND_IMG, (background_x + SCREEN_WIDTH, 0))

        if start_screen:
            # Draw semi-transparent start screen image
            screen.blit(START_SCREEN_IMG, (0, 0))
            screen.blit(PLAY_BUTTON_IMG, PLAY_BUTTON_RECT)

            # Display game name and creator text
            draw_text(GAME_NAME, GAME_FONT, WHITE, screen, SCREEN_WIDTH // 2 - 100, 100)

            # Display knight image on start screen
            knight_img = pygame.transform.scale(KNIGHT_FRAMES[0], (200, 200))  # Scale down for start screen
            knight_rect = knight_img.get_rect(bottomleft=(50, SCREEN_HEIGHT - 50))  # Adjust position
            screen.blit(knight_img, knight_rect)

        else:
            knight.draw(screen)

            # Draw obstacles
            for obstacle in obstacles:
                obstacle.draw(screen)

            # Display score
            draw_text(f"Score: {knight.score}", GAME_FONT, WHITE, screen, SCREEN_WIDTH - 260, 50)

            # Display high score
            draw_text(f"High Score: {knight.high_score}", GAME_FONT, WHITE, screen, SCREEN_WIDTH - 360, 100)

            # Check if game over
            if not knight.is_alive:
                draw_text("Game Over", GAME_FONT, WHITE, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
                if knight.score > knight.high_score:
                    knight.high_score = knight.score
                draw_text("Press SPACE to Retry", GAME_FONT, WHITE, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50)

        # Display moving credits at the bottom
        draw_text(CREATOR_TEXT, GAME_FONT, WHITE, screen, creator_text_x, SCREEN_HEIGHT - 50)
        creator_text_x += 2
        if creator_text_x > SCREEN_WIDTH:
            creator_text_x = -200  # Reset position for moving text

        # Update screen
        pygame.display.flip()
        clock.tick(60)  # Cap the frame rate at 60 FPS

if __name__ == "__main__":
    main()
