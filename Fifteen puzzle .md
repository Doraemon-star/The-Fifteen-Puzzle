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

Phase two:

In phase 2, you will solve the rightmost n-2 columns of the remaining two rows, one column at a time from right to left. You task is to implement four methods:
  two invariant methods and two solution medthods. 
We recommend that you implement the two invariant methods "row1_invariant(j) and row0_invariant(j) first. These invariants check whether the solution process has
process has proceeded correctly to positions (1, j) and (0, j), respectively.

The invariant "row1_invariant(j)" should check whether tile 0 is at (1,j) and whether all positions either below or to the right of this position are solved. The 
invariant "row0_invariant(j)" checks a similar condition, but additionally checks whether position(1,j) is also solved.  The images below show a pair of puzzles 
for which "row1_invariant(2)" and "row0_invariant(2)" are true:
  4  6  1  3     4  2   0   3
  5  2  0  7     5  1   6   7 
  8  9 10  11    8  9  10  11
  12 13 14 15    12 13 14  15
 Once thses two invariant methods are implemented correctly, you should implement corresponding solution methods "solve_row1_tile(j)" and "solve_row0_tile(j)".
 These methods should solve for the tiles at positions (1, j) and (0, j), respectively. These solution methods are related to the invariant methods in a manner 
 similar to that of problem #7 on the homework. In particular, the annotated execution trace for the solver should have the form:
 
    assert my_puzzle.row1_invariant(j)
    my_puzzle.solve_row1_tile(j)
    assert my_puzzle.row0_invariant(j)
    my_puzzle.solve_row0_tile(j)
    assert my_puzzle.row1_invariant(j - 1)
    
Implementing "solve_row1_tile(j)" should be straightforward using a method similar to that of"solve_interior_tile"(or using your helper method"postion_tile").
To implement "solve_row0_tile(j), we suggest that you use a method similar to that for "solve_col0_tile".In particular, you should move the zero tile from 
position (0, j) to (1, j - 1) using the move string "ld" and check whether target tile is at position (0, j). If not, 
reposition the target tile to position (1, j - 1) with tile zero in position (1, j - 2). At this point, you can apply the move string from problem 
#10 in the homework to complete the method.

Again, we recommend that you add assert statements to your solution methods that verify that the methods are receiving a puzzle in a proper input configuration and producing a puzzle with the proper output configuration. Once you are confident that these methods are correct, use OwlTest to confirm that they are correct.

Phase Three
You are now ready to implement phase three and complete the mini-project. For this final phase, your task is to implement two solution methods:
  solve_2X2()
  solve_puzzle()
The method "solve_2x2()" solves the final upper left 2 \times 22×2 portion of the puzzle under the assumption that the remainder of the puzzle is solved(i,e,
row1_invariant(1) is true).We recommend that you consult problems #3-5 in the homework for a suggested method.

When building test cases for your solver, note that not all puzzles generated by random placement of the tiles can be solved. For larger puzzles, everything but
the upper left 2 X 2 portion of the puzzle can always be solved. To test this 2 X 2 portion of the solver, we recommend that you build your tests by applying a
sequence of random moves to an unscrambled puzzle.

The final method "solve_puzzle()" takes a solvable Puzzle object and solves the puzzle. This method 
should call the various solution methods that you have implemented and join the move string returned by these methods to form a single move string that solves the 
entire puzzle. Observe the invariants associated with these solution methods link together to guarantee that each solution method receives the puzzle in the 
configuration necessary for the solution process. (Note that on the transition from phase one to phase two, the invariants lower_row_invariant(1, n - "lower_row_invariant(1, n - 1)" and "row1_invariant(n - 1)" are identical.


