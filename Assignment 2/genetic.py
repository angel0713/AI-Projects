"""
Author: Angel Mendez
Professor: Kate Nguyen
Class: CECS 451-Artificial Intelligence
Project: Assignment2 - Genetic Algorithm & Hill-Climbing Algorithm
"""
import random
import time
from board import Board


# class will contain an initializer
# and the required functions stated by the project specifications
class Genetic:
    # constructor will initialize a number of states
    # and a number of queens (n)
    def __init__(self, n, states):
        # store states in a list
        self.boards = []
        # append a number of boards to the population list
        for x in range(states):
            self.boards.append(Board(n))
        # set the number of queens for future use
        self.n = n

    # need selection implementation according to project req.
    # return the first and second board (should be sorted so they have the best fitnesses)
    def Selection(self):
        # sort the list of states using the built in .sort function
        # sort them based on their fitness levels
        self.boards.sort(key=lambda x: x.get_fitness())
        # return the best boards with the best fitness levesls
        return self.boards[0], self.boards[1]

    # Here we are going to send in two parent boards
    # Then we'll select a random column
    def Crossover(self, p1, p2):
        # pick a column (we'll choose 1)
        num = 1

        # get location of queen on this row
        p1_queen = p1.get_map()[num].index(1)
        p2_queen = p2.get_map()[num].index(1)
        # to increase randomness of where the queen lands in parent1
        p1.flip(num, p1_queen)
        p1.flip(num, p2_queen)
        # return parent1 board
        return p1

    def Mutation(self, board):
        # if a random_int is <= a certain probability
        # then a mutation will occur (usually the more mutations the faster the output)
        if random.randint(1, 100) < 20:
            # get random row
            row = random.randint(0, self.n - 1)
            # find a queen
            find_queen = board.get_map()[row].index(1)
            # then flip the board
            board.flip(row, find_queen)
            # find another queen to help mutate and flip the board
            find_new_queen = random.randint(0, self.n - 1)
            board.flip(row, find_new_queen)
        return board

    def GeneticMethod(self):
        for x in range(10_000):
            # if no attacking queens then return the solution
            if self.boards[0].get_fitness() == 0:
                solution = self.boards[0]
                return solution
            # parent1 = population[0]
            # parent2 = population[1]
            parent1, parent2 = self.Selection()
            # create a child with genetics from both parents
            child = self.Crossover(parent1, parent2)
            # mutate the child board
            child = self.Mutation(child)
            # replace the last board in the list
            self.boards[self.n - 1] = child
        # if no solution found then return None
        return None


st = time.time()
num_queens = 5  # number of queens
states = 8  # number of states
genetic = Genetic(num_queens, states)

result = genetic.GeneticMethod()
# if we find a result then calculate the total time and show the map of the solution board
# otherwise print out no solution
if result is not None:
    et = time.time()
    final_time = (et - st) * 1000
    print(f"Running Time: {final_time:.2f}ms")
    result.show_map()
else:
    print("Solution not found within required iterations")
