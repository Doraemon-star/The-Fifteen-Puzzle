"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """       
        if self.get_number(target_row, target_col) == 0:                     
            
            for row in range(target_row +1, self._height):
                    for col in range(self._width):                        
                        if  self.get_number(row, col) != (col + self._width * row):
                            return False
                
            for col in range(target_col + 1, self._width):                
                if self.get_number(target_row, col) != col + self._width * target_row:
                    return False                  
            return True
            
        return False
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col), "wrong condition"
        
        # find the matched tile's current position
        current_pos = self.current_position(target_row, target_col)
        # if tartet tile is in the same col
        if target_col == current_pos[1]:
            str1 = (target_row - current_pos[0]) * "u" + (target_row - current_pos[0]-1) * "lddru" + "ld" 
            
        # if tartet tile is in right
        elif target_col < current_pos[1]: 
            # tartet tile is in row 0
            if current_pos[0] == 0:
                str1 = (target_row - current_pos[0]) * "u" + (current_pos[1] - target_col) * "r" + \
                        (current_pos[1] - target_col - 1) * "dllur" + "dlu" + (target_row - current_pos[0]-1) * "lddru" + "ld"
            # tartet tile is below row 0    
            else:
                str1 = (target_row - current_pos[0]) * "u" + (current_pos[1] - target_col) * "r" + \
                    (current_pos[1] - target_col - 1) * "ulldr" + "ul" + (target_row - current_pos[0]) * "lddru" + "ld"
                
        # if tartet tile is in left
        else:
            # tartet tile is in row 0
            if current_pos[0] == 0:
                str1 = str1 = (target_row - current_pos[0]) * "u" + (target_col - current_pos[1]) * "l" + \
                    (target_col -current_pos[1] - 1) * "drrul" + "dru" + (target_row - current_pos[0]-1) * "lddru" + "ld"
            # tartet tile is in target_row     
            elif current_pos[0] == target_row:
                str1 = (target_col - current_pos[1]) * "l" + (target_col -current_pos[1] - 1) *"urrdl"
                
            # tartet tile is in row1 to row sself._height -2
            else:       
                str1 = (target_row - current_pos[0]) * "u" + (target_col - current_pos[1]) * "l" + \
                    (target_col -current_pos[1] - 1) * "urrdl" + "ur" + (target_row - current_pos[0]) * "lddru" + "ld"
                
        self.update_puzzle(str1)
        assert self.lower_row_invariant(target_row, target_col - 1), "wrong moves"
        return str1 

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0), "wrong condition"
        current_pos = self.current_position(target_row, 0)
        if current_pos == (target_row - 1, 0):
            str1 = "u" + (self._width - 1) * "r"
            self.update_puzzle(str1)
            assert self.lower_row_invariant(target_row - 1, self._width - 1), "wrong moves"
            return str1
        
        elif current_pos[0] != target_row - 1 and current_pos[1] == 0:
            str1 = (target_row - current_pos[0]) * "u" + (target_row - current_pos[0]-1-1) * "rddlu" + "rdl" + \
                   "ruldrdlurdluurddlu" + (self._width - 1) * "r"
            self.update_puzzle(str1)
            assert self.lower_row_invariant(target_row - 1, self._width - 1), "wrong moves"
            return str1
        
        elif current_pos[1] > 0 and current_pos[0] > 0:
            str1 = (target_row - current_pos[0]) * "u" + current_pos[1] * "r" + \
                   (current_pos[1]-1) * "ulldr" + "dlu" + (target_row - current_pos[0]-1-1) * "rddlu" + "rdl" \
                   + "ruldrdlurdluurddlu" + (self._width - 1) * "r"
            self.update_puzzle(str1)
            assert self.lower_row_invariant(target_row - 1, self._width - 1), "wrong moves"
            return str1
        else:
            str1 = (target_row - current_pos[0]) * "u" + current_pos[1] * "r" + \
                   (current_pos[1]-1) * "dllur" + "dlu" + (target_row - current_pos[0]-1-1) * "rddlu" + "rdl"\
                   + "ruldrdlurdluurddlu" + (self._width - 1) * "r"
            self.update_puzzle(str1)
            assert self.lower_row_invariant(target_row - 1, self._width - 1), "wrong moves"
            return str1
    
    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """   
       
        if self.get_number(0, target_col) == 0:                     
            
            for row in range(2, self._height):
                    for col in range(self._width):                        
                        if  self.get_number(row, col) != (col + self._width * row):
                            return False
                
            for col in range(target_col, self._width):                
                if self.get_number(1, col) != col + self._width:
                    return False 
            
            for col in range(target_col + 1, self._width):                
                if self.get_number(0, col) != col:
                    return False 
            return True
            
        return False
            
 
    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
       
        if self.lower_row_invariant(1, target_col): 
            for col in range(target_col + 1, self._width -1 ):
                cell_value = self.get_number(0, col)
                if cell_value != col:
                    return False
            return True
        return False
            
    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col), "wrong condition"
        current_pos = self.current_position(0,target_col)        
        if current_pos == (0, target_col -1):
            str1 = "ld"
            self.update_puzzle(str1)
            assert self.row1_invariant(target_col-1), "wrong moves"
            return str1
        else:
            if current_pos[0] ==0:
                str1 = (target_col - current_pos[1]) * "l" + (target_col-current_pos[1]-2) * "drrul" + "druld" + "urdlurrdluldrruld"
                self.update_puzzle(str1)
                assert self.row1_invariant(target_col-1), "wrong moves"
                return str1
            else:
                
                if current_pos[1] != 0:
                    str1 = (target_col - current_pos[1] +1) * "l" + "d" + (target_col - current_pos[1]-1) * "urrdl" + "urdlurrdluldrruld"
                    self.update_puzzle(str1)
                    assert self.row1_invariant(target_col-1), "wrong moves"
                    return str1
                else:
                    str1 =  (target_col - current_pos[1] -1) * "l" + "dl" + (target_col - current_pos[1]-2) * "urrdl" + "urdlurrdluldrruld"
                    self.update_puzzle(str1)
                    assert self.row1_invariant(target_col-1), "wrong moves"
                    return str1


    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col), "wrong condition"
        current_pos = self.current_position(1, target_col)
        if current_pos[0] == 1:
            str1 = (target_col - current_pos[1]) * "l" + (target_col - current_pos[1] - 1) * "urrdl" + "ur"
            self.update_puzzle(str1)
            assert self.row0_invariant(target_col), "wrong moves"
            return str1
        else:
            if current_pos[1] == target_col:
                str1 = "u"
                self.update_puzzle(str1)
                assert self.row0_invariant(target_col), "wrong moves"
                return str1
            else:
                str1 = (target_col - current_pos[1]) * "l" + (1-current_pos[0]) * "u" +"rdl" \
                   + (target_col - current_pos[1] - 1) * "urrdl" + "ur"
                self.update_puzzle(str1)
                assert self.row0_invariant(target_col), "wrong moves"
                return str1
            
    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1), "wrong condition"
       
        first_move = "ul"
        self.update_puzzle(first_move)
        if self.current_position(0, 1) ==(0, 1) and self.current_position(1, 1) ==(1, 1):
            return first_move
        if self.get_number(0,1) < self.get_number(1,0):
            str1 = "rdlu"
        else:
            str1 = "drul"
        self.update_puzzle(str1)
        return first_move + str1

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        
        # find 0 tile and put it to right lower coner
        current_0_pos = self.current_position(0, 0)
        str1 = "r" * (self._width -1 -current_0_pos[1]) + "d" * (self._height -1 -current_0_pos[0])
        self.update_puzzle(str1)
        start_pos = (self._height -1,self._width -1)
        # apply phase one
        while start_pos != (1, self._width-1):
            if start_pos[1] > 0:
                str1 += self.solve_interior_tile(start_pos[0], start_pos[1])                               
                start_pos = (start_pos[0], start_pos[1]-1)
            else:
                str1 += self.solve_col0_tile(start_pos[0])                        
                start_pos = (start_pos[0]-1, self._width-1)        
            
        while start_pos != (1, 1):
            str1 += self.solve_row1_tile(start_pos[1])
            start_pos =(0 , start_pos[1])
            str1 += self.solve_row0_tile(start_pos[1])             
            start_pos = (1, start_pos[1] -1)
       
        str1 += self.solve_2x2()
               
        return str1

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(3, 3))
