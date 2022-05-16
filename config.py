from os import path
import random

#colours
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
DARKGREY = (40,40,40)

#Game settings

WIDTH = 1280
HEIGHT = 1024
FPS = 1
TITLE = "Animal Kindom"

#Game inputs
max_hunger_limit = 100
max_thirst_limit = 100

#lion
num_lions = 3
lion_breeding_cooldown = 50000 #Large number = longer time for female lions to be ready for mating 
lion_reproduction_rate = random.randint(1,2) #larger number = higher 
lion_hunger_depletion_rate = random.randint(1,2) #larger number = higher 
lion_thirst_rate = random.randint(1,2) #larger number = higher 

#wolf
num_wolves = 4
wolf_breeding_cooldown = 20000 #Large number = longer time for female wolves to be ready for mating 
wolf_reproduction_rate = random.randint(1,2) #larger number = higher 
wolf_hunger_depletion_rate = random.randint(1,2) #larger number = higher 
wolf_thirst_rate = random.randint(1,2) #larger number = higher 

#rabbit
num_rabbits = 8
rabbit_breeding_cooldown = 10000 #Large number = longer time for female rabbits to be ready for mating 
rabbit_reproduction_rate = random.randint(0,5) #larger number = higher 
rabbit_hunger_depletion_rate = random.randint(1,5) #larger number = higher 
rabbit_thirst_rate = random.randint(1,3) #larger number = higher 

map =[]
with open(path.join('map.txt'),'r') as file:
    for line in file:
        map.append(line.strip())
    file.close()

NO_OF_BLOCKS_WIDE = len(map[0]) 
NO_OF_BLOCKS_HIGH = len(map) 
GRIDWIDTH = round(WIDTH/NO_OF_BLOCKS_WIDE) 
GRIDHEIGHT = round(HEIGHT/NO_OF_BLOCKS_HIGH)
