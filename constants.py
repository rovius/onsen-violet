import pygame

onsen = {
    "jingle": "assets/jingle.ogg",
    "logo": "assets/onsen.png"
}

clr = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
}

img = {
    "title": "assets/home/title.png",
    "star": "assets/level/star.png",
    "fear": "assets/fear.png"
}

snd = {
    "home": "assets/home/breathe.ogg",
    "star": "assets/level/mastery_star.ogg",
    "harmony": "assets/fear.ogg",
}
    
game = {
    "name": "MUSE Adventure",
    "codename": "violet",
    "width": 1280,
    "height": 720,
    "fps": 60,
    "tracks": 4,
    "block_size": 50,
    "block_speed": 10,
    "char_size": 50,
    "char_speed": 10,
    "star_size": 50,
    "star_speed": 10,
}

fonts = {
    "vt": "assets/font/vt.ttf",
    "fira": "assets/font/fira.ttf",
    "disket": "assets/font/disket.ttf"
}

screen = pygame.display.set_mode(((game["width"], game["height"])), pygame.SCALED)
pygame.display.set_caption(game["name"])
clock = pygame.time.Clock()