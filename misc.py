import pygame
import os
import subprocess

from constants import screen

def play_sound(sound_path):
    sound = pygame.mixer.Sound(sound_path)
    sound.play()

def draw_text(text, font, color, x, y):
    text_surface = pygame.font.Font(font, 32).render(text, True, color)
    text_rect = text_surface.get_rect(center=(x,y))
    screen.blit(text_surface, text_rect)

def ytdl(url: str, format: str = 'bestaudio/best') -> str:
    output_dir = './songs'

    # Download the video using yt-dlp
    subprocess.run(['yt-dlp', url, '-o', f'{output_dir}/%(id)s.%(ext)s', '-x', '--audio-format', 'mp3'])

    # Find the downloaded video file
    video_filename = os.listdir(output_dir)[-1]  # Get the last file in the directory (the downloaded video)
    mp3_filename = f'{os.path.splitext(video_filename)[0]}.mp3'
    mp3_filepath = os.path.join(output_dir, mp3_filename)

    return mp3_filepath