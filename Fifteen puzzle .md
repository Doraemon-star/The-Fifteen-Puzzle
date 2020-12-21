# The-Fifteen-Puzzle
                                                      Overview
                                                      
This week's homework introduced you to the Fifteen puzzle and outlined the highlights of building a solver for the puzzle.
As described in the homework, the solutioin process for a puzzle of size m X n has three phases:
  1. Solve the bottom m-2 rows of the puzzle in a row manner from bottom to top. Each individual row will be solved in a right to left
     order.
  2. Solve the rightmost n-2 columns of the top two rows of the puzzle(in a right to left order). Eac column consists of two unsolved 
     positions and will be solved in a bottom to top order
  3. Solve the upper left 2 X 2 portion of the puzzle directly
  
As noted in the homework, we have provided a program template(http://www.codeskulptor.org/#poc_fifteen_template.py) that includes 
a partially implemented Puzzle class that allows you to interaxt with a GUI designed to simulate the Fifteen puzzle. Your task for this
mini-project is to write a collection of Puzzle methods that implement each phase ofthe solution process. Several of these methods will
correspond to invariants designed to help guide you towards a correct implementation of the solver. The remaining methods are solution 
methods fro portions of the puzzle. Note that each of these solution methods updates the puzzle and returns the move string associated with 
this update.

                                              Testing your mini project
The provided template includes stubs for the methods that you will need to implement for htis mini-project. You should write tests for the 
Puzzle methods as you implement them. (Notw that the initializer for a Puzzle object accepts an optional initial configuration for the 
Puzzle that is specified as a 2D list of integers.) This mini-project is difficult. If you attempt to implement all of the methods before 
doing any testing, the mini-projext will be impossible. 

Phase one:

In this phase, your task is to implement three methods: one invariant method and two solution methods. The invariant method for this phase
is "lower_row_invariant(i, j)". This method should:
    1. Tile 0 is positioned at (i, j)
    2. All tiles in rows i+1 or below are positioned at their solved location
    3. All tiles in row i to the right of position (i, j) are positioned at their solved location.
You should implement and fully test "lower_row_invariant" before proceeding. In particular, we suggesst that you test this method using
OwlTest(http://codeskulptor.appspot.com/owltest?urlTests=poc.poc_fifteen_tests.py&urlPylintConfig=poc.pylint_config.py&imports=%7Bpoc:(poc_fifteen_gui)%7D)
to confirm that your implementation of this method is correct before proceeding. Next, you will implement the two solution methods for 
this phase: "solve_interior_tile" and "solve_col0_tile".

The method "solve_interior_tile(i, j)" is designed to solve the puzzle at position(i, j) where i>1 and J>0. Specifically, this method takes 
a puzzle for which "lower_row_invariant(i, j)" is true and repositions the tiles in the puzzle such that "lower_row_invariant(i, j-1) is 
true. To implement "solve_interior_tile", we suggest that you review problem 8 on the homework.

The second solution method "solve_col0_tile(i)" is designed to solve the puzzle at position(i, 0) where i>1. Specifically, this method 
takes a puzzle that satisfies the invariant "lower)row_invariant(i, 0)" and repositions the tiles in the puzzle such that 
"lower_row_invariant(i-1, n-1) is true where n is the width of the grid. Implementing "solve_col0_tile is trickier than " solve_interior_tile"
since the solution strategy for "solve_interior_tile(i,j)" invilved moving tile 0 through column j-1. In the case of the left column 
where j = 0, this solution process is not feasible.

Our recommended strategy for "solve_col0_tile" si to move the 0 tile from (i,0) to (i-1, 1) using the move string "ur". If you are lucky 
and the target tile(i.e. the tile being solved for) is now at position(i, 0), you can simply move tile zero to the end of row i-1 and 
be done. However, if the targe tile is not positioned at (i, 0), we suggest the following solution strategy:
  1. Reposition the target tile to position (i-1,1) and the 0 tile to position(i-1,0) using a process similar tothat of "solve_interior_tile",
  2. Then apply the move string for a 3 X 2 puzzle as described in problem #9 of the homework to bring the target tile into position(i0)
  3. Finally, conclude by moving tile 0 to the right end of row i-1.
Note the process for the first step is so similar to that of solve-interior_tile that you may wish to refactor your implementation to 
include a helper method "position_tile" that is used by both tasks.

Note that the invariant method "lower_row_invariant" can be extremely valuable as you test and debug "solve_interior_tile" and "solve_col0_tile".
Minimally, we recommend that you add "assert"statements to your solution metods that verify that these methods are reciving a puzzle in a 
proper input configuration and producing a puzzle with the proper output configuration. Once you are confideng that these methods are correct,
use OwlTest to confirm that they are correct.

