import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 480, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game with Levels")

clock = pygame.time.Clock()

# Load backgrounds
backgrounds = [
    pygame.transform.scale(pygame.image.load(f"assets/background{i}.png"), (WIDTH, HEIGHT))
    for i in range(1, 4)
]

# Load car and obstacle
car = pygame.transform.scale(pygame.image.load("assets/car.png"), (60, 100))
obstacle_img = pygame.transform.scale(pygame.image.load("assets/obstacle.png"), (60, 100))

# Music
pygame.mixer.music.load("assets/sound.mp3")
pygame.mixer.music.play(-1)

# Fonts
font = pygame.font.SysFont("Arial", 28)

# Car position
car_x = WIDTH // 2 - 30
car_y = HEIGHT - 120
car_speed = 7

# Background scroll
bg_y1 = 0
bg_y2 = -HEIGHT
bg_speed = 5

# Obstacles
obstacles = []
obstacle_speed = 5
obstacle_timer = 0

# Score & level
score = 0
level = 1
prev_level = 1
show_level_up = False
level_up_timer = 0
level_completed = False
level_completed_timer = 0

# Distance tracking
distance_covered = 0

def get_level_distance(level):
    return 4000 + (level - 1) * 1500

def draw_background(current_bg):
    global bg_y1, bg_y2, distance_covered
    screen.blit(current_bg, (0, bg_y1))
    screen.blit(current_bg, (0, bg_y2))

    bg_y1 += bg_speed
    bg_y2 += bg_speed
    distance_covered += bg_speed

    if bg_y1 >= HEIGHT:
        bg_y1 = -HEIGHT
    if bg_y2 >= HEIGHT:
        bg_y2 = -HEIGHT

def draw_text(text, x, y, color=(255, 255, 255)):
    txt = font.render(text, True, color)
    screen.blit(txt, (x, y))

def draw_progress_bar(current, total):
    bar_width = 300
    bar_height = 20
    x = WIDTH // 2 - bar_width // 2
    y = HEIGHT - 40

    # Bar background
    pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height), border_radius=10)

    # Filled progress
    fill_width = int(bar_width * min(current / total, 1))
    pygame.draw.rect(screen, (0, 200, 0), (x, y, fill_width, bar_height), border_radius=10)

    # Border
    pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2, border_radius=10)

    # Text above bar
    draw_text(f"{min(int(current), int(total))} / {int(total)}", x + 100, y - 25)

def reset_game():
    global score, level, prev_level, car_x, obstacles
    global bg_y1, bg_y2, obstacle_speed, bg_speed
    global distance_covered, level_completed, show_level_up

    score = 0
    level = 1
    prev_level = 1
    car_x = WIDTH // 2 - 30
    obstacles = []
    bg_y1 = 0
    bg_y2 = -HEIGHT
    obstacle_speed = 5
    bg_speed = 5
    distance_covered = 0
    level_completed = False
    show_level_up = False

running = True
game_over = False

while running:
    screen.fill((0, 0, 0))

    current_bg = backgrounds[(level - 1) % len(backgrounds)]
    draw_background(current_bg)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT] and car_x > 10:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < WIDTH - 70:
            car_x += car_speed

        screen.blit(car, (car_x, car_y))

        # Spawn obstacles
        obstacle_timer += 1
        if obstacle_timer > 40:
            x_pos = random.randint(50, WIDTH - 110)
            obstacles.append([x_pos, -100])
            obstacle_timer = 0

        # Move obstacles
        for obs in obstacles[:]:
            obs[1] += obstacle_speed
            screen.blit(obstacle_img, (obs[0], obs[1]))

            # Collision detection
            if (
                car_y < obs[1] + 100 and car_y + 100 > obs[1] and
                car_x < obs[0] + 60 and car_x + 60 > obs[0]
            ):
                game_over = True

            # Off-screen removal
            if obs[1] > HEIGHT:
                obstacles.remove(obs)
                score += 1

        # Check level completion by distance
        if distance_covered >= get_level_distance(level) and not level_completed:
            level_completed = True
            level_completed_timer = pygame.time.get_ticks()
            distance_covered = 0

        # Display "Level X Completed!" message
        if level_completed:
            draw_text(f"✅ Level {level} Completed!", WIDTH // 2 - 150, HEIGHT // 2 - 100, (255, 255, 0))
            if pygame.time.get_ticks() - level_completed_timer > 2000:
                level += 1
                prev_level = level
                show_level_up = True
                level_up_timer = pygame.time.get_ticks()
                level_completed = False
                obstacle_speed = 5 + level
                bg_speed = 5 + level // 2

        # Display "Level X!" after advancing
        if show_level_up:
            draw_text(f"🎉 Level {level}!", WIDTH // 2 - 80, HEIGHT // 2 - 100, (0, 255, 0))
            if pygame.time.get_ticks() - level_up_timer > 2000:
                show_level_up = False

        # Display score & level
        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Level: {level}", 10, 40)

        # Progress bar
        draw_progress_bar(distance_covered, get_level_distance(level))

    else:
        draw_text("GAME OVER", WIDTH // 2 - 100, HEIGHT // 2, (255, 0, 0))
        draw_text("Press R to Restart", WIDTH // 2 - 120, HEIGHT // 2 + 40)
        if keys[pygame.K_r]:
            reset_game()
            game_over = False

    pygame.display.update()
    clock.tick(60)
