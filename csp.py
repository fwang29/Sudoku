import sys

def csf(bank, grid):
		


if __name__ == '__main__':
	# Parse input files, word bank into a 1D array and grid into a 2D array
	word_bank_file, grid_file = sys.argv[1:3]

	word_bank = []
	grid = [["_" for i in range(9)] for j in range(9)]

	file = open(word_bank_file)
	for line in file:
		word_bank.append(line)
	file.close()

	file = open(grid_file)
	x = y = 0
	for line in file:
		for x in range(0,9):
			grid[y][x] = line[x]
		y += 1
	file.close()
	
	csf(word_bank, grid)
