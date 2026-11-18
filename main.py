from game import pos, Board, CellType, Cell
import random

def canPlaceOnBoard(b: Board,x: int,y: int, count: int, sum: int) -> bool:
	type = b.get(x,y).Type
	if type != CellType.EMPTY and type != CellType.ZERO:
		return False
	nSum: int   = 0
	potential_cells: int = 8

	for offset in pos:
		curr_pos: tuple[int, int] = x+offset[0],y+offset[1]
		if not b.isInBounds(curr_pos[0],curr_pos[1]):
			potential_cells-=1
			continue
		cell: Cell = b.get(curr_pos[0],curr_pos[1])
		if cell.Type != CellType.EMPTY:
			if cell.Type == CellType.NUMBER:
				nSum+=cell.getValue()
			potential_cells-=1
			continue
	
	if potential_cells < count:
		return False
	if nSum > sum:
		return False
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

def arrangeComposite(b: Board,x:int, y:int, _arr: list[int])-> list[int]:
	arr: list[int|None] = [None]*8
	leftToArrange: list[int] = _arr.copy()
	offsets: list[tuple[int,tuple[int,int]]] = [(index,pos) for (index, pos) in enumerate(pos.copy())]
	random.shuffle(leftToArrange)
	random.shuffle(offsets)
	while len(leftToArrange) > 0:
		new_offset: tuple[int,int]
		new_index: int = -1
		for offset in offsets:
			potential_pos: tuple[int, int] = x+offset[1][0],y+offset[1][1]
			if arr[offset[0]] != None or not b.isInBounds(potential_pos[0],potential_pos[1]) or b.get(potential_pos[0],potential_pos[1]).Type != CellType.EMPTY:
				continue
			new_index = offset[0]
			new_offset = offset[1]
			break
		if new_index < 0:
			raise Exception(f"No room left for placing! Left in array: {leftToArrange}")
			break
		new_pos: tuple[int, int] = (new_offset[0] + x,new_offset[1]+y)
		arr[new_index] = leftToArrange.pop()
	return arr
b: Board = Board(size=7)
canPlace: bool = True
placed: bool = False
zeroes: list[tuple[int,int]] = []
positionsToCheck: list[tuple[int,int]] = []
for x in range(b.Size):
	for y in range(b.Size):
		positionsToCheck.append((x,y))
while canPlace:
	canPlace = False
	amountToPlace, sumToPlace = dicesRoll()

	if len(zeroes) > 0:
		print(f"Zeroes found: {zeroes}")
		for zero in zeroes:
			positionsToCheck.remove(zero)
			positionsToCheck.insert(0,zero)
		zeroes.clear()
	
	for c_pos in positionsToCheck:
		x=c_pos[0]
		y=c_pos[1]
		if canPlaceOnBoard(b,x,y,amountToPlace,sumToPlace):
			comp = composite(sumToPlace,amountToPlace)
			comp = arrangeComposite(b,x,y,comp)
			if 0 in comp:
				for (index, element) in enumerate(comp):
					if element == 0:
						curr_offset = pos[index]
						zeroes.append((curr_offset[0]+x,curr_offset[1]+y))
			print(f"Placing at ({x},{y})"+(" (zero)" if b.get(x,y).Type==CellType.ZERO else ""))
			b.placeMark(x,y,comp)
			positionsToCheck.remove((x,y))
			print(b)
			
			canPlace = True
			break
print(f"Game end! Score: {b.getScore()}")
				