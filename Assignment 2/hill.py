import copy
import board as b
import time

# store a Random-Restart Hill Climbing Algorithm
class HillClimbing:
    # Initializer will initialize with a board and the number of queens
    def __init__(self, b, n):
        self.board = b
        self.n = n

    # restart function will re-initialize a new board and run the HillClimbingMethod again
    def restart(self) -> object:
        self.board = b.Board(self.n)
        return self.HillClimbingMethod()

    # Run random-restart hill climbing algo
    def HillClimbingMethod(self) -> object:
        if self.board.get_fitness() == 0:
            return self.board


        # if we get a board that doesn't have 0 attacking pairs of queens
        # then we'll start the hill-climbing algorithm
        while self.board.get_fitness() != 0:
            # copy the best board thus far
            best = copy.deepcopy(self.board)
            # boolean if there is a better board config available
            better_board_config = False

            for r in range(self.n):
                # if 1 not in self.board.get_map()[row]:
                #     continue
                # find the queen in the row
                next_c = self.board.get_map()[r].index(1)

                # iterate through columns
                for c in range(self.n):
                    # copy the current board to a temp variable
                    temp = copy.deepcopy(self.board)
                    # move the queen to a different column
                    temp.flip(r, c)
                    temp.flip(r, next_c)
                    # if the board stored in temp has a better fitness (less attacking queens)
                    # Then set the best to temp
                    if temp.get_fitness() < best.get_fitness():
                        best = copy.deepcopy(temp)
                        better_board_config = True
            # If we do not find a better board we are going to re-initialize the board with the
            # restart function
            if not better_board_config:
                return self.restart()
            # else We'll set the board equal to the best board found thus far
            self.board = best

        return self.board  # Return the best board found


# start time
st = time.time()

# number of queens on the board
num_queens = 5

# creatte hill climbing object
hill_climbing_object = HillClimbing(b.Board(num_queens), num_queens)

# run the hill climbing method
s = hill_climbing_object.HillClimbingMethod()

while s is None:
    s = hill_climbing_object.HillClimbingMethod()
    # if s != None:
    #     s.show_map()
    #     break
# calculate the total time and print it out
et = time.time()
total_time = (et - st) * 1000
print(f'This is the total time: {total_time:.2f}ms')
# finally show the map
s.show_map()  # Print the best board


