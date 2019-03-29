
import random
import numpy as np
from copy import copy, deepcopy
#WIP: need to implement 4 things. 1: skyfalls and cascades, 2: predictedcombocount, 3: deal with spaces, 4: tensorflor and scoring option/compete., 
#5: more than 1 board per run, 6: Make each node an object class and link them together in a graph like manner to handle stuff more elegantly.
class gameboard:
	# an initialization of a gameboard of size 6x5 or 7x6 with 6 colors and up to 4 hazards

	def __init__(self, size, hazards):
		if size != 6 and size != 7:
			raise Exception('invalid size')
		if hazards < 0 or hazards > 4:
			raise Exception('invalid hazard #')
		if size == 6:
			self.grid = [[random.randint(1, 6 + hazards), random.randint(1, 6 + hazards), random.randint(1, 6 + hazards), \
			random.randint(1, 6 + hazards), random.randint(1, 6 + hazards), random.randint(1, 6 + hazards)] for i in range(5)]
		if size == 7:
			self.grid = [[random.randint(1, 6 + hazards),random.randint(1, 6 + hazards),random.randint(1, 6 + hazards),\
			random.randint(1, 6 + hazards),random.randint(1, 6 + hazards),random.randint(1, 6 + hazards),random.randint(1, 6 + hazards)] for i in range(6)]
		for i in range(size - 1):
			for j in range(size):
				if self.grid[i][j] == 1:
					self.grid[i][j] = "r"
				if self.grid[i][j] == 2:
					self.grid[i][j] = "b"
				if self.grid[i][j] == 3:
					self.grid[i][j] = "g"
				if self.grid[i][j] == 4:
					self.grid[i][j] = "d"
				if self.grid[i][j] == 5:
					self.grid[i][j] = "l"
				if self.grid[i][j] == 6:
					self.grid[i][j] = "h"
				if self.grid[i][j] == 7:
					self.grid[i][j] = "p"
				if self.grid[i][j] == 8:
					self.grid[i][j] = "j"
				if self.grid[i][j] == 9:
					self.grid[i][j] = "m"
				if self.grid[i][j] == 10:
					self.grid[i][j] = "x"
	def getboard(self):
		returnedmatrix = np.asmatrix(self.grid)
		print(returnedmatrix)
	def getboardpicked(self, choicerow, choicecol):
		tempboard = deepcopy(self.grid)
		tempval = tempboard[choicerow][choicecol]
		tempboard[choicerow][choicecol] = tempval.capitalize()
		print(np.asmatrix(tempboard))
	def countcomboshoriz(self):
		horizmatches = []
		for row in range(size - 1):
			currcolor = self.grid[row][0]
			listindex = []
			for col in range(size):
				thiscolor = self.grid[row][col]
				if thiscolor == ' ':
					listindex = [col]
				if thiscolor == currcolor:
					listindex.append(col)
				else: 
					if currcolor == ' ':
						listindex = [col]
					if len(listindex) > 2:
						horizmatches.append((row, listindex))
					listindex = [col]
					currcolor = thiscolor
			if len(listindex) > 2:
				horizmatches.append((row, listindex))
		return horizmatches #returns list of pairs of row and list of indexes for col
	def countcombosvert(self): 
		vertmatches = []
		for col in range(size):
			currcolor = self.grid[0][col]
			listindex = []
			for row in range(size - 1):
				thiscolor = self.grid[row][col]
				if thiscolor == ' ':
					listindex = [row]
				if thiscolor == currcolor:
					listindex.append(row)
				else: 
					if currcolor == ' ':
						listindex == [row]
					if len(listindex) > 2:
						vertmatches.append((col, listindex))
					listindex = [row]
					currcolor = thiscolor
			if len(listindex) > 2:
				vertmatches.append((col, listindex))
		return vertmatches
	def combining(self, horizontals, verticals):
		count = 0 
		setlistcoord = set() #each is row, col, color
		if horizontals != None:
			for rowlist in horizontals:
				validcombo = True
				for node in rowlist[1]:
					row = rowlist[0]
					coordinate = [row, node, self.grid[row][node]]
					coordup = (row - 1, node, self.grid[row][node])
					coorddown = (row + 1, node, self.grid[row][node])
					for coord in setlistcoord:
						if coord == coordup or coord == coorddown:
							validcombo = False
				if validcombo == True:
					count += 1
				for node in rowlist[1]:
					row = rowlist[0]
					setlistcoord.add((row, node, self.grid[row][node]))
		if verticals == None:
			return count
		for collist in verticals:
			validcombo = True
			for node in collist[1]:
				col = collist[0]
				coordinate = [node, col, self.grid[node][col]]
				coordleft = (node, col - 1, self.grid[node][col])
				coordright = (node, col + 1, self.grid[node][col])
				for coord in setlistcoord:
					if coord == coordleft or coord == coordright:
						validcombo = False
			if validcombo == True:
				count += 1
			for node in collist[1]:
				col = collist[0]
				setlistcoord.add((node, col, self.grid[node][col]))
		for coord in setlistcoord:
			self.grid[coord[0]][coord[1]] = ' '
		return count
	def cascade(self):
		arbitrary = 20
		while arbitrary > 0:
			for row in range(size - 2):
				for col in range(size):
					if self.grid[row + 1][col] == ' ':
						self.grid[row + 1][col] = self.grid[row][col]
						self.grid[row][col] = ' '
			arbitrary -= 1
	def countcombos(self):
		horizontals = self.countcomboshoriz()
		verticals = self.countcombosvert()
		totalmatches = self.combining(horizontals, verticals)
		bottomup = reversed(range(size - 1))
		cascade = True
		count = 10
		while cascade == True and count != 0:
			self.cascade()
			horizcasc = self.countcomboshoriz()
			verticasc = self.countcombosvert()
			extra = self.combining(horizcasc, verticasc)
			totalmatches = totalmatches + extra - 1
			if extra == 1:
				cascade = False
			count -= 1
		self.getboard()
		print('your board has ' + str(totalmatches) + ' combos on it. The AI found a solve with # .') #finish later.




