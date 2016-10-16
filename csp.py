import sys
import copy
import time


# python csp.py bank1.txt grid1.txt
# python csp.py testbank.txt testgrid.txt

if __name__ == '__main__':
    # Parse input files, word bank into a 1D array and grid into a 2D array
    word_bank_file, grid_file = sys.argv[1:3]
    word_bank = []
    grid = []    

# parse word bank file
    file = open(word_bank_file)    
    for line in file:
        word_bank.append(line.split('\n')[0])
    file.close()

# parse grid file
    with open(grid_file, 'r') as f:
        for l in f.read().split('\n'):
            row = []
            # ignore lines with only whitespace
            if not l.strip():
                continue
            for c in l:
                row.append(c)
            grid.append(row)    


def select_word(word_bank):
    return word_bank.pop()



# return a list of possible assignments in the format
# each possible assignment is a list with [0]=Orientation(H/V), [1]=Row# y, [2]=Col# x, [3]=WORD
def ordered_values(word, grid, assignment):
    # traverse all possible start coordinate in the grid for the word
    # print('\r')
    # print('ordered_values')
    # print('ordered_values word', word)

    # for line in grid:
    #     print(line)
    # print('\r')
    
    values = []
    for y in xrange(0,len(grid)):
        for x in xrange(0,len(grid[0])):
            # Horizontal    
            # length could fit in grid horizontally
            if x + len(word) <= len(grid[0]):                
                tmpX = x
                matching = True
                # try placing the word from current coordinate horizontally
                for char in word:
                    # not matching
                    if grid[y][tmpX] != '_' and grid[y][tmpX].upper() != char.upper():  
                        matching = False
                        # print('not matching H', y, x, word, grid[y][tmpX])
                        break
                    tmpX += 1
                if matching:
                    # print('matching H', y, x, len(word))
                    value = []
                    value.append('H')
                    value.append(y)
                    value.append(x)
                    value.append(word)
                    values.append(value)

            # length out of bound, directly skip        
            # else:
                # print('skip H', y, x, len(word))


            # Vertical
            if y + len(word) <= len(grid):                
                tmpY = y
                matching = True
                # try placing the word from current coordinate vertically
                for char in word:
                    # not matching
                    if grid[tmpY][x] != '_' and grid[tmpY][x].upper() != char.upper():
                        # print('not matching V', y, x, word, grid[tmpY][x]) 
                        matching = False
                        break
                    tmpY += 1
                if matching:
                    # print('matching V', y, x, len(word))
                    value = []
                    value.append('V')
                    value.append(y)
                    value.append(x)
                    value.append(word)
                    values.append(value)

            # length out of bound, directly skip        
            # else:
                # print('skip V', y, x, len(word))   

        # print('\r')               

    return values


def check_consistency(value, grid):
    ori = value[0]
    tmpY = value[1]
    tmpX = value[2]

    blockY = tmpY / 3
    blockX = tmpX / 3

# check col unique
    hashmap = {}
    for y in xrange(0,len(grid)):
        if grid[y][tmpX] == '_':
            continue
        if grid[y][tmpX] in hashmap:
            # print('col not unique\n')
            return False            
        hashmap[ grid[y][tmpX] ] = 1

# check row unique
    hashmap = {}
    for x in xrange(0,len(grid[0])):
        if grid[tmpY][x] == '_':
            continue
        if grid[tmpY][x] in hashmap:
            # print('row not unique\n')
            return False            
        hashmap[ grid[tmpY][x] ] = 1

# check block unique
    hashmap = {}
    for y in xrange(blockY * 3, blockY * 3 + 3):
        for x in xrange(blockX * 3, blockX * 3 + 3):
            if grid[y][x] == '_':
                continue
            if grid[y][x] in hashmap:
                # print('block not unique\n')
                return False            
            hashmap[ grid[y][x] ] = 1

    return True


def recur_backtracking(word_bank, grid, assignment):
    # print('\r')
    # print('recur_backtracking')
    if word_bank == []:        
        for y in xrange(0,len(grid)):
            for x in xrange(0,len(grid[0])):
                if grid[y][x] == '_':
                    # print('word_bank empty, grid not complete\n')
                    return False
        # print('FINISH! word_bank is Empty!')
        return True
    tmp_word_bank = list(word_bank)
    # tmp_grid = copy.deepcopy(grid)
    # tmp_assignment = list(assignment) 

    word = select_word(tmp_word_bank)
    print('word', word)
    # print('tmp_word_bank', tmp_word_bank)
    # print('word_bank', word_bank)
    
    values = ordered_values(word, grid, assignment)
    # print('assigned', assignment)
    # print('possible values', values)

    for value in values:
        # print('value', value)
        # deep copy grid, and apply assignment on tmp_grid
        tmp_grid = copy.deepcopy(grid)
        ori = value[0]
        tmpY = value[1]
        tmpX = value[2]
        for char in word:
            tmp_grid[tmpY][tmpX] = char
            if ori == 'H':
                tmpX += 1
            else:
                tmpY += 1
        
        for line in tmp_grid:
            print(line)
        print('\r')

        # if consistent, add to assignment
        if check_consistency(value, tmp_grid):
            # print('assignment append', assignment, value)
            assignment.append(value)

            # print('\r')
            # print('Recursion')
            if recur_backtracking(tmp_word_bank, tmp_grid, assignment) == True:
                # print('recur_backtracking is True!')
                # print('\r')
                return True
            else:
                # print('assignment pop', assignment)
                # print('\r')
                assignment.pop()

    return False


def csp(word_bank, grid):
    assignment = []
    success = recur_backtracking(word_bank, grid, assignment)
    print('success?', success)
    return assignment




start = time.time()

# sort word_bank by length ascending
word_bank.sort(key = len)
print(len(word_bank))
for word in word_bank:
    print(word)

print(len(grid))
for line in grid:
    print(line)

assignment = csp(word_bank, grid)
print('assignment', assignment)

end = time.time()
print('execution time in seconds', end - start)
























