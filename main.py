import pygame
import os
import sqlite3
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def play_sound(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

def draw_button(screen, text, x, y, width, height, inactive_color, active_color):
    font = pygame.font.Font(None, 36)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (x + width / 2, y + height / 2)
    screen.blit(text_surface, text_rect)
    return False

def load_click_count(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT click_count FROM click_counts")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def save_click_count(db_path, click_count):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE click_counts SET click_count = ?", (click_count,))
    conn.commit()
    conn.close()

pygame.init()

pygame.display.set_caption("Cat meme sounder --- created by @TaiyakiSontyo")

icon_path = resource_path("icon.png")
icon_exists = os.path.exists(icon_path)
if icon_exists:
    icon_surface = pygame.image.load(icon_path)
    pygame.display.set_icon(icon_surface)

background_image_path = "background.jpg"

images = [resource_path(image_path) for image_path in ["chipichipicat.png", "girlfriendcat.png", "EDMcat.png", "sekkyoucat.png", "sekkyousarerucat.png", "goat.png", "huhcat.png", "punchcat.png", "happycat.png", "bananadash.png", "bananacry.png", "crycat.png", "ibikicat.png", "bikecat.png", "PCcat.png", "saracat.png", "pakupakucat.png", "niramicat.png", "deencat.png", "gunyacat.png", "sleepycat.png", "Maxwellcat.png", "hagishiricat.png", "DJcat.png", "ikicat.png", "guncat.png", "bikkuricat.png", "sleepycat2.png", "drivecat.png", "godcat.png", "zetsuboucat.png", "laughingdog.png", "gerocat.png", "applecat.png", "nothappycat.png", "waitingforlovecat.png", "mogumogucat.png", "miccat.png", "toothlesscat.png", "mukanjoucat.png"]]
sounds = [resource_path(sound_path) for sound_path in ["chipichipicat.mp3", "girlfriendcat.mp3", "EDMcat.mp3", "sekkyoucat.mp3", "sekkyousarerucat.mp3", "goat.mp3", "huhcat.mp3", "punchcat.mp3", "happycat.mp3", "bananadash.mp3", "bananacry.mp3", "crycat.mp3", "ibikicat.mp3", "bikecat.mp3", "PCcat.mp3", "saracat.mp3", "pakupakucat.mp3", "niramicat.mp3", "deencat.mp3", "gunyacat.mp3", "sleepycat.mp3", "Maxwellcat.mp3", "hagishiricat.mp3", "DJcat.mp3", "ikicat.mp3", "guncat.mp3", "bikkuricat.mp3", "sleepycat2.mp3", "drivecat.mp3", "godcat.mp3", "zetsuboucat.mp3", "laughingdog.mp3", "gerocat.mp3", "applecat.mp3", "nothappycat.mp3", "waitingforlovecat.mp3", "mogumogucat.mp3", "miccat.mp3", "toothlesscat.mp3", "mukanjoucat.mp3"]]

num_columns = min(len(images), 10)
num_rows = len(images) // num_columns + (1 if len(images) % num_columns != 0 else 0)
max_columns = min(len(images), 40)
screen_width = min(num_columns * 400, 1920)
screen_height = min(num_rows * 200, 1080)

screen = pygame.display.set_mode((screen_width, screen_height))

background_image = pygame.transform.scale(pygame.image.load(background_image_path), (screen_width, screen_height))
screen.blit(background_image, (0, 0))

backgrounds = [pygame.transform.scale(pygame.image.load(image_path), (screen_width // num_columns, screen_height // num_rows)) for image_path in images]
for i, background in enumerate(backgrounds):
    row = i // num_columns
    col = i % num_columns
    screen.blit(background, (col * screen_width // num_columns, row * screen_height // num_rows))
pygame.display.flip()

button_width = 140
button_height = 40
button_x = screen_width - button_width - 20
button_y = 20
button_inactive_color = (100, 100, 100)
button_active_color = (150, 150, 150)
button_text = "Exit"

db_path = 'click_count.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS click_counts (click_count INTEGER)")
cursor.execute("INSERT INTO click_counts (click_count) VALUES (0)")
conn.commit()
conn.close()

click_count = load_click_count(db_path)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_click_count(db_path, click_count)
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                index = (y // (screen_height // num_rows)) * num_columns + (x // (screen_width // num_columns))
                if index < len(sounds):
                    if not draw_button(screen, button_text, button_x, button_y, button_width, button_height, button_inactive_color, button_active_color):
                        play_sound(sounds[index])

                        selected_image = pygame.transform.scale(backgrounds[index], (int(screen_width * 0.8), int(screen_height * 0.8)))
                        rect = selected_image.get_rect()
                        rect.center = screen.get_rect().center
                        screen.blit(selected_image, rect)
                        pygame.display.flip()

                        pygame.time.wait(1000)

                        screen.blit(background_image, (0, 0))
                        for i, background in enumerate(backgrounds):
                            row = i // num_columns
                            col = i % num_columns
                            screen.blit(background, (col * screen_width // num_columns, row * screen_height // num_rows))
                        pygame.display.flip()

                        click_count += 1

    if draw_button(screen, button_text, button_x, button_y, button_width, button_height, button_inactive_color, button_active_color):
        save_click_count(db_path, click_count)
        running = False

    font = pygame.font.Font(None, 24)
    text_surface = font.render(f"Click Count: {click_count}", True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.bottomright = (screen_width - 10, screen_height - 10)
    screen.blit(text_surface, text_rect)

    pygame.display.update()

pygame.quit()