size = int(input("What board size would you like, 6x5(type 6) or 7x6(type 7) "))
hazards = int(input("How many colors would you like (base of 6, type 0, 1, 2, 3, or 4 for up to 4 additional) "))
moves = int(input("How many moves do you wish to allow yourself(recommendation is 70) "))
difficulty = input("Would you like easy, medium, hard, or cyan(sticky blind) level (type easy, medium, hard, or cyan): ")
if difficulty != 'easy' and difficulty != 'medium' and difficulty != 'hard' and difficulty != 'cyan':
	raise Exception('invalid difficulty selection')
print("game size is " + str(size))
board = gameboard(size, hazards)
board.getboard()
choicerow = int(input("Choose which node to pick up (row number): ")) - 1
if choicerow > size - 2 or choicerow < 0:
	raise Exception('invalid row choice')
choicecol = int(input("Choose which node to pick up (column number): ")) - 1
if choicecol > size - 1 or choicecol < 0:
	raise Exception('invalid column choice')
while moves > 0:  #main game loop
	print('You currently have ' + str(moves) + ' moves left')
	board.getboardpicked(choicerow, choicecol)
	if difficulty == 'cyan':
		movestr = input('Please type all of your moves without spaces in between, (w = up, a = left, s = down, d = right, x = finished) only the first ' + str(moves) + 'will count: ')
		movelist = list(movestr)
		counter = moves
		for move in movelist:
			if counter == 0:
				break
			if move == 'w':
				if choicerow > 0:
					temp = board.grid[choicerow][choicecol]
					board.grid[choicerow][choicecol] = board.grid[choicerow - 1][choicecol]
					board.grid[choicerow - 1][choicecol] = temp
					choicerow -= 1
			elif move == 'a':
				if choicecol > 0:
					temp = board.grid[choicerow][choicecol]
					board.grid[choicerow][choicecol] = board.grid[choicerow][choicecol - 1]
					board.grid[choicerow][choicecol - 1] = temp
					choicecol -= 1
			elif move == 's':
				if choicerow < size - 2:
					temp = board.grid[choicerow][choicecol]
					board.grid[choicerow][choicecol] = board.grid[choicerow + 1][choicecol]
					board.grid[choicerow + 1][choicecol] = temp
					choicerow += 1
			elif move == 'd':
				if choicecol < size - 1:
					temp = board.grid[choicerow][choicecol]
					board.grid[choicerow][choicecol] = board.grid[choicerow][choicecol + 1]
					board.grid[choicerow][choicecol + 1] = temp
					choicecol += 1
			elif move == 'x':
				moves = 0
				break;
			counter -= 1
		board.getboard()
		moves = 0
	if difficulty == 'hard':
		remmoves = 10
		if moves < 10:
			remmoves = moves
		movestr = input('Please type ' + str(remmoves) + ' moves without spaces in between, (w = up, a = left, s = down, d = right, x = finished) only the first ' + str(remmoves) +' will count: ')
		movelist = list(movestr)
		counter = remmoves
		for move in movelist:
			if counter == 0:
				break
			if move == 'w':
				if choicerow > 0:
					temp = board.grid[choicerow][choicecol]
					board.grid[choicerow][choicecol] = board.grid[choicerow - 1][choicecol]
					board.grid[choicerow - 1][choicecol] = temp
					choicerow -= 1
			elif move == 'a':
				if choicecol > 0:
					temp = board.grid[choicerow][choicecol]
					board.grid[choicerow][choicecol] = board.grid[choicerow][choicecol - 1]
					board.grid[choicerow][choicecol - 1] = temp
					choicecol -= 1
			elif move == 's':
				if choicerow < size - 2:
					temp = board.grid[choicerow][choicecol]
					board.grid[choicerow][choicecol] = board.grid[choicerow + 1][choicecol]
					board.grid[choicerow + 1][choicecol] = temp
					choicerow += 1
			elif move == 'd':
				if choicecol < size - 1:
					temp = board.grid[choicerow][choicecol]
					board.grid[choicerow][choicecol] = board.grid[choicerow][choicecol + 1]
					board.grid[choicerow][choicecol + 1] = temp
					choicecol += 1
			elif move == 'x':
				moves = 0
				break;
			counter -= 1
		moves -= remmoves
		if moves > 0:
			board.getboardpicked(choicerow, choicecol)
		else:
			board.getboard()
	if difficulty == 'medium':
		remmoves = 5
		if moves < 5:
			remmoves = moves
		movestr = input('Please type ' + str(remmoves) + ' moves without spaces in between, (w = up, a = left, s = down, d = right, x = finished) only the first ' + str(remmoves) +' will count: ')
		movelist = list(movestr)
		counter = remmoves
		for move in movelist:
			if counter == 0:
				break
			if move == 'w':
				if choicerow > 0:
					temp = board.grid[choicerow][choicecol]
					board.grid[choicerow][choicecol] = board.grid[choicerow - 1][choicecol]
					board.grid[choicerow - 1][choicecol] = temp
					choicerow -= 1
			elif move == 'a':
				if choicecol > 0:
					temp = board.grid[choicerow][choicecol]
					board.grid[choicerow][choicecol] = board.grid[choicerow][choicecol - 1]
					board.grid[choicerow][choicecol - 1] = temp
					choicecol -= 1
			elif move == 's':
				if choicerow < size - 2:
					temp = board.grid[choicerow][choicecol]
					board.grid[choicerow][choicecol] = board.grid[choicerow + 1][choicecol]
					board.grid[choicerow + 1][choicecol] = temp
					choicerow += 1
			elif move == 'd':
				if choicecol < size - 1:
					temp = board.grid[choicerow][choicecol]
					board.grid[choicerow][choicecol] = board.grid[choicerow][choicecol + 1]
					board.grid[choicerow][choicecol + 1] = temp
					choicecol += 1
			elif move == 'x':
				moves = 0
				break;
			counter -= 1
		moves -= remmoves
		if moves > 0:
			board.getboardpicked(choicerow, choicecol)
		else:
			board.getboard()
	if difficulty == 'easy':
		remmoves = 1
		if moves < 1:
			remmoves = moves
		movestr = input('Please type ' + str(remmoves) + ' moves without spaces in between, (w = up, a = left, s = down, d = right, x = finished) only the first ' + str(remmoves) +' will count: ')
		movelist = list(movestr)
		counter = remmoves
		for move in movelist:
			if counter == 0:
				break
			if move == 'w':
				if choicerow > 0:
					temp = board.grid[choicerow][choicecol]
					board.grid[choicerow][choicecol] = board.grid[choicerow - 1][choicecol]
					board.grid[choicerow - 1][choicecol] = temp
					choicerow -= 1
			elif move == 'a':
				if choicecol > 0:
					temp = board.grid[choicerow][choicecol]
					board.grid[choicerow][choicecol] = board.grid[choicerow][choicecol - 1]
					board.grid[choicerow][choicecol - 1] = temp
					choicecol -= 1
			elif move == 's':
				if choicerow < size - 2:
					temp = board.grid[choicerow][choicecol]
					board.grid[choicerow][choicecol] = board.grid[choicerow + 1][choicecol]
					board.grid[choicerow + 1][choicecol] = temp
					choicerow += 1
			elif move == 'd':
				if choicecol < size - 1:
					temp = board.grid[choicerow][choicecol]
					board.grid[choicerow][choicecol] = board.grid[choicerow][choicecol + 1]
					board.grid[choicerow][choicecol + 1] = temp
					choicecol += 1
			elif move == 'x':
				moves = 0
				break;
			counter -= 1
		moves -= remmoves
		if moves > 0:
			board.getboardpicked(choicerow, choicecol)
		else:
			board.getboard()
board.countcombos()


