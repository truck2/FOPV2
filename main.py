from xml.sax.handler import property_declaration_handler
import pygame 
import sys
import random
from os import path
from config import *
from sprites import *
import math
from copy import deepcopy

#stores the x and y cordinates of preloaded terrain
valid_spawning_area = []
water_sources = []

num_lions = 3
lion_location = ()
num_wolves = 5
wolf_location = ()
num_rabbits = 10
rabbit_location = []
num_deers = 7
deer_location = ()


def distance(startX,startY,endX,endY):
    res = math.sqrt(((endX-startX)**2) + ((endY-startY)**2))
    return res

def chase(animal,prey):
    animal_location = animal.getlocation()
    if animal_location[0] < prey.x:
        animal.move(1,0)
    elif animal_location[0] > prey.x:
        animal.move(-1,0)
    if animal_location[1] < prey.y:
        animal.move(0,1)
    elif animal_location[1] > prey.y:
        animal.move(0,-1)

def look_for_nearst_water(animal):
    locations = water_sources[:]
    animal_location = animal.getlocation()
    locations.append(animal_location)
    locations.sort()
    for loc in locations:
        if loc == animal_location:
            d1=0;d2=0
            index1 = locations.index(loc) + 1
            index2 = locations.index(loc) - 1 
            if index1>=0 and index1 <len(locations): 
                d1 = distance(locations[index1][0],locations[index1][1],animal_location[0],animal_location[1])
            if index2>=0 and index2 - 1 <len(locations):
                d2 = distance(locations[index2][0],locations[index2][1],animal_location[0],animal_location[1])

            if d1>d2:
                watloc = locations[index1]
            else:
                watloc = locations[index2]
                    
            if animal.closest_water == ():
                animal.closest_water = deepcopy(watloc)
                break
                    
            #now move towards closest water_source
            if animal_location[0] < animal.closest_water[0]:
                animal.move(1,0)
            elif animal_location[0] > animal.closest_water[0]:
                animal.move(-1,0)
            if animal_location[1] < animal.closest_water[1]:
                animal.move(0,1)
            elif animal_location[1] > animal.closest_water[1]:
                animal.move(0,-1)

            neigbors = animal.get_neighbors()
            for i in neigbors:
                if i in water_sources:
                    animal.drink()
                    print(str(animal.name)+ "drank water")

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
        self.lion_group = pygame.sprite.Group()
        self.lion_baby = pygame.sprite.Group()
        self.wolf_group = pygame.sprite.Group()
        self.deer_group = pygame.sprite.Group()
        self.rabbit_group = pygame.sprite.Group()

        #generate input map 
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == 'm':
                    Mountain(self,col,row)
                if tile == 'b':
                    Boundary(self,col,row)
                if tile == 'w':
                    Water(self,col,row)
                    water_sources.append((col,row))
                if tile =='.':
                    Grass(self,col,row)
                    valid_spawning_area.append((col,row))
                    
        #generate random spawning lions
        for i in range(num_lions):
            randxy = [random.choice(valid_spawning_area)]
            self.lion = Lion(self,randxy[0][0],randxy[0][1])
            self.lion_group.add(self.lion)
            

        #generate random spawning wolves
        for i in range(num_wolves):
            randxy = [random.choice(valid_spawning_area)]
            self.wolf = Wolf(self,randxy[0][0],randxy[0][1])
            self.wolf_group.add(self.wolf)
            

        #generate random spawning rabbits
        for i in range(num_rabbits):
            randxy = [random.choice(valid_spawning_area)]
            self.rabbit = Rabbit(self,randxy[0][0],randxy[0][1])
            self.rabbit_group.add(self.rabbit)
           

        #generate random spawning deer
        for i in range(num_deers):
            randxy = [random.choice(valid_spawning_area)]
            self.deer = Deer(self,randxy[0][0],randxy[0][1])
            self.deer_group.add(self.deer)
           
        
            
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
         #random wolf movement   
        for wolf in self.wolf_group:
            x = random.randint(-1,1); y= random.randint(-1,1)
            wolf.move(x,y)
            
    #random rabbit movement
        for rabbit in self.rabbit_group:
            x = random.randint(-1,1); y= random.randint(-1,1)
            rabbit.move(x,y)

    #random deer movement
        for deer in self.deer_group:
            x = random.randint(-1,1); y= random.randint(-1,1)
            deer.move(x,y)


        for lion in self.lion_group:
            #calculate the closest watersource for each lion
            prey = ()
            prey_rabbit = pygame.math.Vector2()
            prey_deer = pygame.math.Vector2()
            prey_wolf = pygame.math.Vector2()
            lion.thirst_limit -= random.randint(1,2)
            lion.hunger_limit -= random.randint(1,2)
            #lion.reproduction_level -= random.randint(1,20)
            partner = pygame.math.Vector2()
            if lion.thirst_limit <=0: #if lion is thirst then we look for the nearst water.
                print(str(lion.name) + " is Thirsty")
                look_for_nearst_water(lion)

            if lion.hunger_limit <=0:
                lion.hungry = True
                print(str(lion.name) + " is Hungry")
                pos = pygame.math.Vector2(lion.x, lion.y)
                if self.rabbit_group:
                    prey_rabbit = min([e for e in self.rabbit_group], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
                if self.deer_group:
                    prey_deer = min([e for e in self.deer_group], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
                if self.wolf_group:
                    prey_wolf = min([e for e in self.wolf_group], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))

                dist_to_rab = distance(prey_rabbit.x,prey_rabbit.y,lion.getlocation()[0],lion.getlocation()[1])
                dist_to_deer = distance(prey_deer.x,prey_deer.y,lion.getlocation()[0],lion.getlocation()[1])
                dist_to_wolf = distance(prey_wolf.x,prey_wolf.y,lion.getlocation()[0],lion.getlocation()[1])
                if dist_to_rab < dist_to_wolf and dist_to_rab < dist_to_deer:
                    prey = prey_rabbit
                elif dist_to_deer < dist_to_wolf and dist_to_deer < dist_to_rab:
                    prey = prey_deer
                else:
                    prey = prey_wolf
                
                chase(lion,prey)

                lion_neighbors = lion.get_neighbors()
                for i in lion_neighbors:
                    if i == (prey.x,prey.y):
                        prey.kill()
                        lion.ate()

            if lion.reproduction_level == 100 and lion.can_breed ==True: #Find nearst opposite gender
                print(str(lion.name) + str(lion.gender) +" is ready to mate")
                pos = pygame.math.Vector2(lion.x, lion.y)
                if lion.gender == 'm':
                    partner = min([e for e in self.lion_group if e is not lion and e.gender =='f'], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
                else:
                    partner = min([e for e in self.lion_group if e is not lion and e.gender =='m'], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
                chase(lion,partner)

                lion_neighbors = lion.get_neighbors()
                for i in lion_neighbors:
                    if i == (partner.x,partner.y):
                        lion.reproduce()
                        randxy = [random.randint(-1,1)]
                        if not lion.collide_with_entity(randxy[0],randxy[1]):
                            if random.randint(0,5) == 4: #25% chance of producing a baby
                                lion.baby = Lion(self,partner.x+randxy[0],partner.y+randxy[1])
                                self.lion_baby.append(lion.baby)
                                lion.breeding ==True
                                lion.can_breed = False
                        
            else:# move randomly
                x = random.randint(-1,1); y= random.randint(-1,1)
                lion.move(x,y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing =False
                pygame.quit()
                sys.exit()
            
            
g = Game()
while True:
    g.new()
    g.run()
    