import pygame 
import sys
import random
from os import path
from config import *
from sprites import *

#stores the x and y cordinates of preloaded terrain
valid_spawning_area = []

num_lions = 3
lion_group = pygame.sprite.Group()

num_wolves = 5
wolf_group = pygame.sprite.Group()

num_rabbits = 10
rabbit_group = pygame.sprite.Group()

num_deers = 7
deer_group = pygame.sprite.Group()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()
    
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data =[]
        with open(path.join(game_folder,'map.txt'),'r') as file:
            for line in file:
                self.map_data.append(line.strip())
            file.close()

    def new(self):
        self.all_sprites =pygame.sprite.Group()
        self.water = pygame.sprite.Group()
        self.boundary = pygame.sprite.Group()
        self.mountain = pygame.sprite.Group()
        self.grass = pygame.sprite.Group()
        #generate input map 
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == 'm':
                    Mountain(self,col,row)
                if tile == 'b':
                   Boundary(self,col,row)
                   pass
                if tile == 'w':
                    water(self,col,row)
                if tile =='.':
                    Grass(self,col,row)
                    valid_spawning_area.append((col,row))
        #generate random spawning lions
        for i in range(num_lions):
            randxy = [random.choice(valid_spawning_area)]
            self.lion = Lion(self,randxy[0][0],randxy[0][1])
            lion_group.add(self.lion)

        #generate random spawning wolves
        for i in range(num_wolves):
            randxy = [random.choice(valid_spawning_area)]
            self.wolf = Wolf(self,randxy[0][0],randxy[0][1])
            wolf_group.add(self.wolf)

        #generate random spawning rabbits
        for i in range(num_rabbits):
            randxy = [random.choice(valid_spawning_area)]
            self.rabbit = Rabbit(self,randxy[0][0],randxy[0][1])
            rabbit_group.add(self.rabbit)

        #generate random spawning deer
        for i in range(num_deers):
            randxy = [random.choice(valid_spawning_area)]
            self.deer = Deer(self,randxy[0][0],randxy[0][1])
            deer_group.add(self.deer)

        
              
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

      #update portion of the gameloop
    def update(self):
        self.all_sprites.update()

    def draw_grid(self):
        for i in range(NO_OF_BLOCKS_WIDE):
            new_height =round(i*GRIDHEIGHT)
            new_width = round(i*GRIDWIDTH)
            pygame.draw.line(self.screen,BLACK,(0,new_height),(WIDTH,new_height),2)
            pygame.draw.line(self.screen,BLACK,(new_width,0),(new_width,HEIGHT),2)

    def draw(self):
        self.screen.fill(DARKGREY)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        pygame.display.flip()

    def events(self):
    #random lion movement 
        for lion in lion_group:
            x = random.randint(-1,1); y= random.randint(-1,1)
            lion.move(x,y)
        
    #random wolf movement
        for wolf in wolf_group:
            x = random.randint(-1,1); y= random.randint(-1,1)
            wolf.move(x,y)

    #random rabbit movement
        for rabbit in rabbit_group:
            x = random.randint(-1,1); y= random.randint(-1,1)
            rabbit.move(x,y)

    #random deer movement
        for deer in deer_group:
            x = random.randint(-1,1); y= random.randint(-1,1)
            deer.move(x,y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing =False
                pygame.quit()
                sys.exit()
            
            
g = Game()
while True:
    g.new()
    g.run()
    