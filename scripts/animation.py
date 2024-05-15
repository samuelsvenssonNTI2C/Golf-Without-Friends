import os
import pygame

# An animation class which can handle an animation
# Returns: class Animation
class Animation():
    
    # Intitilizes an animation class
    # Parameters:
    #   - Surface screen
    #   - PathLike folder_name
    #   - float scale
    #   - list offsets
    # Returns: None
    def __init__(self, screen: pygame.Surface, folder_name: os.PathLike, scale: float, offsets: list):
        self.screen = screen
        self.images = []
        self.offsets = offsets
        for image in os.listdir(folder_name):
            self.images.append(pygame.transform.scale_by(pygame.image.load(folder_name + '/' + image), scale))
        self.number_of_frames = len(self.images)
        self.frame = 0
    
    
    # Draws out one frame of the animation, increases frame counter and returns True if animation is finished
    # Parameters:
    #   - list coordinates
    # Returns Bool
    def draw(self, coordinates: list):
        coordinates = [coordinates[i] + self.offsets[i] for i in range(2)]
        drawing_surface = pygame.Surface(self.images[self.frame].get_size(), pygame.SRCALPHA, 32)
        drawing_surface = drawing_surface.convert_alpha()
        drawing_surface.fill((0, 0, 0))
        drawing_surface.fill((0, 0, 0, 0))
        drawing_surface.blit(self.images[self.frame], (0, 0))
        self.screen.blit(drawing_surface, coordinates)
        if self.frame < len(self.images)-1:
            self.frame += 1
            return False
        else:
            self.frame = 0
            return True