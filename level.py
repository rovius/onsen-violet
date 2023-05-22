import pygame
from constants import *
from misc import *
import menus

def start_game():
    pygame.mixer.music.stop()
    running = True
    input = "https://www.youtube.com/watch?v=f1GUKnqEbu0"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input = input[:-1]
                elif event.key == pygame.K_RETURN:
                    try:
                        video_path = ytdl(input)
                        blocks, tempo = generate_level(video_path)
                        start_level(video_path, blocks, tempo)
                    except:
                        draw_text("Invalid URL", fonts["disket"], clr["red"], game["width"] // 2, game["height"] // 2)
                else:
                    input += event.unicode

        screen.fill(clr["black"])
        draw_text("Enter a YouTube URL:", fonts["disket"], clr["white"], game["width"] // 2, game["height"] // 4)
        draw_text(input, fonts["disket"], clr["white"], game["width"] // 2, game["height"] // 2)
        draw_text("Search", fonts["disket"], clr["white"], game["width"] * 7 // 8, game["height"] * 7 // 8)

        pygame.display.flip()
        clock.tick(game["fps"])

def generate_level(song_path: str):
    import librosa
    import numpy as np
    
    y, sr = librosa.load(song_path)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_strengths = onset_env[beats]
    onset_strengths /= np.max(onset_strengths)

    blocks = []
    for i, onset_strength in enumerate(onset_strengths):
        if onset_strength > 0.25: # = threshold
            time = beats[i] / sr
            position = time * tempo * game["fps"] * game["block_speed"]
            track = np.random.randint(game["tracks"])

            print(time, tempo, position)

            if onset_strength < 0.25:
                color = clr["cyan"]
            elif onset_strength < 0.5:
                color = clr["green"]
            elif onset_strength < 0.75:
                color = clr["yellow"]
            else:
                color = clr["red"]

            block = {
                "track": track,
                "position": position,
                "color": color,
                "size": game["block_size"],
            }

            blocks.append(block)
    return blocks, tempo

# Define a function to draw a block on the screen
def draw_block(block):
    # Get the track, position, color and size of the block
    track = block["track"]
    position = block["position"]
    color = block["color"]
    size = block["size"]

    # Calculate the x and y coordinates of the block based on its track and position
    x = (track + 0.5) * game["width"] / game["tracks"]
    y = position

    # Draw a rectangle on the screen with the given color and size
    pygame.draw.rect(screen, color, (x - size // 2, y - size // 2, size, size))

# Define a function to draw the character on the screen
def draw_character(character):
    # Get the track and color of the character
    track = character["track"]
    color = character["color"]

    # Calculate the x and y coordinates of the character based on its track
    x = (track + 0.5) * game["width"] / game["tracks"]
    y = game["height"] - game["char_size"] // 2

    # Draw a circle on the screen with the given color and size
    pygame.draw.circle(screen, color, (x, y), game["char_size"] // 2)

# Define a function to draw a star on the screen
def draw_star(star):
    # Get the x, y and color of the star
    x = star["x"]
    y = star["y"]
    color = star["color"]

    # Load the star image and scale it to the star size
    star_image = pygame.image.load(img["star"]).convert_alpha()
    star_image = pygame.transform.scale(star_image, (game["star_size"], game["star_size"]))

    # Draw the star image on the screen with the given x and y coordinates
    screen.blit(star_image, (x - game["star_size"] // 2, y - game["star_size"] // 2))

# Define a function to check if a block and a character are colliding
def is_colliding(block, character):
    # Get the track and position of the block
    block_track = block["track"]
    block_position = block["position"]

    # Get the track of the character
    character_track = character["track"]

    # Check if the block and the character are on the same track
    if block_track == character_track:
        # Check if the block and the character are close enough in position
        if abs(block_position - (game["height"] - game["char_size"] // 2)) < (game["block_size"] + game["char_size"]) // 2:
            # Return True if they are colliding
            return True

    # Return False otherwise
    return False

# Define a function to show the result screen
def show_result_screen(score, total, video_path, blocks, tempo):
    # Calculate the percentage of blocks collected
    percentage = score / total

    # Calculate the number of stars earned based on the percentage
    if percentage < 0.6:
        stars = 1
    elif percentage < 0.8:
        stars = 2
    else:
        stars = 3

    # Create a boolean variable to indicate if the result screen is running
    results_running = True

    # Create a loop for the result screen
    while results_running:
        # Handle events
        for event in pygame.event.get():
            # If the user quits, exit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # If the user taps the screen, go back to the main menu or replay the level
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if the mouse is on the main menu button
                if mouse_x > game["width"] // 4 and mouse_x < game["width"] * 3 // 4 and mouse_y > game["height"] * 3 // 4 and mouse_y < game["height"] * 7 // 8:
                    # Go back to the main menu
                    running = False
                    menus.home()

                # Check if the mouse is on the replay button
                elif mouse_x > game["width"] // 4 and mouse_x < game["width"] * 3 // 4 and mouse_y > game["height"] // 2 and mouse_y < game["height"] * 5 // 8:
                    # Replay the level
                    running = False
                    start_level(video_path, blocks, tempo)

        # Draw the stars, the percentage and the buttons on the screen
        screen.fill(clr["black"])
        for i in range(stars):
            draw_star({
                "x": (i + 1) * game["width"] / (stars + 1),
                "y": game["height"] // 4,
                "color": clr["white"],
            })
        draw_text(f"{percentage * 100:.0f}%", fonts["disket"], clr["white"], game["width"] // 2, game["height"] // 8)
        draw_text("MAIN MENU", fonts["disket"], clr["white"], game["width"] // 2, game["height"] * 7 // 8)
        draw_text("REPLAY", fonts["disket"], clr["white"], game["width"] // 2, game["height"] * 5 // 8)

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(game["fps"])

# Define a function to start a level
def start_level(video_path, blocks, tempo):
    running = False
    # Load the video and play it
    video = pygame.mixer.music.load(video_path)
    pygame.mixer.music.play()

    # Create a character as a dictionary with its track and color
    character = {
        "track": game["tracks"] // 2,
        "color": clr["magenta"],
    }

    stars = []
    score = 0
    level_running = True

    while level_running:
        # Handle events
        for event in pygame.event.get():
            # If the user quits, exit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # If the user presses a key, move the character
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Move the character to the left track if possible
                    if character["track"] > 0:
                        character["track"] -= 1
                elif event.key == pygame.K_RIGHT:
                    # Move the character to the right track if possible
                    if character["track"] < game["tracks"] - 1:
                        character["track"] += 1

        # Update the blocks and the stars
        for block in blocks:
            # Move the block down by its speed
            block["position"] += game["block_speed"]

            # Check if the block is colliding with the character
            if is_colliding(block, character):
                # Increase the score by one
                score += 1

                # Remove the block from the list of blocks
                blocks.remove(block)

                # Create a star as a dictionary with its x, y and color
                star = {
                    "x": (block["track"] + 0.5) * game["width"] / game["tracks"],
                    "y": game["height"] - game["char_size"] // 2,
                    "color": block["color"],
                }

                # Add the star to the list of stars
                stars.append(star)

        for i, star in enumerate(stars):
            # Move the star up by its speed
            star["y"] += game["star_speed"]

            # Remove the star from the list of stars if it goes off the screen
            if star["y"] < 0:
                stars.pop(i)

        # Draw the blocks, the character and the stars on the screen
        screen.fill(clr["black"])
        for block in blocks:
            draw_block(block)
        draw_character(character)
        for star in stars:
            draw_star(star)

        # Draw the score on the screen
        draw_text(f"{score}", fonts["disket"], clr["white"], 32, 32)

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(game["fps"])

        # Check if the video is over
        if not pygame.mixer.music.get_busy():
            # Stop the level and show the result screen
            running = False
            show_result_screen(score, len(blocks) + score, video_path, blocks, tempo)