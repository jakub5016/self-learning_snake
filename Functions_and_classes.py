from time import sleep
import pygame
import os
import random

WIDTH = HEIGHT = 900
#WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption("Snake")
BACKGROUND = (186, 255, 255)
FPS = WIDTH/20
CLOCK = pygame.time.Clock()

SNAKE_HEAD_IMG = pygame.image.load(os.path.join('Assets', 'Snake_head.png'))
SNAKE_TAIL_IMG = pygame.image.load(os.path.join('Assets', 'Snake_tail.png'))
SNAKE_HEAD = SNAKE_HEAD_IMG
STAR_IMG = pygame.image.load(os.path.join('Assets', 'Star.png'))

SPEED = 15


def blit(img, x, y): # Use it later!
    pygame.display.set_mode((WIDTH, HEIGHT)).blit(img, (x, y))

def star_position(constant):
    return random.randint(7, round((constant/15)-7))*15

# Classes for snake construction
class Snake_head:
    def __init__(self):
        self.Rectangle = pygame.Rect(WIDTH/2, HEIGHT/2, SNAKE_HEAD_IMG.get_width(), SNAKE_HEAD_IMG.get_height()) # Head hitbox
        self.Vector = [0,-1] # Going up
        pygame.display.set_mode((WIDTH, HEIGHT)).blit(SNAKE_HEAD_IMG, (self.Rectangle.x, self.Rectangle.y))
    
    def move(self):
        self.Rectangle.x += self.Vector[0] * SPEED
        if self.Rectangle.x > WIDTH :
            self.Rectangle.x = 15
        if self.Rectangle.x < 0 :
            self.Rectangle.x = WIDTH-15
        
        self.Rectangle.y += self.Vector[1] * SPEED
        if self.Rectangle.y > HEIGHT :
            self.Rectangle.y = 15
        if self.Rectangle.y < 0 :
            self.Rectangle.y = HEIGHT-15

        pygame.display.set_mode((WIDTH, HEIGHT)).blit(SNAKE_HEAD, (self.Rectangle.x, self.Rectangle.y))
    
    def rotate(self, side):
        global SNAKE_HEAD_IMG 
        global SNAKE_HEAD
        
        if side == 0 and (self.Vector != [0, 1]):
            self.Vector = [0,-1] 
            SNAKE_HEAD = pygame.transform.rotate(SNAKE_HEAD_IMG, side)
        
        if side == 90 and (self.Vector != [1, 0]):
            self.Vector = [-1,0] 
            SNAKE_HEAD = pygame.transform.rotate(SNAKE_HEAD_IMG, side)
        
        if side == 180 and (self.Vector != [0, -1]):
            self.Vector = [0,1] 
            SNAKE_HEAD = pygame.transform.rotate(SNAKE_HEAD_IMG, side)
        
        if side == 270 and (self.Vector != [-1, 0]):
            self.Vector = [1,0] 
            SNAKE_HEAD = pygame.transform.rotate(SNAKE_HEAD_IMG, side)

        
class Snake_tail:
    def __init__(self, x = (WIDTH/2) , y = (WIDTH/2)+SPEED, base_Vector = [0,-1]):
        self.Rectangle = pygame.Rect(x, y, SNAKE_HEAD_IMG.get_width(), SNAKE_HEAD_IMG.get_height())
        self.Vector = base_Vector # Going up        
        pygame.display.set_mode((WIDTH, HEIGHT)).blit(SNAKE_TAIL_IMG, (self.Rectangle.x, self.Rectangle.y))
    
    def move(self, x, y):
        self.Rectangle.x = x
        self.Rectangle.y = y
        pygame.display.set_mode((WIDTH, HEIGHT)).blit(SNAKE_TAIL_IMG, (self.Rectangle.x, self.Rectangle.y))


class Snake(Snake_head):
    def __init__(self):
        super().__init__()
        self.list_of_tails = [Snake_tail(), Snake_tail()]
        self.places = [[(WIDTH/2) + SPEED, (HEIGHT/2) + SPEED], [(WIDTH/2) + 2*SPEED, (HEIGHT/2) + 2*SPEED]]   
        self.score = 0
    
    def append(self):
        x = (self.list_of_tails[-1].Rectangle.x)
        y = (self.list_of_tails[-1].Rectangle.y)
        Vector_x = (self.list_of_tails[-1].Vector[0])
        Vector_y = (self.list_of_tails[-1].Vector[1])

        self.list_of_tails.append(Snake_tail(x= x - (SPEED* Vector_x), y = y - (SPEED* Vector_y)))
        self.places.append([x, y])
    
    def move(self):       
        # Vectors
        self.list_of_tails[0].Vector = self.Vector ###

        overwrite = []
        i = 0
        while i < len(self.list_of_tails): # PYTHON YOU SUCCC
            overwrite.append(self.list_of_tails[i].Vector)
            i = i+1
        
        i=0
        while i < len(self.list_of_tails)-1:
            self.list_of_tails[i+1].Vector = overwrite[i]
            i=i+1

        # Places
        self.places[0] = [self.Rectangle.x, self.Rectangle.y]
        
        super().move()
        
        overwrite = []
        i = 0
        while i < len(self.places): # PYTHON YOU SUCCC
            overwrite.append(self.places[i])
            i = i+1
        
        i=0
 
        while i < len(self.places)-1:
            self.places[i+1] = overwrite[i]
            i=i+1
        
        i = 1
        while i < len(self.list_of_tails):
            self.list_of_tails[i].move(self.places[i][0], self.places[i][1])
            i = i +1

    def rotate(self, side):
        super().rotate(side)    

    def lose_condition(self):

        for i in range(len(self.list_of_tails)):
            if (self.list_of_tails[i].Rectangle.x == self.Rectangle.x) and (self.list_of_tails[i].Rectangle.y == self.Rectangle.y) and (i != 0):
                print(self.list_of_tails[i].Rectangle.y, self.list_of_tails[i].Rectangle.x)
                return True
        return False
    
    def collect_star(self, Star):
        if (Star.Rectangle.x == self.Rectangle.x) and (Star.Rectangle.y == self.Rectangle.y):
            Star.change_position()
            self.append()
            self.score +=1
            return True

class Star:
    def __init__(self, x, y):
        self.Rectangle = pygame.Rect(x, y, STAR_IMG.get_width(), STAR_IMG.get_height()) # Creating rectangle
        blit(STAR_IMG, x, y)

    def draw(self):
        blit(STAR_IMG, self.Rectangle.x, self.Rectangle.y)
    
    def change_position(self):
        self.Rectangle.x = star_position(WIDTH)
        self.Rectangle.y = star_position(HEIGHT)
