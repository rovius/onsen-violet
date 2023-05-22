import time
import pygame
import math
from constants import *
from level import start_game, generate_level, start_level
from misc import draw_text, play_sound

# Define a function to show the loading screen
def loading(screen, ml: bool = False):
    if ml:
        jingle = snd["harmony"]
        logo = img["fear"]
    else:
        jingle = onsen["jingle"]
        logo = onsen["logo"]

    logo = pygame.image.load(logo).convert_alpha()
    logo_rect = logo.get_rect(center=(game["width"] // 2, game["height"] // 2))
    sound = pygame.mixer.Sound(jingle)
    
    if not ml:
        play_sound(sound)
        screen.fill(clr["black"])
        screen.blit(logo, logo_rect)
        pygame.display.flip()
    else:
        screen.fill(clr["black"])
        pygame.display.flip()
        play_sound(sound)
        pygame.time.wait(8750)
        for c in clr:
            # print(clr[c])
            screen.fill(clr[c])
            pygame.display.flip()
            pygame.time.wait(25)
        screen.fill(clr["black"])
        screen.blit(logo, logo_rect)
        pygame.display.flip()
        pygame.time.wait(9250)
        draw_text("i'm sorry", fonts["vt"], clr["white"], game["width"] // 8, game["height"] // 16)
        pygame.display.flip()

    timeout = math.ceil(sound.get_length())
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < timeout * 1000:
        if not pygame.mixer.music.get_busy:
            pygame.quit()
        else:
            pygame.event.pump()
            pygame.time.wait(100)

    if not ml:
        home()

# Define a function to show the main menu
def home():
    # Load the title and the breathe music
    title = pygame.image.load(img["title"]).convert_alpha()
    title_rect = title.get_rect(center=(game["width"] // 2, game["height"] // 2))

    # Load menu music
    pygame.mixer.music.load(snd["home"])
    pygame.mixer.music.play(-1)

    # Create a boolean variable to indicate if the main menu is running
    menu = True

    # Create a loop for the main menu
    while menu:
        # Handle events
        for event in pygame.event.get():
            # If the user quits, exit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                print(f"Window resized to {event.size}")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                menu = False
                test_song = "./test-songs/velvet_v2.ogg"
                blocks,tempo=generate_level(test_song)
                start_level(test_song, blocks, tempo)

        # Draw the title and the text on the screen
        screen.fill(clr["black"])
        screen.blit(title, title_rect)
        draw_text("tap to play", fonts["disket"], clr["white"], game["width"] * 0.5, game["height"] * 0.75)

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(game["fps"])

