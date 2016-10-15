import sys
import pprint
import copy

filled = 6
available_grids = []
word_bank = []
grid = [["_" for i in range(9)] for j in range(9)]

# check overlappable and game rules at the same time
def check(row, word, y, x, direction):
    overlapped = 0
    if direction == 0:
        for i in range(0, min(len(word), 9-x)):
            if word[i] == row[x+i]:
                overlapped += 1
            else:
                return False
    else:
        for i in range(0, min(len(word), 9-y)):
            if word[i] == row[y+i]:
                overlapped += 1
            else:
                return False

    l = []
    for r in row:
        if r != "_":
            l.append(r)
            
    for w in word:
        l.append(w)
    #print l
    #print set(l)
    if len(l) != len(set(l)) + overlapped:   # repeated
        return False
    return True

def check_cell(grid, y, x, word, direction):
    overlapped = 0
    if direction == 0:
        for i in range(0, min(len(word), 9-x)):
            if word[i] == row[x+i]:
                overlapped += 1
            else:
                return False
    else:
        for i in range(0, min(len(word), 9-y)):
            if word[i] == row[y+i]:
                overlapped += 1
            else:
                return False
    l = []
    startx = x%3 * 3
    starty = y%3 * 3
    for i in range(0,3):
        for j in range(0,3):
            c = grid[starty+i][startx+j]
            if c != "_":
                l.append(c)
    if direction==0:
        for i in range(0,min(len(word), startx+3-x)):
            l.append(word[i])
    if direction==1:
        for i in range(0,min(len(word), starty+3-y)):
            l.append(word[i])
    #print l
    #print set(l)
    if len(l) != len(set(l)) + overlapped:   # repeated
        return False
    return True


def add_word(grid, direction, y, x, word):
    for i in range(0, len(word)):
        grid[y][x] = word[i]
        if direction == 0:
            x += 1
        else:
            y += 1

def csp(bank, grid, filled, available_grids):
    if filled == 81:
        return grid
    if bank:
        word = bank.pop()
    else:
        return grid
    for agrid in available_grids:
        # check length
        # horizontal
        y = agrid[0]
        x = agrid[1]
        if agrid[1]+len(word) <= 9:
            if check(grid[agrid[0]], word, y, x, 0) and check([row[agrid[1]] for row in grid], word, y, x, 1) and check_cell(grid, agrid[0], agrid[1], word, 0):
                add_word(grid, 0, agrid[0], agrid[1], word)
                available_grids.remove(agrid)
                filled += len(word)
        elif agrid[0]+len(word) <= 9:   # vertical
            if check(grid[agrid[0]], word, y, x, 0) and check([row[agrid[1]] for row in grid], word, y, x, 1) and check_cell(grid, agrid[0], agrid[1], word, 1):
                add_word(grid, 1, agrid[0], agrid[1], word)
                available_grids.remove(agrid)
                filled += len(word)
        new_grid = copy.deepcopy(grid)
        new_bank = list(bank)
        new_available_grids = list(available_grids)
        csp(new_bank, new_grid, filled, new_available_grids)
        
            
            

if __name__ == '__main__':
    # Parse input files, word bank into a 1D array and grid into a 2D array
    word_bank_file, grid_file = sys.argv[1:3]


    file = open(word_bank_file)
    for line in file:
        word_bank.append(line[:len(line)-1])
    file.close()

    file = open(grid_file)
    x = y = 0
    for line in file:
    	for x in range(0,9):
    	    grid[y][x] = line[x]
	y += 1
    file.close()

    for i in range(0,9):
        for j in range(0,9):
            if (grid[i][j] == '_'): 
                available_grids.append((i,j))

	
    csp(word_bank, grid, 6, available_grids)

    # pretty print
    pprint.pprint(grid)
    
