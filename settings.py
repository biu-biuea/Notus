import pygame
import sys
import math

pygame.init()
pygame.mouse.set_visible(False) # hides cursor



# change this when you get the resolution of ur screen

W, H = 1024, 600
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("notus")
clock = pygame.time.Clock()


CREAM       = (249, 246, 240)
WARM_WHITE  = (255, 253, 248)
STONE       = (214, 208, 198)
TAUPE       = (174, 165, 152)
DARK_TAUPE  = (110, 100,  88)
CHARCOAL    = ( 54,  48,  42)
BLUSH       = (224, 196, 183)
SAGE        = (172, 189, 168)
DUSTY_BLUE  = (168, 183, 201)
PIXEL_GRID  = (230, 225, 216)   # this makes subtle dot grid colour