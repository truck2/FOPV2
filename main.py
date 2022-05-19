import pygame
import pygame.freetype 
import sys
import random
from os import path
from config import *
from sprites import *
import math
from copy import deepcopy
from datetime import datetime
import logging
import matplotlib.pyplot as plt


# datetime object containing current date and time
today = datetime.now()
f_today = str(today).replace(" ","").replace(".","").replace("-","").replace(":","")

#stores the x and y cordinates of preloaded terrain
valid_spawning_area = []
water_sources = []

#From mgmalheiros on Stackoverflow
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()
logger.addHandler(logging.FileHandler(path.join('Logs','simulation'+str(f_today)+'.log'), 'a'))
print = logger.info


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

def run_away(animal, predator):
    animal_location = animal.getlocation()
    if animal_location[0] < predator.x:
        animal.move(-1,0)
    elif animal_location[0] > predator.x:
        animal.move(1,0)
    if animal_location[1] < predator.y:
        animal.move(0,-1)
    elif animal_location[1] > predator.y:
        animal.move(0,1)

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

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.DOUBLEBUF)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()
        self.time = 0
        self.playing = True
        self.data = [["Inputs","Simulation Time: "+str(simulation_time),"Lions: "+str(num_lions),"Wolves: "+str(num_wolves),"Rabbits: "+str(num_rabbits),"distance of interaction: "+str(distance_of_interation),"Grass grow time(ticks): "+str(grass_grow_time)],
                     [" ","life span: ",str(lion_death_timer),str(wolf_death_timer),str(rabbit_death_timer)],
                     [" ","Breeding Cooldown",str(lion_breeding_cooldown),str(wolf_breeding_cooldown),str(rabbit_breeding_cooldown)],
                     [" "," Mating Threshold",str(lion_mating_threshold),str(wolf_mating_threshold),str(rabbit_mating_threshold)],
                     [" ","Hunger Threshold",str(lion_hunger_threshold),str(wolf_hunger_threshold),str(rabbit_hunger_threshold)],
                     [" ","Thirst Threshold",str(lion_thirst_threshold),str(wolf_thirst_threshold),str(rabbit_thirst_threshold)],
                     ["Iterations","Number of Lions","Number of Wolves","Number of Rabbits"]]

    def load_data(self):
        self.map_data =[]
        game_folder = path.dirname(__file__)
        with open(path.join(game_folder,'map.txt'),'r') as file:
            for line in file:
                self.map_data.append(line.strip())
        file.close()

    def new(self):
        self.all_sprites =pygame.sprite.LayeredUpdates()
        self.water = pygame.sprite.Group()
        self.boundary = pygame.sprite.Group()
        self.mountain = pygame.sprite.Group()
        self.grass_group = pygame.sprite.Group()
        self.lion_group = pygame.sprite.Group()
        self.wolf_group = pygame.sprite.Group()
        self.rabbit_group = pygame.sprite.Group()
        self.soil_group = pygame.sprite.Group()

        #generate input map 
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == 'm':
                   mount = Mountain(self,col,row)
                   self.mountain.add(mount)
                if tile == 'b':
                    bound = Boundary(self,col,row)
                    self.boundary.add(bound)
                if tile == 'w':
                    w = Water(self,col,row)
                    water_sources.append((col,row))
                    self.water.add(w)
                if tile =='.':
                    self.grass =Grass(self,col,row)
                    self.grass_group.add(self.grass)
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

    def write_file(self,name,data):
        game_folder = path.dirname(__file__) 
        with open(path.join(game_folder,'simulations',str(name)+str(f_today))+".csv",'x') as file:
            for lines in data:
                l = ",".join(lines)
                file.writelines(l+"\n")
        file.close()
    
    def graph_data(self,name):

        game_folder = path.dirname(__file__)
        iterations = [i for i in range(simulation_time)]
        data = []
        lion_population = []
        wolf_population = []
        rabbit_population = []
        with open(path.join(game_folder,'simulations',str(name)+str(f_today))+".csv",'r') as file:
            for line in file:
                string = line.split(',')
                data.append(string)
        file.close()

        for line in data[7:]:
            lion_population.append(float(line[1].strip()))
            wolf_population.append(float(line[2].strip()))
            rabbit_population.append(float(line[3].strip()))
        
        plt.figure("Population against Time")
    
        plt.subplot(311)
        plt.plot(iterations, lion_population,'r',label ="Lion")
        plt.xlabel('Iterations')
        plt.ylabel('Population')
        plt.legend()

        plt.subplot(312)
        plt.plot(iterations,wolf_population,'b',label ="Wolf")
        plt.xlabel('Iterations')
        plt.ylabel('Population')
        plt.legend()

        plt.subplot(313)
        plt.plot(iterations,rabbit_population,label ="Rabbit")
        plt.xlabel('Iterations')
        plt.ylabel('Population')
        plt.legend()
        
        plt.savefig(path.join(game_folder,'plot_figures',str(name)+str(f_today)))
        plt.show()

    def run(self):
        while self.playing:
            self.time +=1
            self.dt = self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            self.data.append([str(self.time),str(len(self.lion_group)),str(len(self.wolf_group)),str(len(self.rabbit_group))]) 
            if self.time == simulation_time:
                self.write_file("simulation",self.data)
                pygame.image.save(self.screen,"plot_state_images/plot"+str(f_today)+".jpg")
                self.playing = False
                self.graph_data("simulation")
                pygame.quit()
                sys.exit()



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
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        self.font = pygame.font.SysFont("sans",50)
        self.text = self.font.render( "Time Left: "+str(simulation_time-self.time)+"  "+"nLions: "+ str(len(self.lion_group))+ "  "+"nWolves: "+str(len(self.wolf_group))+ "  "+ "nRabbits: "+str(len(self.rabbit_group)),True, RED)
        self.screen.blit(self.text,[0,0])
        pygame.display.flip()

    

    def events(self):

       #---------------------------------------------------------#Wolf Movement ---------------------------------------------------------------------------------------------------------------------------#
        for wolf in self.wolf_group:
            partner = pygame.math.Vector2()
            predator_lion = pygame.math.Vector2()
            prey_rabbit = pygame.math.Vector2()
            pos = pygame.math.Vector2()
            wolf_offspring = pygame.sprite.Sprite()
            wolf.thirst_limit -= wolf_thirst_rate
            wolf.hunger_limit -= wolf_hunger_depletion_rate
            wolf.reproduction_level -= wolf_reproduction_rate 
            wolf_offspring = pygame.sprite.Sprite()

            wolf.life_time +=1
            if wolf.life_time == wolf_death_timer or wolf.hunger_limit <=0 or wolf.thirst_limit <=0:
                wolf.kill()
                print("Wolf " + str(wolf.name) + str(wolf.gender)+ " Died of Old Age")

            #runaway from lions are close by
            if self.lion_group:
                pos = pygame.math.Vector2(wolf.x, wolf.y)
                predator_lion = min([e for e in self.lion_group], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
                if pos.distance_to(pygame.math.Vector2(predator_lion.x, predator_lion.y)) <= distance_of_interation:
                    run_away(wolf,predator_lion)
                    print("Wolf " +str(wolf.name) + str(wolf.gender)+ " is running away from: "+ "Lion" + str(predator_lion.name))

            if self.rabbit_group:
                pos = pygame.math.Vector2(wolf.x, wolf.y)
                prey_rabbit = min([e for e in self.rabbit_group], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
                wolf_neighbors = wolf.get_neighbors()
                for i in wolf_neighbors:
                    if i == (prey_rabbit.x,prey_rabbit.y) and wolf.hunger_limit<95:
                        prey_rabbit.kill()
                        wolf.ate()
                        print("Wolf " +str(wolf.name) + str(wolf.gender)+ " ate!")

            #if wolves are hungry
            if wolf.hunger_limit <= wolf_hunger_threshold:
                print("Wolf " +str(wolf.name) + " is Hungry")
                pos = pygame.math.Vector2(wolf.x, wolf.y)
                if self.rabbit_group:
                    prey_rabbit = min([e for e in self.rabbit_group], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
                
                if prey_rabbit:
                    chase(wolf,prey_rabbit)
                    print("Wolf " +str(wolf.name) + str(wolf.gender)+ " is chasing: "+ str(prey_rabbit.name)+str(prey_rabbit.gender))
            
                    wolf_neighbors = wolf.get_neighbors()
                    for i in wolf_neighbors:
                        if i == (prey_rabbit.x,prey_rabbit.y):
                            prey_rabbit.kill()
                            wolf.ate()
                            print("Wolf " +str(wolf.name) + str(wolf.gender)+ " ate!")
                elif not prey_rabbit or wolf.hunger_limit<=0:
                    wolf.kill()
                    print("Wolf"+ str(wolf.name)+ str(wolf.gender)+ " died of hunger")

            #if wolves are thristy.
            if wolf.thirst_limit <= wolf_thirst_threshold: #if lion is thirst then we look for the nearst water.
                print("Wolf " +str(wolf.name) + " is Thirsty")
                look_for_nearst_water(wolf)
                print("Wolf " + str(wolf.name)+ "drank water")
    
            now = pygame.time.get_ticks()
            breeding_cooldown = wolf.breedingCooldown
            #print(str(wolf.name)+ " " + str(now) +" "+ str(wolf.time) +" "+ str(breeding_cooldown)+" "+ str(wolf.can_breed))
            if now-wolf.time >= int(breeding_cooldown):
                wolf.can_breed = True
                wolf.mated = False

            pos = pygame.math.Vector2(wolf.x, wolf.y)
          
            if wolf.reproduction_level <=wolf_mating_threshold and wolf.can_breed ==True and wolf.mated == False: #Find nearst opposite gender
                print("Wolf " +str(wolf.name) +" "+ str(wolf.gender) +" is ready to mate")

                try:
                    if wolf.gender == 'm':
                        partner = min([e for e in self.wolf_group if e is not wolf and e.gender =='f' and e.mated==False and e.can_breed==True], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
                except ValueError:
                        print("No Female Wolf Partner or Female Wolf Partner not ready yet!")
                        continue

                if partner:  
            
                    chase(wolf,partner)

                    wolf_neighbors = wolf.get_neighbors()
                    for i in wolf_neighbors:
                        if i == (partner.x,partner.y):
                            randx = random.randint(-1,1); randy= random.randint(-1,1)
                            if not partner.collide_with_entity(randx,randy) and (partner.x+randx,partner.y+randy) in valid_spawning_area:
                                wolf_offspring = Wolf(self,partner.x+randx,partner.y+randy)
                                wolf_offspring.reproduce()
                                partner.reproduce()
                                wolf.time = pygame.time.get_ticks()
                                partner.time = pygame.time.get_ticks()
                                print("Wolf " + str(wolf_offspring.name) + " "+str(wolf_offspring.gender) + " was born!" + " Father is " + str(wolf.name) +" and "+"Mother is " + str(partner.name))
                                self.wolf_group.add(wolf_offspring)

                        #if stuck by a water source
                        for water in self.water:
                            if i == water.getlocation():
                                x = random.randint(-1,1); y= random.randint(-1,1)
                                wolf.move(x,y)

                        #if stuck by a moutain
                        for mount in self.mountain:
                            if i == mount.getlocation():
                                x = random.randint(-1,1); y= random.randint(-1,1)
                                wolf.move(x,y)

                        for bound in self.boundary:
                            if i == bound.getlocation():
                                x = random.randint(-1,1); y= random.randint(-1,1)
                                wolf.move(x,y)
                else: 
                    x = random.randint(-1,1); y= random.randint(-1,1)
                    wolf.move(x,y)

            else: #random movement
                x = random.randint(-1,1); y= random.randint(-1,1)
                wolf.move(x,y)



        #---------------------------------------------------------#Rabbit Movement ---------------------------------------------------------------------------------------------------------------------------#

        for rabbit in self.rabbit_group:
            partner = pygame.math.Vector2()
            prey = ()
            grass_cooldown = 0
            grass_time = 0
            rabbit.thirst_limit -= rabbit_thirst_rate
            rabbit.hunger_limit -= rabbit_hunger_depletion_rate
            rabbit.reproduction_level -= rabbit_reproduction_rate
            rabbit_offspring = pygame.sprite.Sprite()

            rabbit.life_time +=1
            if rabbit.life_time == rabbit_death_timer or rabbit.hunger_limit <=0 or rabbit.thirst_limit <=0:
                rabbit.kill()
                print("rabbit " + str(rabbit.name) + str(rabbit.gender)+ " Died of Old Age")
                

            if rabbit.thirst_limit <= rabbit_thirst_threshold:
                print("Rabbit " +str(rabbit.name) + " is Thirsty")
                look_for_nearst_water(rabbit)
                print("Rabbit " + str(rabbit.name)+ " drank water")
                
            #run away from predators, if they are nearby
            if self.lion_group:
                pos = pygame.math.Vector2(rabbit.x, rabbit.y)
                predator_lion = min([e for e in self.lion_group], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
                if pos.distance_to(pygame.math.Vector2(predator_lion.x, predator_lion.y)) <= distance_of_interation:
                    run_away(rabbit,predator_lion)
                    print("Rabbit "+ str(rabbit.name)+ str(rabbit.gender)+ " is running away from: " +"Lion"+ str(predator_lion.name))

            if self.wolf_group:
                pos = pygame.math.Vector2(rabbit.x, rabbit.y)
                predator_wolf = min([e for e in self.wolf_group], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
                if pos.distance_to(pygame.math.Vector2(predator_wolf.x, predator_wolf.y)) <= distance_of_interation:
                    run_away(rabbit,predator_wolf)
                    print("Rabbit "+ str(rabbit.name)+ str(rabbit.gender)+ " is running away from: " +"Wolf"+ str(predator_wolf.name)) 

            if rabbit.hunger_limit <= rabbit_hunger_threshold:
                print("Rabbit " +str(rabbit.name) + " is Hungry")

                if not self.grass_group  or rabbit.hunger_limit<=0:
                    rabbit.kill()
                    print("Rabbit"+str(rabbit.name)+str(rabbit.gender)+ " died of hunger")

                for grass in self.grass_group:
                    grass_cooldown = grass.cooldown
                    if grass.getlocation() == rabbit.getlocation():
                        grass.time = pygame.time.get_ticks()
                        grass_time = grass.time
                        grassLoc = grass.getlocation()
                        grass.kill()
                        self.soil = Soil(self,grassLoc[0],grassLoc[1])
                        self.soil_group.add(self.soil)
                        rabbit.ate()
                        print("Rabbit "+str(rabbit.name)+str(rabbit.gender) + " ate")
                      
                    grass_now = pygame.time.get_ticks()
                    if grass_now-grass_time>=int(grass_cooldown):
                        for soil in self.soil_group:
                            soil_loc = soil.getlocation()
                            soil.kill()
                            self.grass = Grass(self,soil_loc[0],soil_loc[1])
                            self.grass_group.add(self.grass)

            now = pygame.time.get_ticks()
            breeding_cooldown = rabbit.breedingCooldown
            if now-rabbit.time >= int(breeding_cooldown):
                rabbit.can_breed = True
                rabbit.mated = False

            
            if rabbit.reproduction_level <= rabbit_mating_threshold and rabbit.can_breed ==True and rabbit.mated == False: #Find nearst opposite gender
                print("Rabbit " +str(rabbit.name) +" "+ str(rabbit.gender) +" is ready to mate")

                pos = pygame.math.Vector2(rabbit.x, rabbit.y)
                try:
                    if rabbit.gender == 'm': #locate nearst female 
                        partner = min([e for e in self.rabbit_group if e is not rabbit and e.gender =='f' and e.mated == False and e.can_breed ==True], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
                except ValueError:
                    print("Not enough female Rabbits or Female Rabbit partners are not ready yet!")
                    continue

                if partner:
                    chase(rabbit,partner)
                    print("Rabbit " +str(rabbit.name) +" "+ str(rabbit.gender) +" is approaching partner: "+"Rabbit " +str(partner.name)+str(partner.gender))
                    rabbit_neighbors = rabbit.get_neighbors()
                    for i in rabbit_neighbors:
                        if i == (partner.x,partner.y):
                            randx = random.randint(-1,1); randy= random.randint(-1,1)
                            if not partner.collide_with_entity(randx,randy) and (partner.x+randx,partner.y+randy) in valid_spawning_area:
                                rabbit_offspring = Rabbit(self,partner.x+randx,partner.y+randy)
                                rabbit_offspring.reproduce()
                                partner.reproduce()
                                rabbit.time = pygame.time.get_ticks()
                                partner.time = pygame.time.get_ticks()
                                print("Rabbit " + str(rabbit_offspring.name) + " "+str(rabbit_offspring.gender) + " was born!" + "Father is " + str(rabbit.name) +" and "+"Mother is " + str(partner.name))
                                self.rabbit_group.add(rabbit_offspring)
                        
                        #if stuck by a water source
                        for water in self.water:
                            if i == water.getlocation():
                                x = random.randint(-1,1); y= random.randint(-1,1)
                                rabbit.move(x,y)
                        #if stuck by a moutain
                        for mount in self.mountain:
                            if i == mount.getlocation():
                                x = random.randint(-1,1); y= random.randint(-1,1)
                                rabbit.move(x,y)
                        for bound in self.boundary:
                            if i == bound.getlocation():
                                x = random.randint(-1,1); y= random.randint(-1,1)
                                rabbit.move(x,y)
                else: 
                    x = random.randint(-1,1); y= random.randint(-1,1)
                    rabbit.move(x,y)


            else:# move randomly
                x = random.randint(-1,1); y= random.randint(-1,1)
                rabbit.move(x,y)




        #---------------------------------------------------------#Lion Movement ---------------------------------------------------------------------------------------------------------------------------#
        for lion in self.lion_group:
            partner = pygame.math.Vector2()
            prey = ()
            prey_rabbit = pygame.math.Vector2()
            prey_wolf = pygame.math.Vector2()
            lion.thirst_limit -= lion_thirst_rate
            lion.hunger_limit -= lion_hunger_depletion_rate
            lion.reproduction_level -= lion_reproduction_rate
            
            lion.life_time +=1
            if lion.life_time == lion_death_timer or lion.hunger_limit<=0 or lion.thirst_limit<=0:
                lion.kill()
                print("Lion " + str(lion.name) + str(lion.gender)+ " Died of Old Age")

            lion_offspring = pygame.sprite.Sprite()
            if lion.thirst_limit <=lion_thirst_threshold: #if lion is thirst then we look for the nearst water.
                print("Lion " +str(lion.name) + " is Thirsty")
                look_for_nearst_water(lion)
                print("Lion " + str(lion.name)+ " drank water")
            
            if self.rabbit_group:
                pos = pygame.math.Vector2(lion.x, lion.y)
                prey_rabbit = min([e for e in self.rabbit_group], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
                lion_neighbors = lion.get_neighbors()
                for i in lion_neighbors:
                    if i == (prey_rabbit.x,prey_rabbit.y) and lion.hunger_limit<95:  
                        prey_rabbit.kill
                        lion.ate()
                        print("Lion "+str(lion.name)+str(lion.gender)+ " ate: "+str(prey_rabbit.name)+str(prey_rabbit.gender))
                    else:
                            continue
                
            if self.wolf_group:
                pos = pygame.math.Vector2(lion.x, lion.y)
                prey_wolf = min([e for e in self.wolf_group], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
                lion_neighbors = lion.get_neighbors()
                for i in lion_neighbors:
                    if i == (prey_wolf.x,prey_wolf.y) and lion.hunger_limit<95:  
                        prey_wolf.kill
                        lion.ate()
                        print("Lion "+str(lion.name)+str(lion.gender)+ " ate: "+str(prey_wolf.name)+str(prey_wolf.gender))
                    else:
                        continue

            #start chasing prey if hungry
            if lion.hunger_limit <=lion_hunger_threshold: 
                print("Lion " +str(lion.name) + " is Hungry")
                pos = pygame.math.Vector2(lion.x, lion.y)

                if self.rabbit_group:
                    prey_rabbit = min([e for e in self.rabbit_group], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
                if self.wolf_group:
                    prey_wolf = min([e for e in self.wolf_group], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
                
                dist_to_rab = distance(prey_rabbit.x,prey_rabbit.y,lion.getlocation()[0],lion.getlocation()[1])
                dist_to_wolf = distance(prey_wolf.x,prey_wolf.y,lion.getlocation()[0],lion.getlocation()[1])
                
                if dist_to_rab < dist_to_wolf:
                    prey = prey_rabbit
                else:
                    prey = prey_wolf
                
                if prey:

                    chase(lion,prey)
                    print("Lion"+str(lion.name)+str(lion.gender)+ "is chasing: "+str(prey.name)+str(prey.gender))

                    lion_neighbors = lion.get_neighbors()
                    for i in lion_neighbors:
                        if i == (prey.x,prey.y):
                            prey.kill()
                            lion.ate()
                            print("Lion"+str(lion.name)+str(lion.gender)+ " ate: "+str(prey.name)+str(prey.gender))
                elif not prey or lion.hunger_limit <=0:
                    lion.kill()
                    print("Lion"+ str(lion.name)+ str(lion.gender)+ " died of hunger")
    
            #cooldown for female partners after mating, males do not have cooldown
            now = pygame.time.get_ticks()
            breeding_cooldown = lion.breedingCooldown
            #print(str(lion.name)+ " " + str(now) +" "+ str(lion.time) +" "+ str(breeding_cooldown)+" "+ str(lion.can_breed) + " " + str(lion.reproduction_level)+ " " + str(lion.mated))
            if now-lion.time >= int(breeding_cooldown):
                lion.can_breed = True
                lion.mated = False


            pos = pygame.math.Vector2(lion.x, lion.y)
           
            if lion.reproduction_level <=80 and lion.can_breed ==True and lion.mated == False: #Find nearst opposite gender
                print("Lion " +str(lion.name) +" "+ str(lion.gender) +" is ready to mate")

                try:
                    if lion.gender == 'm': #locate nearst female 
                        partner = min([e for e in self.lion_group if e is not lion and e.gender =='f' and e.can_breed == True and e.mated == False], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
                except ValueError:
                    print("No Female Lion Partner or Female Lion partners are not ready to mate Yet!")
                    continue

                if partner:
                    chase(lion,partner)

                    lion_neighbors = lion.get_neighbors()
                    for i in lion_neighbors:
                        if i == (partner.x,partner.y):
                            randx = random.randint(-1,1); randy= random.randint(-1,1)
                            if not partner.collide_with_entity(randx,randy) and (partner.x+randx,partner.y+randy) in valid_spawning_area:
                                lion_offspring = Lion(self,partner.x+randx,partner.y+randy)
                                lion_offspring.reproduce()
                                partner.reproduce()
                                lion.time = pygame.time.get_ticks()
                                partner.time = pygame.time.get_ticks()
                                print("Lion " + str(lion_offspring.name) + " "+str(lion_offspring.gender) + " was born!" + "Father is " + str(lion.name) +" and "+"Mother is " + str(partner.name))
                                self.lion_group.add(lion_offspring)
                    
                        #if stuck by a water source
                        for water in self.water:
                            if i == water.getlocation():
                                x = random.randint(-1,1); y= random.randint(-1,1)
                                lion.move(x,y)
                        #if stuck by a moutain
                        for mount in self.mountain:
                            if i == mount.getlocation():
                                x = random.randint(-1,1); y= random.randint(-1,1)
                                lion.move(x,y)
                        #if stuck by boundary
                        for bound in self.boundary:
                            if i == bound.getlocation():
                                x = random.randint(-1,1); y= random.randint(-1,1)
                                lion.move(x,y)
                else: 
                    x = random.randint(-1,1); y= random.randint(-1,1)
                    lion.move(x,y)

            else:# move randomly
                x = random.randint(-1,1); y= random.randint(-1,1)
                lion.move(x,y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing =False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.image.save(self.screen,"plot_state_images/plot"+str(f_today)+".jpg")
                
            
            
g = Game()
while True:
    g.new()
    g.run()
    