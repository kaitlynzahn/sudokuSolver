"""
References
 1.) https://www.geeksforgeeks.org/sudoku-backtracking-7/
 2.) https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
"""

#From Reference #2
import time
counting = 0

##Iterates through the rows and columns and prints out the sudoku board
def print_board(game_board):
    row_num = 0
    column_num = 0

    # loops through the entire board
    for row in game_board:
        row_num += 1
        string = '|'
        for column in row:
            column_num += 1

            ##If location has a set variable it adds it to the string
            if(type(column) is int):
                string = string + str(column) + '|'

            ##If not it adds 0 to string as a placeholder value
            else:
                string = string + str(0) + '|'

            ##If at right of a 3x3 adds tabs to string
            if(column_num % 3 == 0) and (column_num % 9 != 0):
                string = string + '\t|'

        print(string)

        ##If at the bottom of a 3x3 adds a new line to string
        if(row_num % 3 == 0) and (row_num % 9 != 0):
            print()



##Minimum remaining values
##Finds the location of the variable with the least remaining values
##and returns it to backtracking function
##Location is in the format of [row: int, col: int]
def mrv(board):
    ##Fewest variables set to 10 since there are 9 possible values
    min_value = 10

    ##Saves possible moves for the degree heuristic
    moves = []

    ##Iterates through the game grid and finds variables with the least legal values
    for i in range(9):
        for j in range(9):
            ##Checks if the variable is set, if it's not func continues
            if type(board[i][j]) is not int:
                num_values = len(board[i][j])

                ##if the number of values is less than min: clear moves, set new min, append move
                if num_values < min_value:
                    moves.clear()
                    min_value = num_values
                    moves.append([i,j])

                ##if the number of values is equal to min: append move
                elif num_values == min_value:
                    moves.append([i,j])

    # initialize max value
    max_constraints = 0
    num_constraints = 0

    # loop through all of the potential moves - move is a 2d [row][col] coordinate
    for move in moves:
        # Check given row of the board for empty spaces
        for x in range(9):
            # checks every column for this move's row
            if type(board[move[0]][x]) is not int:
                # increment the number of spaces that it has constraints on
                num_constraints += 1
    
        # Check that col of the board for empty spaces
        for x in range(9):
            # checks every column for this move's row
            if type(board[x][move[1]]) is not int:
                # increment the number of spaces that it has constraints on
                num_constraints += 1
    
        # Check 3x3 box
        startRow = move[0] - (move[0] % 3)
        startCol = move[1] - (move[1] % 3)
        for i in range(3):
            for j in range(3):
                # make sure to not repeat counting row & column boxes
                if type(board[i + startRow][j + startCol]) is not int and i+startRow != move[0] and i+startCol != move[1]:
                    num_constraints += 1

        # now we have the total number of constraints for this move
        if(num_constraints > max_constraints):
            moves.clear()
            max_constraints = num_constraints
            moves.append([i,j])

    # prints the first five steps as required in report
    # global counting
    # if counting < 5:
    #     print("MOVE")
    #     print(move)
    #     print("DOMAIN")
    #     print(min_value)
    #     print("DEGREE VALUE")
    #     print(num_constraints)
    #     counting += 1

    return move



##Back tracking algorthem
##Modified version of the solveSuduko() function from Reference #1
def back_tracking(board, calls = 0):
    finished = True
    calls += 1
    
    ##Checks to see if the board is full, if it's not finished is set to False
    for i in range(9):
        for j in range(9):
            ##Checks if variable is set already
            if(type(board[i][j]) is not int):
                ##If not, checks if the domain is of size one
                if len(board[i][j]) != 1:
                    finished = False

    ##If the board is full it loops through to find any variables with a single value in it's domain
    ##If one is found the variable is set to its single value
    if finished:
        for i in range(9):
            for j in range(9):
                ##Checks if variable is set and if not sets value to its domain
                if(type(board[i][j]) is not int):
                    value = board[i][j][0]
                    board[i][j] = value
        return True, calls

    ##Calls Minimum Remaining Values function for the position of move
    move = mrv(board)
    row = move[0]
    col = move[1]

    ##Sets the domain for the given position
    domain = list(board[row][col])

    ##Loops through the variables in the domain and sets the position to the given value
    ##and recursively calls the back tracking algorthem with the new board
    ##if a solution is found it returns True
    for num in domain:
        ##Sets variable to value from domain
        board[row][col] = num

        ##Forward Checks the new board
        viable = forward_checking(board)

        ##If every variable has at least one value the function continues
        if viable:
            results, calls = back_tracking(board, calls)
        
            ##Returns the True if a solution was found
            if results:
                return True, calls

    board[row][col] = []
    
    ##Returns False if no solution was found
    return False, calls
        
    

