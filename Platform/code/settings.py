import pygame
from os import walk
from os.path import join
from pytmx.util_pygame import load_pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
TILE_SIZE = 64 
FRAMERATE = 60
BG_COLOR = '#fcdfcd'

### Game Settings ###

# Player Settings
PLAYER_SPEED = 350
PLAYER_ANIMATION_SPEED = 10
PLAYER_JUMP_ACCELERATION = 1000
GRAVITY = 1800

WORM_SPEED = 100

