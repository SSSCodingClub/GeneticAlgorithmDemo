import pygame
from random import random, choices
from math import hypot


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
STEPS_PER_GENERATION = 2000

class Rocket:
    acceleration_rate = 0.005
    radius = 10

    def __init__(self, dna = None):
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT)
        self.velocity = pygame.Vector2()

        if dna is None:
            self.dna = []
            for i in range(STEPS_PER_GENERATION):
                self.dna.append(pygame.Vector2(random() * 2 - 1, random() * 2 - 1))
                self.dna[i].scale_to_length(self.acceleration_rate)
        else:
            self.dna = dna

    def update(self, step):
        self.position += self.velocity

        self.velocity += self.dna[step]

    def show(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, 10)

class Population:
    population_size = 100
    max_acceptable_distance = SCREEN_HEIGHT
    
    def __init__(self):
        self.rockets = [Rocket() for _ in range(self.population_size)]
        self.step = 0
        self.mutation_rate = 0.0005
        
    def show(self, screen):
        for rocket in self.rockets:
            rocket.show(screen)

    def update(self, target):
        for rocket in self.rockets:
            rocket.update(self.step)
        
        self.step += 1

        if self.step == STEPS_PER_GENERATION:
            self.step = 0
            self.get_next_generation(target)

    def get_next_generation(self, target):

        # Calculate fitnesses
        fitnesses = []
        best_fitness = 0
        for rocket in self.rockets:
            f = max(0.01, self.max_acceptable_distance - hypot(rocket.position.x - target.x, rocket.position.y - target.y))
            best_fitness = max(best_fitness, f)
            fitnesses.append(f)

        print(f"Best fitness: {best_fitness}")
        
        # Choose parents based on fitnesses
        parentsA = choices(self.rockets, fitnesses, k = self.population_size)
        parentsB = choices(self.rockets, fitnesses, k = self.population_size)
        
        # Get the children of the chosen parents
        children = []

        for i in range(self.population_size):
            children.append(self.get_child(parentsA[i], parentsB[i]))

        self.rockets = children

    def get_child(self, parentA, parentB):
        '''
        Ex: parentA = [1, 2, 3]
            parentB = [4, 5, 6]
            child =   [1, 5, 3]
        '''

        new_dna = []
        for i in range(STEPS_PER_GENERATION):
            if random() < 0.5:
                new_dna.append(parentA.dna[i])
            else:
                new_dna.append(parentB.dna[i])

            if random() < self.mutation_rate:
                new_dna[i] = pygame.Vector2(random() * 2 - 1, random() * 2 - 1)
                new_dna[i].scale_to_length(Rocket.acceleration_rate)

        return Rocket(dna = new_dna)
        

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

population = Population()

is_running = True

target = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

while is_running:
    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, (255, 0, 0), target, 10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    population.update(target)
    population.show(screen)

    pygame.display.update()

pygame.quit()