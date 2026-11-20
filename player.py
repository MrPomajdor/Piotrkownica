from enum import  Flag
from typing import override
from game import pos, Board, CellType, Cell
import random

class GameResult:
	EndZeroes: int = 0
	Sum: int = 0
	Score: float = 0
	Marks: int = 0
	Filled: int = 0
	BoardSize: int = 0

	@override
	def __str__(self) -> str:
		p = int(self.Filled/(self.BoardSize*self.BoardSize)*100)
		res: str  = f"""----------Game result----------
	Score: {self.Score}
	Zeroes: {self.EndZeroes}
	Marks: {self.Marks}
	Sum of numbers: {self.Sum}
	Filled cells: {self.Filled} ({p}%)
-------------------------------
"""
		return res

class MarkPlaceBias(Flag):
	RANDOM = 1
	SCAN = 2
	CORNERS_FIRST = 8
	ZEROES_FIRST = 16

class PlayerSettings:
	def __init__(self, place_bias: MarkPlaceBias, board_size: int = 7, max_sum: int=20):
		self.board_size: int = board_size
		self.placeBias: MarkPlaceBias = place_bias
		self.maxSum: int = max_sum
	@override
	def __str__(self) -> str:
		return f"""--------------Game Settings--------------
  Board Size: {self.board_size}
  Place Bias: {self.placeBias}
  Max Sum Per Mark: {self.maxSum}
-----------------------------------------
"""
class GamePlayer:
	def __init__(self,playSettings: PlayerSettings):
		if MarkPlaceBias.RANDOM in playSettings.placeBias and MarkPlaceBias.SCAN in playSettings.placeBias:
			raise Exception("Mark place bias cannot be both RANDOM and SCAN!")

		self.playSettings: PlayerSettings = playSettings
		self.Board: Board = Board(self.playSettings.board_size)
		self.result: GameResult = GameResult()
		self.zeroes: list[tuple[int,int]] = []
		self.positionsToCheck: list[tuple[int,int]] = []
		self.result.BoardSize = self.Board.Size

		corners: list[tuple[int,int]] = [
			(1,1),
			(self.playSettings.board_size-2,self.playSettings.board_size-2),
			(1,self.playSettings.board_size-2),
			(self.playSettings.board_size-2,1),
		]
		
		for x in range(self.playSettings.board_size):
			for y in range(self.playSettings.board_size):
				if MarkPlaceBias.CORNERS_FIRST in self.playSettings.placeBias and (x,y) in corners:
					continue
				self.positionsToCheck.append((x,y))

		if MarkPlaceBias.RANDOM in self.playSettings.placeBias:
			random.shuffle(self.positionsToCheck)
		
		if MarkPlaceBias.CORNERS_FIRST in self.playSettings.placeBias:
			for c in corners.__reversed__():
				self.positionsToCheck.insert(0,c)
	def __iter__(self):
		return self
	def __next__(self) -> GameResult:
		amount, sum = self.dicesRoll()
		if not self.playHand(amount,sum):
			raise StopIteration
		return self.result
	def playHand(self,amountToPlace: int, sumToPlace: int) -> bool:
		if len(self.zeroes) > 0:
			#print(f"Zeroes found: {self.zeroes}")
			self.result.EndZeroes += len(self.zeroes)
			if MarkPlaceBias.ZEROES_FIRST in self.playSettings.placeBias:
				for zero in self.zeroes:
					self.positionsToCheck.remove(zero)
					self.positionsToCheck.insert(0,zero)
			self.zeroes.clear()
		
		for c_pos in self.positionsToCheck:
			x=c_pos[0]
			y=c_pos[1]
			if self.canPlaceOnBoard(x,y,amountToPlace,sumToPlace):
				cell_under: Cell = self.Board.get(x,y)
				comp = self.composite(sumToPlace,amountToPlace)
				self.result.Sum += sumToPlace
				self.result.Marks += 1
				self.result.Filled += amountToPlace
				comp = self.arrangeComposite(x,y,comp)
				if 0 in comp:
					for (index, element) in enumerate(comp):
						if element == 0:
							curr_offset = pos[index]
							self.zeroes.append((curr_offset[0]+x,curr_offset[1]+y))
				#print(f"Placing at ({x},{y})"+(" (zero)" if cell_under.Type==CellType.ZERO else ""))
				if cell_under.Type == CellType.ZERO:
					self.result.EndZeroes -= 1
				else:
					self.result.Filled += 1
				self.Board.placeMark(x,y,comp)
				self.positionsToCheck.remove((x,y))
				self.result.Score = self.Board.getScore()
				return True
		return False
	def canPlaceOnBoard(self,x: int,y: int, count: int, sum: int) -> bool:
		type = self.Board.get(x,y).Type
		if type != CellType.EMPTY and type != CellType.ZERO:
			return False
		nSum: int   = 0
		potential_cells: int = 8

		for offset in pos:
			curr_pos: tuple[int, int] = x+offset[0],y+offset[1]
			if not self.Board.isInBounds(curr_pos[0],curr_pos[1]):
				potential_cells-=1
				continue
			cell: Cell = self.Board.get(curr_pos[0],curr_pos[1])
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

	def getMissingSum(self,x: int,y: int, sum: int) -> int:
		return sum - self.Board.getNeigbourSum(x,y)

	def getMissingCount(self,x: int,y: int, count: int) -> int:
		return count - self.Board.getNeigbourCount(x,y)

	# Create list of (amount) of numbers, with the total sum of (number)
	def composite(self,number: int, amount: int) -> list[int]:
		
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
		#print(f"Compositing {number} with {amount} numbers, by: {result}")
		return result

	# returns (amount, sum)
	def dicesRoll(self)-> tuple[int,int]:
		return (random.randrange(1,9),random.randrange(1,self.playSettings.maxSum))

	def arrangeComposite(self,x:int, y:int, _arr: list[int])-> list[int | None]:
		arr: list[int|None] = [None]*8
		leftToArrange: list[int] = _arr.copy()
		offsets: list[tuple[int,tuple[int,int]]] = [(index,pos) for (index, pos) in enumerate(pos.copy())]
		random.shuffle(leftToArrange)
		random.shuffle(offsets)
		while len(leftToArrange) > 0:
			new_index: int = -1
			for offset in offsets:
				potential_pos: tuple[int, int] = x+offset[1][0],y+offset[1][1]
				if arr[offset[0]] != None or not self.Board.isInBounds(potential_pos[0],potential_pos[1]) or self.Board.get(potential_pos[0],potential_pos[1]).Type != CellType.EMPTY:
					continue
				new_index = offset[0]
				break
			else:
				raise Exception(f"No room left for placing! Left in array: {leftToArrange}")
			arr[new_index] = leftToArrange.pop()
		return arr