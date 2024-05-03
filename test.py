import pygame
import sys

screen = pygame.display.set_mode((300, 200))
image = pygame.image.load('nedladdning.jpg')
image = pygame.transform.scale(image, (256, 144))
while True:
    for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
    screen.blit(image, (0, 0))
    pygame.display.update()