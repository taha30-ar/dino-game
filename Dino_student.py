import pygame
import random

# Initialize Pygame
pygame.init()

# Game Variables
screen_width = 800
screen_height = 600
ground_height = screen_height - 30   # 👈 ارتفاع زمین
dino_height = 60                      # 👈 ارتفاع داینو
dino_width = 70                   # 👈 عرض داینو
dino_pos = [50 , ground_height - dino_height]
cactus_dimensions = [(35, 55), (30, 45)]  # (width, height) for each cactus image
jump_height = 150                     # 👈 ارتفاع پرش
game_speed = 7                      # 👈 سرعت بازی
jumping = False
game_over = False
score = 0

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dino Game with Multiple Cacti")

# Load images
dino_img = pygame.transform.scale(pygame.image.load('Dino.png'), (dino_width, dino_height))   # 👈 نام فایل داینو
cactus_imgs = [
    pygame.transform.scale(pygame.image.load('LargeCactus1.png'), cactus_dimensions[0]),              # 👈 کاکتوس ۱
    pygame.transform.scale(pygame.image.load('LargeCaCtus2.png'), cactus_dimensions[1])               # 👈 کاکتوس ۲
]
track_img = pygame.transform.scale(pygame.image.load('Track.png'), (screen_width, 30))         # 👈 تصویر زمین
game_over_img = pygame.image.load('GameOver.png')                                                 # 👈 تصویر گیم اور

# Font for score
font = pygame.font.Font(None, 36)

# Function to draw ground
def draw_ground():
    screen.blit(track_img, (0, ground_height))  # 👈 محل قرار گرفتن زمین

# Function to draw cacti
def draw_cacti(cacti):
    for cactus in cacti:
        screen.blit(cactus['image'], (cactus['pos_x'], cactus['pos_y']))

# Function to show score
def show_score():
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))  # 👈 مختصات Y امتیاز

# Main game loop
running = True
cactus_list = []  # List to keep track of cacti

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not jumping and not game_over:  # 👈 کلید پرش
            jumping = True
            jump_peak = dino_pos[1] - jump_height

    # Dino jump logic
    if jumping:
        if dino_pos[1] > jump_peak:
            dino_pos[1] -= 11  # 👈 سرعت بالا رفتن
        else:
            jumping = False
    else:
        if dino_pos[1] < ground_height - dino_height:
            dino_pos[1] += 11  # 👈 سرعت پایین آمدن

    # Cactus movement logic
    if not game_over:
        score += 1
        if not cactus_list or cactus_list[-1]['pos_x'] < screen_width - 250:  # 👈 فاصله ایجاد کاکتوس جدید
            cactus_type = random.choice([0, 1])
            new_cactus = {
                'image': cactus_imgs[cactus_type],
                'pos_x': screen_width,
                'pos_y': ground_height - cactus_dimensions[cactus_type][1],
                'width': cactus_dimensions[cactus_type][0],
                'height': cactus_dimensions[cactus_type][1]
            }
            cactus_list.append(new_cactus)

        # Move cacti
        for cactus in cactus_list:
            cactus['pos_x'] -= game_speed

        # Remove cacti that have moved off screen
        cactus_list = [cactus for cactus in cactus_list if cactus['pos_x'] > -cactus['width']]

    # Check for collisions
    for cactus in cactus_list:
        if dino_pos[0] < cactus['pos_x'] + cactus['width'] and cactus['pos_x'] < dino_pos[0] + dino_width:
            if dino_pos[1] + dino_height > cactus['pos_y']:
                game_over = True  # End game on collision

    # Drawing
    screen.fill((255, 255, 255))
    draw_ground()
    draw_cacti(cactus_list)
    show_score()
    screen.blit(dino_img, dino_pos)
    if game_over:
        screen.blit(game_over_img, (screen_width // 2 - game_over_img.get_width() // 2,
                                    screen_height // 2 - game_over_img.get_height() // 2))
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)  # 👈 FPS

pygame.quit()
