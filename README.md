# Solve Sudoku with AI

## Synopsis

In this project, I have implemented and extended the Sudoku-solving agent to solve _diagonal_ Sudoku puzzles and implement a new constraint strategy called "naked twins". A diagonal Sudoku puzzle is identical to traditional Sudoku puzzles with the added constraint that the boxes on the two main diagonals of the board must also contain the digits 1-9 in each cell (just like the rows, columns, and 3x3 blocks). The naked twins strategy says that if you have two or more unallocated boxes in a unit and there are only two digits that can go in those two boxes, then those two digits can be eliminated from the possible assignments of all other boxes in the same unit.


## How to run

The code to run is `solution.py`. The input is provided by providing numbers for each cell (row wise) followed by a `.` to indicate a cell to be filled by the AI. For example this input `2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3` can be visualized as:

2 . . |. . . |. . .
. . . |. . 6 |2 . .
. . 1 |. . . |. 7 .
------+------+------
. . 6 |. . 8 |. . .
3 . . |. 9 . |. . 7
. . . |6 . . |4 . .
------+------+------
. 4 . |. . . |8 . .
. . 5 |2 . . |. . .
. . . |. . . |. . 3

The solution is displayed as:

2 6 7 |9 4 5 |3 8 1
8 5 3 |7 1 6 |2 4 9
4 9 1 |8 2 3 |5 7 6
------+------+------
5 7 6 |4 3 8 |1 9 2
3 8 4 |1 9 2 |6 5 7
1 2 9 |6 5 7 |4 3 8
------+------+------
6 4 2 |3 7 9 |8 1 5
9 3 5 |2 8 1 |7 6 4
7 1 8 |5 6 4 |9 2 3