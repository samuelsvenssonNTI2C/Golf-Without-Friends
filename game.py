import pygame
import sys
import json
from scripts.ball import Ball
from scripts.map import Map
from scripts.animation import Animation

class Game:
    
    # Intitilizes the game with pygame and declares some variables
    # Returns: None
    def __init__(self):
        pygame.init()
        self.screen = pygame.Surface((256, 144))
        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.scale = self.display.get_width() / self.screen.get_width()
        self.sideview = True
        self.current_map_index = -1
        self.win = False
    
    
    # Handles the input from the player and changes the relevant varibles
    # Returns: None
    def user_input(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                case pygame.MOUSEBUTTONDOWN:
                    if self.golf_ball.resultant == [0, 0]:
                        self.golf_ball.selected = True
                        
                case pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_f:
                        if self.golf_ball.resultant == [0, 0]:
                            self.sideview = not self.sideview
                            self.golf_ball.in_block = True
                            if self.sideview:
                                self.golf_ball.depth = self.golf_ball.y
                                self.golf_ball.y = self.screen.get_height() - 16 - self.golf_ball.radius # put golf ball on ground
                            else:
                                self.golf_ball.y = self.golf_ball.depth
    
    
    # Draws the map and return the hitboxes of the map and the current map
    # Parameters:
    #   - Map map
    # Returns: list hitboxes, dict current_map
    def draw_map(self, map: Map):
        if self.sideview:
            map.draw_side()
            hitboxes = map.side_hitboxes
            current_map = map.side_map
        else:
            map.draw_top()
            hitboxes = map.top_hitboxes
            current_map = map.top_map
        return hitboxes, current_map

    
    # Changes the map to the next and resets the ball and sets the view to sideview
    # Returns: Map
    def next_map(self):
        maps = json.load(open('maps.json'))
        if self.current_map_index < len(maps)-1:
            self.current_map_index += 1
            map = Map(self.screen, maps[self.current_map_index])
            self.golf_ball = Ball(self.screen, self.scale, map.side_map['starting_point'])
            self.sideview = True
            return map
        else:
            raise Exception('No more maps')
    
    
    # Controls the movement of the ball and its collisions If the ball gets to the goal it returns the block index of the goal 
    # Parameters:
    #   - Map map
    #   - list hitboxes
    #   - dict current_map
    # Returns: int
    def movement(self, map: Map, hitboxes: list, current_map: dict):
        winblock_index = -1
        self.golf_ball.friction(Map.background[current_map['background']]['friction'])  # constant friction from background
        collided_with = self.golf_ball.move(hitboxes, current_map)
        if collided_with != -1 and collided_with < len(current_map['blocks']):
            if not self.golf_ball.in_block and self.sideview:
                self.golf_ball.friction(map.materials[current_map['blocks'][collided_with]['type']]['friction'])
            if current_map['blocks'][collided_with]['type'] == 'victory_block':
                self.win = True
                winblock_index = collided_with
        return winblock_index
    
    
    # The main game
    # Returns: None
    def run(self):
        # Declares varibles
        clock = pygame.time.Clock()
        fps = 60
        goal_animation = Animation(self.display, 'animations/goal_confetti', 0.4, (-64, -100))
        map = self.next_map()
        font = pygame.font.Font(size = 30)
        hitboxes, current_map = self.draw_map(map)
        
        # Main loop
        while True:
            self.screen.blit(Map.background[current_map['background']]['texture'], (0, 0))
            hitboxes, current_map = self.draw_map(map)
            
            self.user_input()
                                         
            if not self.sideview:
                self.golf_ball.on_ground = True 
            self.golf_ball.gravity()
            
            if self.golf_ball.selected == True:
                self.golf_ball.shoot()           
                    
            winblock_index = self.movement(map, hitboxes, current_map)

            self.golf_ball.update()
            
            self.display.blit(pygame.transform.scale(self.screen, self.display.get_size()), (0, 0))
            
            if self.win:
                if goal_animation.draw(([coord * 16 * self.scale for coord in current_map['blocks'][winblock_index]['position']])):
                    self.win = False
                    map = self.next_map()
                    
            self.display.blit(font.render('Shots: ' + str(self.golf_ball.shots), True, (0, 0, 0)), (20, 20))
            pygame.display.update()

            clock.tick(fps) # sets framerate

Game().run()    # Starts the game