import copy
import itertools
from utils import *

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
principal_diagonal_units = [[rows[i]+cols[i] for i in range(9)]]
secondary_diagonal_units = [[rows[i]+cols[::-1][i] for i in range(9)]]
unitlist = row_units + column_units + square_units + principal_diagonal_units + secondary_diagonal_units

def is_correct_solution(d):
    for unit in unitlist:
        total = sum([int(d[k]) for k in unit])
        if total != 45:
            return 'INCORRECT SOLUTION'
    return 'CORRECT'

# Must be called after all units (including diagonals) are added to the unitlist
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def naked_twins(d):
    """Eliminate values using the naked twins strategy.
    Args:
        d(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the d dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        # finding all keys that have 2 options only
        pairs = [cell for cell in unit if len(d[cell]) == 2]
        # create possible combinations of those all in a unit
        possible_twins = [list(pair) for pair in itertools.combinations(pairs, 2)]
        for k1, k2 in possible_twins:
            # for every possible combinition, check if they hold the same values
            if d[k1] == d[k2]:
                for cell in unit:
                    # in which cases remove them both from their peers
                    if cell != k1 and cell != k2:
                        d[cell] = d[cell].replace(d[k1][0],'').replace(d[k1][1],'')
    return d


def eliminate(d):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    for k,v in d.items(): 
        if len(v) == 1:
            for unit in unitlist:
                if k in ''.join(unit):
                    for value in unit:
                        if len(d[value]) > 1:
                            d[value] = d[value].replace(v,'')
    return d


def only_choice(d):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned
    """
    for k,v in d.items():
        if len(v) > 1:
            for unit in unitlist:
                if k in ''.join(unit):
                    values_of_remaining_units = ''.join([d[key] for key in unit if key != k])
                    for char in v:
                        if char not in ''.join(values_of_remaining_units):
                            d[k] = char
    return d


def reduce_puzzle(d):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    solved_values = [box for box in d.keys() if len(d[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in d.keys() if len(d[box]) == 1])
        d = eliminate(d)
        d = only_choice(d)
        d = naked_twins(d)
        solved_values_after = len([box for box in d.keys() if len(d[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in d.keys() if len(d[box]) == 0]):
            return False
    return d


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False
    """
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = copy.deepcopy(values)
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values

if __name__ == "__main__":
    sudoku_input = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3' #input("Please input the sudoku: ")
    # s1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..' 
    # s2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    # s3 ='.'*81 
    # ll = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
    # s4 = ''.join([''.join(x) for x in ll])
    result = solve(sudoku_input) 
    display(result)