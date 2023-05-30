import pygame, cv2, random, os

pygame.init()

window_width = 1280
window_height = 860
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Memory Game')

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

FPS = 60
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
         running = False

pygame.quit()