"""

alife_D_reproduction.py: An animated Artificial Life Simulation

Rabbit reproduction (all rabbits that eat & survive will reproduce)
Rabbits starve if they don't eat in one generation
Grass grows at some rate.

Key concepts:
- Modeling and simulation as a way of understanding complex systems
- Artificial Life: Life as it could be
- Numpy array processing!
- Animation using the matplotlib.animation library

Key life lesson: Let curiosity be your guide.

Need to have (x, y) for each animal instead of list (tuple)

NOTES FROM CLASS:
- rabbits die after 1 generation of not eating
- foxes should have a starvation level of about 50-100 because there aren't enough rabbits around
- hunger level representing how many generations that animal has gone without eating
- starvation level is fixed, hunger level changes
- starvation level for rabbits = 1
- reproduction level = how much you need to eat before you can reproduce
- animals can only reproduce if the amount they have eaten is at least as high as the reproduction level
- add animal-specific offspring level (max number of offspring for each animal)
- red field color for fox is superior -- doesn't matter if theres also grass or rabbits
- need to just use the field for 0s and 1s for grass/no grass
- add rendering for foxes and rabbits
- if two rabbits at same location, only one gets grass
- if two foxes at same location, both get rabbit(s)
- instead of simply setting field value, we need to build overlay for field, rabbits, and foxes
- algorithm for foxes and rabbits at same locaiton:
    - key: coord
    - value; list of rabbits at that location

    rabbits = [(1, 1), (1, 1), (5, 3)]
    transform this into a dictionary:
    (1, 1) --> [r1, r2]
    (5, 3) --> [r3]

    Along comes a fox at position 1, 1
    What rabbits does it eat? (What rabbits die?)
    r1 and r2 are both marked dead
    fox.eated += 2
"""

import random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import copy
# import seaborn   # conda install seaborn


ARRSIZE = 200  # The dimensions of the field
FIGSIZE = 8  # 8 x 8 inch rendering of the field
INIT_RABBITS = 100  # Number of initial rabbits
GRASS_RATE = 0.06   # Probability that grass grows back at any given location in one generation
OFFSPRING = 2 # Max number of offspring
COLOR_MAP = {"nothing" : "black",
            "grass" : "green",
            "rabbit" : "white",
            "fox" : "red"}


class Animal:
    """ Use the Animal object to represent foxes and rabbits (fox = predator, rabbit = prey) """

    def __init__(self, max_offspring=1, starvation_level=1, reproduction_level=1):
        """ Animal constructor """
        self.x = rnd.randrange(0, ARRSIZE)
        self.y = rnd.randrange(0, ARRSIZE)
        self.eaten = 0 # represents how much the animal ate)
        self.max_offspring = max_offspring
        self.starvation_level = starvation_level
        self.reproduction_level = reproduction_level
        self.hunger = 0
        self.alive = True

    def reproduce(self):
        """ Make a new rabbit at the same location.
         Reproduction is hard work! Each reproducing
         rabbit's eaten level is reset to zero. """
        self.eaten = 0
        return copy.deepcopy(self)

    def eat(self, amount):
        """ Feed the rabbit some grass """
        self.eaten += amount

    def move(self):
        """ Move up, down, left, right randomly """
        self.x = (self.x + rnd.choice([-1, 0, 1])) % ARRSIZE  # 0 <= x <= (ARRSIZE-1)
        self.y = (self.y + rnd.choice([-1, 0, 1])) % ARRSIZE  # 0 <= y <= (ARRSIZE-1)
        self.eaten = 0


class Field:
    """ A field is a patch of grass with 0 or more rabbits hopping around
    in search of grass """

    def __init__(self):
        """ Create a patch of grass with dimensions SIZE x SIZE
        and initially no rabbits

        In the numpy array: 0=dirt, 1=grass """
        self.field = np.ones(shape=(ARRSIZE, ARRSIZE), dtype=int)
        self.rabbits = []


    def add_rabbit(self, rabbit):
        """ A new rabbit is added to the field """
        self.rabbits.append(rabbit)

    def move(self):
        """ All Rabbits move """
        for r in self.rabbits:
            r.move()

    def eat(self):
        """ All Rabbits eat (if they find grass where they are) """
        for r in self.rabbits:
            r.eat(self.field[r.x, r.y])
            self.field[r.x, r.y] = 0  # The grass being consumed at the rabbits x,y location



    def survive(self):
        """ Rabbits who eat some grass live to eat another day """
        self.rabbits = [r for r in self.rabbits if r.eaten > 0]

    def reproduce(self):
        """ Rabbits reproduce like rabbits. """
        born = []    # A list of all the rabbits that have been born
        for r in self.rabbits:
            for _ in range(rnd.randint(0, OFFSPRING)):
                born.append(r.reproduce())
        self.rabbits += born


    def grow(self):
        """ Grass grows back with some probability """
        growloc = (np.random.rand(ARRSIZE, ARRSIZE) < GRASS_RATE) * 1
        self.field = np.maximum(self.field, growloc)

    def generation(self):
        """ Run one generation of rabbits """
        self.move()   # everybody move
        self.eat()    # everybody eat
        self.survive() # Who lives
        self.reproduce() # All rabbits reproduce up to OFFSPRING baby rabbits
        self.grow()   # The grass grows back (maybe)



def animate(i, field, im):
    field.generation()
    im.set_array(field.field)   # Injecting the field state values into the array
    plt.title(f"Generation: {i}  Nrabbits: {len(field.rabbits)}")
    return im,


def main():

    # Create a field
    field = Field()

    # Then God created rabbits....
    for _ in range(INIT_RABBITS):
        new_rabbit = Rabbit()   # Creating a single rabbit at a random location
        field.add_rabbit(new_rabbit)  # adding the rabbit to the field simulation

    # Animate the world!
    array = np.ones(shape=(ARRSIZE, ARRSIZE))
    fig = plt.figure(figsize=(FIGSIZE, FIGSIZE))
    im = plt.imshow(array, cmap='viridis', interpolation='hamming', vmin=0, vmax=1)
    anim = animation.FuncAnimation(fig, animate, fargs=(field, im), frames=10**100, interval=1)
    plt.show()




if __name__ == '__main__':
    main()