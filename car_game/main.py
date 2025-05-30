import pygame
import random
import os
import sys

# Initialize Pygame
pygame.init()

# Create screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Game")

# Clock for frame rate
clock = pygame.time.Clock()

# Colors
RED = (255, 0, 0)

# Load images
def load_image(path, size=None, flip=False):
    if not os.path.exists(path):
        print(f"Image not found: {path}")
        pygame.quit()
        sys.exit()
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    if flip:
        img = pygame.transform.flip(img, False, True)
    return img

# Paths
car_path = os.path.join("images", "lamborghini.png")
car2_path = os.path.join("images", "lamborghini2.png")
road_path = os.path.join("images", "road.jpg")

# Load and scale images
car = load_image(car_path, (250, 250))
car2 = load_image(car2_path, (260, 260), flip=True)
road = load_image(road_path, (3600, 650))

# Fonts
font = pygame.font.SysFont("ComicSansMS", 45)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def reset_game():
    global car_x, car_y, car2_x, car2_y, game_over
    car_x = 100
    car_y = 300
    car2_x = random.randint(100, 640)
    car2_y = -250
    game_over = False

# Initial positions
reset_game()
# Game loop
run = True
car_speed = 10
car2_speed = 8
while run:
    if game_over:
        screen.fill(RED)
        draw_text("Game Over - Press R to Restart", font, (255, 255, 255),60, 250)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
        continue

    clock.tick(60)  # 60 FPS
    screen.blit(road, (-1400, 0))
    screen.blit(car, (car_x, car_y))
    screen.blit(car2, (car2_x, car2_y))

    # Enemy car movement
    car2_y += car2_speed
    if car2_y > screen_height:
        car2_y = -260
        car2_x = random.randint(100, 640)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Get keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        car_y -= car_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        car_y += car_speed
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        car_x -= car_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        car_x += car_speed

    # Clamp car to screen bounds
    car_x = max(0, min(car_x, screen_width - 250))
    car_y = max(0, min(car_y, screen_height - 250))

    # Collision detection
    if abs(car_x - car2_x) < 90 and abs(car_y - car2_y) < 200:
        game_over = True

    pygame.display.update()

pygame.quit()
