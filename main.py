from game import pos, Board, CellType, Cell
import random

def canPlaceOnBoard(b: Board,x: int,y: int, count: int, sum: int) -> bool:
	if b.get(x,y).Type != (CellType.EMPTY or CellType.ZERO):
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

def placeComposite(b: Board,x:int, y:int, _arr: list[int])->None:
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
	b.placeMark(x,y,arr)

b: Board = Board(size=7)
canPlace: bool = True
placed: bool = False

while canPlace:
	canPlace = False
	amountToPlace, sumToPlace = dicesRoll()
	for x in range(b.Size):
		if placed:
			placed = False
			break 
		for y in range(b.Size):
			if canPlaceOnBoard(b,x,y,amountToPlace,sumToPlace):
				comp = composite(sumToPlace,amountToPlace)
				print(f"Placing at ({x},{y})")
				placeComposite(b,x,y,comp)
				print(b)
				placed = True
				canPlace = True
				break
	
				