##Function from Reference #1
# Checks whether it will be
# legal to assign num to the
# given row, col
def isSafe(grid, row, col, num):
   
    # Check if we find the same num
    # in the similar row , we
    # return false
    for x in range(9):
        if type(grid[row][x]) is int:
            if grid[row][x] == num:
                return False
 
    # Check if we find the same num in
    # the similar column , we
    # return false
    for x in range(9):
        if type(grid[x][col]) is int:
            if grid[x][col] == num:
                return False
 
    # Check if we find the same num in
    # the particular 3*3 matrix,
    # we return false
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if type(grid[i + startRow][j + startCol]) is int:
                if grid[i + startRow][j + startCol] == num:
                    return False

    return True



##Takes a game_board and increments through the positions adjusting their domains
##Returns: True if board is valid, False if a variable has no legal values
def forward_checking(game_board):
    ##Nested for loop that iterates through the board
    for row in range(9):
        for col in range(9):
            ##Checks if variable is set, if not func continues
            if(type(game_board[row][col]) is not int):
                    ##Clears previous domain
                    game_board[row][col].clear()

                    ##Checks if 1-9 are legal values
                    for num in range(1,10):
                        safe = isSafe(game_board, row, col, num)

                        ##If a value is legal it is appended to the variables domain
                        if safe:
                            game_board[row][col].append(num)

                     
    return True



##Takes a list of value locations and sets the game board
##Returns the new game board and if it's solvable
def populate_board(locations):
    ##Creates an empty game board
    game_board = []
    for i in range(9):
        game_board.append([])
        for j in range(9):
            game_board[i].append([])   
    
    ##Loops through the locations of each value, 1-9, and adds it sets their locations
    for num in range(9):
        for loc in locations[num]:
            game_board[loc[0]][loc[1]] = num+1

    ##Prints the starting game board
    print_board(game_board)

    ##Precursor Forward Checking Function
    ##Sets variables domains and ensures the game is solvable
    solvable = forward_checking(game_board)
    
    return game_board, solvable



##Takes a list of variable locations and solves a 9x9 sudoku puzzle
##Variable's value is (index + 1)
def sudoku(locations):    
    print("------------------------------------------------------")
    print("Sudoku Solver")
    print("------------------------------------------------------")
    ##Creates a game board with the given variable locations
    game_board, solvable = populate_board(locations)

    ##If the game board is solvable it calls the backtracking algorithem
    if solvable:
        solution, calls = back_tracking(game_board)

    ##Prints no solution if none found
    if not solvable or not solution:
        print("------------------------------------------------------")
        print("No Solution Found")
        print("------------------------------------------------------")
        return
    else: 
        print("------------------------------------------------------")
        print("Results")
        print("------------------------------------------------------")

        ##Prints the solution
        print_board(game_board)

        print("------------------------------------------------------")
        print("Solution Found")
        print("------------------------------------------------------")



def main():
    ##2d lists for game board information
    ##The first index is the value with 1 corresponding to index 0
    ##The second index points to individual locations of the value
    board_a_locations = [[[0,2],[3,3],[4,6],[7,0]],     ##1 locations
                         [[0,5],[7,4]],                 ##2 locations, etc
                         [[1,7],[4,8],[7,3],[8,6]],
                         [[2,0],[3,5],[4,7],[6,4]],
                         [[1,2],[2,5],[5,6],[6,7]],
                         [[1,5],[2,1],[4,0]],
                         [],
                         [[4,3],[5,8],[6,0]],
                         [[5,4],[6,5],[8,2]]]

    board_b_locations = [[[0,4],[2,0],[5,8],[7,3]],
                         [[1,2],[2,6],[3,0]],
                         [[1,7],[3,4],[6,5]],
                         [[1,5],[4,1]],
                         [[0,2],[5,0],[8,7]],
                         [[2,8],[6,3],[7,1]],
                         [[4,6],[5,5],[8,4]],
                         [],
                         [[2,2]]]

    board_c_locations = [[[4,8],[7,7],[8,0]],
                         [[1,1],[2,6]],
                         [[3,0]],
                         [[5,3]],
                         [[1,2],[2,3],[8,4]],
                         [[0,0],[2,4],[6,3],[8,2]],
                         [[0,1],[5,4],[8,7]],
                         [[3,4],[4,6],[6,2]],
                         [[2,1],[3,6],[6,7]]]


    print("Instance A:")
    ##Starts Timer
    ##From Reference #2
    timer = time.time()
    sudoku(board_a_locations)
    ##Ends Timer
    timer = time.time() - timer
    print("Execution Time:\t" + str(timer) + "\n\n")
    print()


    print("Instance B:")
    ##Starts Timer
    ##From Reference #2
    timer = time.time()
    sudoku(board_b_locations)
    ##Ends Timer
    timer = time.time() - timer
    print("Execution Time:\t" + str(timer) + "\n\n")
    

    print("Instance C:")
    ##Starts Timer
    ##From Reference #2
    timer = time.time()
    sudoku(board_c_locations)
    ##Ends Timer
    timer = time.time() - timer
    print("Execution Time:\t" + str(timer) + "\n\n")





main()
