import itertools
assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def create_units(rows, cols):

    myboxes = cross(rows, cols)
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
    
    main_diag = [rows[i]+cols[i] for i in range(len(rows))]
    secondary_diag = [rows[i]+cols[::-1][i] for i in range(len(rows))]
    diagonal_units = list(set(main_diag + secondary_diag))
    
    myunitlist = row_units + column_units + square_units
    myunits = dict((s, [u for u in myunitlist if s in u]) for s in myboxes)
    mypeers = dict((s, set(sum(myunits[s],[]))-set([s])) for s in myboxes)
    
    return myunits, myunitlist, myboxes, mypeers

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    
    # Use create_units function to return unitlist and peers dict.
    rows = 'ABCDEFGHI'
    cols = '123456789'
    _, unitlist, _, peers = create_units(rows, cols)
    
    # Run a for loop through every unit in unitlist
    for unit in unitlist:
        # Get the boxes with only 2 values in a unit
        double_dgt_boxes = [box for box in unit if len(values[box]) == 2]
        # Get the twin pairs i.e. boxes with the same values occurring in pairs in a given unit.
        n_twins = [[box1, box2] for box1, box2 in itertools.combinations(double_dgt_boxes, 2) if values[box1] == values[box2]]
        # Iterate through the naked twins or boxes
        for twins in n_twins:
            # Store the naked twins value in digits
            digits = values[twins[0]]
            # Find the unique peers shared by the naked twins
            unique_peers = list(set(peers[twins[0]] & peers[twins[1]]))
            # For every box in the unique peer list
            for box in unique_peers:
                # For each digit in naked twins' digits
                for digit in digits:
                    # Check pre-condition that the box has more than 1 digit and is not the same as any of the naked twins
                    # And remove those digits.
                    if len(values[box]) > 1 and box != twins[0] and box != twins[1]:
                        values[box] = values[box].replace(digit, '')
    
    return values



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    rows = 'ABCDEFGHI'
    cols = '123456789'
    
    _, _, boxes, _ = create_units(rows, cols)
    
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    rows = 'ABCDEFGHI'
    cols = '123456789'
    
    _, _, boxes, _ = create_units(rows, cols)
    
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    #rows = 'ABCDEFGHI'
    #cols = '123456789'
    
    #_, _, _, peers = create_units(rows, cols)
    
    #solved_values = [box for box in values.keys() if len(values[box]) == 1]
 
    #for box in solved_values:
    #    digit = values[box]
    #    for peer in peers[box]:
    #        values[peer] = values[peer].replace(digit,'')
            
    #return values
    pass

def only_choice(values):
    
    rows = 'ABCDEFGHI'
    cols = '123456789'
    
    _, unitlist, _, _ = create_units(rows, cols)
    
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    
    rows = 'ABCDEFGHI'
    cols = '123456789'
    
    _, _, boxes, _ = create_units(rows, cols)
    
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
