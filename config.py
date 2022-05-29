#Student name: Ben Huang
#Student ID: 21020526

from os import path
import random
import argparse



parser = argparse.ArgumentParser(description='Simulation Input Parameters')
parser.add_argument('map', help='input map',nargs ='?',default = "map.txt" ,type = str)
parser.add_argument('simulation_time', help='Enter the Time Allowed to Run The Simulation',nargs ='?',default = 200,type = int)
parser.add_argument('neighbourhood_option', help='Moore = 1, Von Neumann neighbourhood = 0',nargs = '?',default = 0,type = int )
parser.add_argument('num_lions', help='Enter the Number of Lions to be Spawned',nargs ='?',default = 4,type = int)
parser.add_argument('num_wolves', help='Enter the Number of Wolves to be Spawned',nargs ='?',default = 4,type = int)
parser.add_argument('num_rabbits', help='Enter the Number of Rabbits to be Spawned',nargs ='?',default = 15,type = int)
#optional game settings
parser.add_argument('distance_of_interation', help='How close should predator be before running away- smaller number to closer, larger number = further',nargs ='?',default = 2.00,type = float)
parser.add_argument('grass_grow_time', help='The time takes for grass to regen',nargs ='?',default = 500000,type = int)
#Life span
parser.add_argument('lion_death_timer', help='Life Span of Lion',nargs ='?',default = 100,type = int)
parser.add_argument('wolf_death_timer', help='Life Span of Wolf',nargs ='?',default = 60,type = int)
parser.add_argument('rabbit_death_timer', help='Life Span of Rabbit',nargs ='?',default = 50,type = int)
#Breeding cooldown
parser.add_argument('lion_breeding_cooldown', help='Large number = longer time for female lions to be ready again for mating ',nargs ='?',default = 1000,type = int)
parser.add_argument('wolf_breeding_cooldown', help='Large number = longer time for female Wolves to be ready again for mating ',nargs ='?',default = 600,type = int)
parser.add_argument('rabbit_breeding_cooldown', help='Large number = longer time for female Rabbit to be ready again for mating ',nargs ='?',default = 100,type = int)
#Mating
parser.add_argument('lion_mating_threshold', help='Ready for mating, Higher number = Ready faster',nargs ='?',default = 80,type = int)
parser.add_argument('wolf_mating_threshold', help='ready for mating, higher number = ready faster',nargs ='?',default = 85,type = int)
parser.add_argument('rabbit_mating_threshold', help='ready for mating, higher number = ready faster',nargs ='?',default = 95,type = int)
#Hunger
parser.add_argument('lion_hunger_threshold', help='starts activily seeking for food, smaller number = takes longer to start looking for food',nargs ='?',default = 70,type = int)
parser.add_argument('wolf_hunger_threshold', help='starts activily seeking for food, smaller number = takes longer to start looking for food.',nargs ='?',default = 70,type = int)
parser.add_argument('rabbit_hunger_threshold', help='starts activily seeking for food, smaller number = takes longer to start looking for food.',nargs ='?',default = 80,type = int)
#Hunger
parser.add_argument('lion_hunger_upper_value', help='Higher Value = Can become hungry faster',nargs ='?',default = 10,type = int)
parser.add_argument('wolf_hunger_upper_value', help='Higher Value = Can become hungry faster',nargs ='?',default = 20,type = int)
parser.add_argument('rabbit_hunger_upper_value', help='Higher Value = Can become hungry faster',nargs ='?',default = 30,type = int)
#Thirsy
parser.add_argument('lion_thirst_threshold', help='starts activily seeking for water, smaller number = takes longer to start looking for food',nargs ='?',default = 80,type = int)
parser.add_argument('wolf_thirst_threshold', help='starts activily seeking for water, smaller number = takes longer to start looking for food',nargs ='?',default = 80,type = int)
parser.add_argument('rabbit_thirst_threshold', help='starts activily seeking for water, smaller number = takes longer to start looking for food',nargs ='?',default = 80,type = int)


args = parser.parse_args()

#colours
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
DARKGREY = (40,40,40)

#Game settings

WIDTH = 1280
HEIGHT = 720
FPS = 60
TITLE = "Animal Kindom"
simulation_time = args.simulation_time
distance_of_interation = args.distance_of_interation
neighbourhood_option = args.neighbourhood_option

#Game inputs
max_hunger_limit = 100
max_thirst_limit = 100



#lion
num_lions = args.num_lions
lion_death_timer = args.lion_death_timer
lion_breeding_cooldown = args.lion_breeding_cooldown #Large number = longer time for female lions to be ready for mating 
lion_reproduction_rate = random.randint(1,5) #larger number = higher 
lion_mating_threshold = args.lion_mating_threshold #ready for mating, higher number = ready faster
lion_hunger_depletion_rate = random.randint(1,args.lion_hunger_upper_value) #larger number = higher 
lion_hunger_threshold = args.lion_hunger_threshold  #starts activily seeking for food, smaller = takes longer to start looking for food.
lion_thirst_rate = random.randint(1,2) #larger number = higher 
lion_thirst_threshold = args.lion_thirst_threshold #starts activily seeking for water

#wolf
num_wolves = args.num_wolves
wolf_death_timer = args.wolf_death_timer
wolf_breeding_cooldown = args.wolf_breeding_cooldown #Large number = longer time for female wolves to be ready for mating 
wolf_reproduction_rate = random.randint(1,5) #larger number = higher 
wolf_mating_threshold = args.wolf_mating_threshold #ready for mating, higher number = ready faster
wolf_hunger_depletion_rate = random.randint(1,args.wolf_hunger_upper_value) #larger number = higher 
wolf_hunger_threshold = args.wolf_hunger_threshold #  #starts activily seeking for food
wolf_thirst_rate = random.randint(1,2) #larger number = higher 
wolf_thirst_threshold = args.wolf_thirst_threshold #starts activily seeking for water

#rabbit
num_rabbits = args.num_rabbits
rabbit_death_timer = args.rabbit_death_timer
rabbit_breeding_cooldown = args.rabbit_breeding_cooldown #Large number = longer time for female rabbits to be ready for mating 
rabbit_reproduction_rate = random.randint(1,10) #larger number = higher 
rabbit_mating_threshold = args.rabbit_mating_threshold #ready for mating, higher number = ready faster
rabbit_hunger_depletion_rate = random.randint(5,args.rabbit_hunger_upper_value) #larger number = higher 
rabbit_hunger_threshold = args.rabbit_hunger_threshold  #starts activily seeking for food
rabbit_thirst_threshold = args.rabbit_thirst_threshold #starts activily seeking for water
rabbit_thirst_rate = random.randint(1,3) #larger number = higher 
grass_grow_time = args.grass_grow_time

map =[]
with open(path.join(args.map),'r') as file:
    for line in file:
        map.append(line.strip())
    file.close()

NO_OF_BLOCKS_WIDE = len(map[0]) 
NO_OF_BLOCKS_HIGH = len(map) 

GRIDWIDTH = round(WIDTH/NO_OF_BLOCKS_WIDE) 
GRIDHEIGHT = round(HEIGHT/NO_OF_BLOCKS_HIGH)

