from utils import *

# `grid` is defined in the test code scope as the following:
# (note: changing the value here will _not_ change the test code)
grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    sudoku = {}
    for i in range(len(boxes)):
        sudoku[boxes[i]] = '123456789' if grid[i] == '.' else grid[i]
    return sudoku

def eliminate(values):
    for key in values:
        if len(values[key]) == 1:
            for pkey in peers[key]:
                values[pkey] = values[pkey].replace(values[key], '')
    return values

display(eliminate(grid_values(grid)))


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for i in '123456789':
            choices = [key for key in unit if i in values[key]]
            if len(choices) == 1:
                values[choices[0]] = i
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False
    if len([k for k in values if len(values[k]) > 1]) == 0:
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    length,key = min([(len(values[key]), key) for key in values if len(values[key]) > 1])
    #print([(values[key], key) for key in values if len(values[key]) > 1])
    for d in values[key]:
        new_vals = values.copy()
        new_vals[key] = d
         # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
        searched = search(new_vals)
        if searched:
            return searched

    # If you're stuck, see the solution.py tab!