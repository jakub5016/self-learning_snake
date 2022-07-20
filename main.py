from ast import And
from nis import match
from statistics import mode
from time import sleep
from traceback import print_tb
from typing import overload
from xmlrpc.server import SimpleXMLRPCDispatcher
import pygame
import os
from enum import Enum  
import random
# Consts
WIDTH = HEIGHT = 900
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
BACKGROUND = (186, 255, 255)
FPS = WIDTH/20
CLOCK = pygame.time.Clock()

SNAKE_HEAD_IMG = pygame.image.load(os.path.join('Assets', 'Snake_head.png'))
SNAKE_TAIL_IMG = pygame.image.load(os.path.join('Assets', 'Snake_tail.png'))
SNAKE_HEAD = SNAKE_HEAD_IMG
STAR_IMG = pygame.image.load(os.path.join('Assets', 'Star.png'))

SPEED = 15

pygame.font.init() 
normal_size = pygame.font.SysFont('Comic Sans MS', round(WIDTH/30))
huge_size = pygame.font.SysFont('Comic Sans MS', round(HEIGHT/18))

pygame.mixer.init()
music = pygame.mixer.music.load(os.path.join('Assets', 'main_theme_1.mp3'))
pygame.mixer.music.play(-1)

# Global functions
def blit(img, x, y): # Use it later!
    WINDOW.blit(img, (x, y))

def star_position(constant):
    return random.randint(7, round((constant/15)-7))*15

# Classes for snake construction
class Snake_head:
    def __init__(self):
        self.Rectangle = pygame.Rect(WIDTH/2, HEIGHT/2, SNAKE_HEAD_IMG.get_width(), SNAKE_HEAD_IMG.get_height()) # Head hitbox
        self.Vector = [0,-1] # Going up
        WINDOW.blit(SNAKE_HEAD_IMG, (self.Rectangle.x, self.Rectangle.y))
    
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

        WINDOW.blit(SNAKE_HEAD, (self.Rectangle.x, self.Rectangle.y))
    
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
        WINDOW.blit(SNAKE_TAIL_IMG, (self.Rectangle.x, self.Rectangle.y))
    
    def move(self, x, y):
        self.Rectangle.x = x
        self.Rectangle.y = y
        WINDOW.blit(SNAKE_TAIL_IMG, (self.Rectangle.x, self.Rectangle.y))


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
    
# Set defult 
WINDOW.fill(BACKGROUND)
pygame.display.update()

def main():
    run = True
    
    label = huge_size.render("Welcome to Snake in Python!", 12, (0,0,0))
    blit(label, (WIDTH/2)-(WIDTH/4), (HEIGHT/2)-(HEIGHT/9))

    label = normal_size.render("Use arrow keys to control the snake", 12, (0,0,0))
    blit(label, (WIDTH/2)-(WIDTH/6), (HEIGHT/2)-(HEIGHT/18))
    label = normal_size.render("Get the highest score by colecting the stars", 12, (0,0,0))
    blit(label, (WIDTH/2)-(WIDTH/4.5), (HEIGHT/2)-(HEIGHT/40))

    pygame.display.update()
    sleep(5)
    while not pygame.key.get_pressed:
        sleep(1)
    
    Hero = Snake()
 
    star_list = [Star(star_position(WIDTH), star_position(HEIGHT))]

    for i in range(int(WIDTH/30)):
        star_list.append(Star(star_position(WIDTH), star_position(HEIGHT)))

    last_score = Hero.score # Save last score to increse difficulty
    while run: # Main loop       
        keys_pressed = pygame.key.get_pressed()
        global FPS 
        local_FPS = Hero.score + FPS
        CLOCK.tick(local_FPS) 
        WINDOW.fill(BACKGROUND)

        if (Hero.score > last_score) and (len(star_list) != WIDTH/60):
            star_list.pop(-1)
            last_score = Hero.score

        # Score sign
        label = normal_size.render("Score: {0}".format(Hero.score), 12, (0,0,0))
        WINDOW.blit(label, (0, 0))
        for i in star_list:
            i.draw()
        

        if keys_pressed[pygame.K_LEFT]:
            Hero.rotate(90)
        if keys_pressed[pygame.K_RIGHT]:
            Hero.rotate(270)
        if keys_pressed[pygame.K_DOWN]:
            Hero.rotate(180)
        if keys_pressed[pygame.K_UP]:
            Hero.rotate(0)  
        if keys_pressed[pygame.K_a]:
            Hero.append()
        
        Hero.move()
        for i in star_list:
            Hero.collect_star(i)
                            
        
        for event in pygame.event.get(): # Getting all the events
            if event.type == pygame.QUIT:
                run = False     
        
        if Hero.lose_condition() == True:
            run = False
        pygame.display.update()
    WINDOW.fill(BACKGROUND)
    # render text

    pygame.mixer.music.stop()
    label = normal_size.render("YOU FAILED!", 1, (0,0,0))
    WINDOW.blit(label, ((WIDTH/2)-(WIDTH/11.25), HEIGHT/2))
    pygame.display.update()
    death_music = pygame.mixer.music.load(os.path.join('Assets', 'death.mp3'))
    pygame.mixer.music.play(-1)    
    sleep(8)
    pygame.quit()            

if __name__ == "__main__": # Checks out file name
    main()