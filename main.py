from game import CellType


import random


from game import *

def canPlaceOnBoard(b: Board,x: int,y: int, count: int, sum: int) -> bool:
	if b.get(x,y).Type != CellType.EMPTY:
		return False
	potentialCells: int = 8
	x_edge: bool = x==0 or x==b.Size-1
	y_edge: bool = y==0 or y==b.Size-1
	if x_edge and y_edge: 
		potentialCells = 3
	else:
		potentialCells -= 3 if x_edge else 0 
		potentialCells -= 3 if y_edge else 0 
	if potentialCells < count:
		return False
	nCount: int = b.getNeigbourCount(x,y)
	nSum: int   = b.getNeigbourSum(x,y)
	if nCount > count:
		return False
	if nSum > sum:
		return False
	print(potentialCells,"potential cells")
	return True

def getMissingSum(b: Board,x: int,y: int, sum: int) -> int:
	return sum - b.getNeigbourSum(x,y)

def getMissingCount(b: Board,x: int,y: int, count: int) -> int:
	return count - b.getNeigbourCount(x,y)

# Create list of (amount) of numbers, with the total sum of (number)
def composite(number: int, amount: int) -> list[int]:
	
	result: list[int] = [1] * number
	if amount > number:
		result.extend([0] * (amount-number))
	index: int = 0
	while len(result) > amount:
		if result[index] == 0:
			index += 1
			if index >= len(result)-1:
				index = 0
			continue
		p: int = result.pop(index)
		result[index] += p
		index += 1
		if index >= len(result)-1:
			index = 0
	print(f"Compositing {number} with {amount} numbers, by: {result}")
	return result

# returns (amount, sum)
def dicesRoll()-> tuple[int,int]:
	return (random.randrange(1,9),random.randrange(1,20))
def placeComposite(b: Board,x:int, y:int, _arr: list[int])->None:
	arr: list[int|None] = [None]*8
	leftToArrange: list[int] = _arr
	random.shuffle(leftToArrange)
	print(f"trying to place at {x},{y} target amount {len(_arr)}")
	while len(leftToArrange) > 0:
		index = random.randrange(0,8)
		new_pos_x, new_pos_y = x+pos[index][0],y+pos[index][1]
		if not b.isInBounds(new_pos_x,new_pos_y):
			#print(f"not in bounds",new_pos_x,new_pos_y,leftToArrange,x,y)
			continue
		a: CellType = b.get(new_pos_x,new_pos_y).Type
		if(arr[index] != None):
			continue
		arr[index] = leftToArrange.pop()
		print(f"placed {arr[index]} {a} {new_pos_x} {new_pos_y} {pos[index]} {index}")
	b.placeMark(x,y,numbers=arr)


b: Board = Board(size=7)
canPlace: bool = True
placed: bool = False
try:
	while canPlace:
		canPlace = False
		amountToPlace, sumToPlace = dicesRoll()

		for x in range(b.Size):
			if placed:
				placed = False
				break 
			for y in range(b.Size):
				if canPlaceOnBoard(b,x,y,amountToPlace,sumToPlace):
					placeComposite(b,x,y,composite(sumToPlace,amountToPlace))
					placed = True
					canPlace = True
					break
					
except Exception as e:
	print(f"{e.with_traceback(None)}\n{b}")