import re
import string
import itertools

LETTERS = string.ascii_uppercase
LETTER_NUMS = {let: ii + 1 for ii, let in enumerate(LETTERS)}


def to_excel_colname(n):
    '''convert an integer 1 <= n <= 16384 to an Excel column name 
    (uppercase letters)'''
    if not (1 <= n <= 16384):
        raise ValueError('Column number must be between 0 and 16383')
    if n == 1:
        return 'A'
    out = ''
    while n > 0:
        n, m = divmod(n-1, 26)
        out += LETTERS[m]

    return out[::-1]


def from_excel_colname(colname):
    '''convert an Excel column name (uppercase letters) to an integer'''
    out = 0
    for ii, let in enumerate(colname[::-1]):
        out += LETTER_NUMS[let] * 26 ** ii
    if out > 16384:
        raise ValueError(f'Column numbers greater than 16384 (name "XFD") are impossible')

    return out


def from_excel_cell(cell):
    '''take a string of the form <colname><rownum> and return (row, col)'''
    colrow = re.findall('([A-Z]+)(\d+)', cell)
    if not colrow:
        raise ValueError('cell must be uppercase letters followed by numbers')
    col = from_excel_colname(colrow[0][0])
    row = int(colrow[0][1])

    return row, col


def from_excel_range(rng):
    '''take a string of the form <colname><rownum>:<colname2><rownum2>
    and output (range(row1, row2 + 1), range(col1, col2 + 1))'''
    if ':' not in rng:
        cell1, cell2 = rng, rng
    else:
        cell1, cell2 = rng.split(':')
    row1, col1 = from_excel_cell(cell1)
    row2, col2 = from_excel_cell(cell2)
    if row1 <= row2:
        startrow, endrow, rowstep = row1, row2 + 1, 1
    else:
        startrow, endrow, rowstep = row1, row2 - 1, -1
    if col1 <= col2:
        startcol, endcol, colstep = col1, col2 + 1, 1
    else:
        startcol, endcol, colstep = col1, col2 - 1, -1

    return range(startrow, endrow, rowstep), range(startcol, endcol, colstep)


def to_excel_range(row1, col1, row2 = None, col2 = None):
    '''Get an Excel range (<colname><int>:<colname><int>) with (row1, col1) 
    as the starting row and column, and (row2, col2) as the ending row and
    column.
    If row2 is None, row1 is the ending row and 1 is the starting row.
    If col2 is None, row1 is the ending row and A is the starting column.
    '''
    if row2 is None:
        row1, row2 = 1, row1
    if col2 is None:
        col1, col2 = 1, col1

    return f'{to_excel_colname(col1)}{row1}:{to_excel_colname(col2)}{row2}'


def cells_in_range(rng):
    '''Return a list of the cells in an Excel range <col1><row1>:<col2><row2>
    or a list of two tuples [(row1, row2), (col1, col2)].
    rng can also be a single Excel cell.
    The cells are returned in C order (so reading left to right and top to
    bottom, assuming row1 <= row2 and col1 <= col2).'''
    if isinstance(rng, tuple) and isinstance(rng[0], range):
        parsed_rng = rng
    else:
        parsed_rng = from_excel_range(rng)

    return list(itertools.product(*parsed_rng))


def cells_from_array(arr, rng):
    '''For an Excel range or an Excel cell, return the values at the
    corresponding indices in a 2D array.
    See cells_in_range for how rng is translated into indices.'''
    return [arr[row - 1][col - 1] for row, col in cells_in_range(rng)]


def range_containing_table(df, index=False, start_cell='A1'):
    if isinstance(start_cell, str):
        start_row, start_col = from_excel_cell(start_cell)
    
    nrow, ncol = df.shape
    end_row, end_col = start_row + nrow, start_col + ncol
    if not index:
        end_col -= 1
    
    return to_excel_range(start_row, start_col, end_row, end_col)