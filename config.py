from os import path

#colours
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
DARKGREY = (40,40,40)

#Game settings

WIDTH = 900
HEIGHT = 700
FPS = 1
TITLE = "Animal Kindom"

#Game inputs
max_hunger_limit = 30
max_thirst_limit = 40

map =[]
with open(path.join('map.txt'),'r') as file:
    for line in file:
        map.append(line.strip())
    file.close()

NO_OF_BLOCKS_WIDE = len(map[0])
NO_OF_BLOCKS_HIGH = len(map)
GRIDWIDTH = round(WIDTH/NO_OF_BLOCKS_WIDE)
GRIDHEIGHT = round(HEIGHT/NO_OF_BLOCKS_HIGH)
