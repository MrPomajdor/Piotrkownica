import random
from enum import Enum
from typing import override
pos: list[tuple[int, int]] = [
            (-1,1),  (0,1), (1,1),
            (-1,0),          (1,0),
            (-1,-1), (0,-1), (1,-1),
        ]
class CellType(Enum):
        EMPTY = -1
        NUMBER = 0
        MARK = 1
        ZERO = 2
class Cell:
    Type: CellType = CellType.EMPTY
    num_val: int = 0
    def __init__(self, cell_type: CellType, num_value: int = 0) -> None:
        self.Type = cell_type
        if(self.Type == CellType.NUMBER):
            self.num_val = num_value
    def getValue(self) -> int:
        if(self.Type == CellType.NUMBER):
            return self.num_val
        else:
            raise Exception("Trying to read a value from a non-number cell!")
    @override
    def __str__(self) -> str:
        match(self.Type):
            case CellType.EMPTY:
                return " "
            case CellType.MARK:
                return "X"
            case CellType.NUMBER:
                return str(self.getValue())
            case CellType.ZERO:
                return "Z"
class Board:
    Cells: list[list[Cell]]    = []
    Size: int = 0
    def __init__(self, size: int):
        self.Size = size
        for y in range(size):
            self.Cells.append([])
            for _ in range(size):
                self.Cells[y].append(Cell(cell_type=CellType.EMPTY))
    def get(self,x: int, y: int) -> Cell:
        return self.Cells[y][x]
    def _set(self,x: int, y: int, type: CellType, val: int=0) -> None:
        self.Cells[y][x].Type = type
        self.Cells[y][x].num_val = val
        
    def getNeigbourCount(self, x: int, y: int) -> int:
        res: int = 0
        for oy in range(-1,2):
            if oy+y < 0 or oy+y > self.Size -1:
                continue
            for ox in range(-1,2):
                if ox+x < 0 or ox+x>self.Size - 1:
                    continue
                if self.Cells[ox+x][oy+y].Type != CellType.EMPTY:
                    res+=1
        return res
    def isInBounds(self, x: int,y: int) -> bool:
        return not (y < 0 or y > self.Size -1 or x < 0 or x>self.Size - 1)
    def getNeigbourSum(self, x: int, y: int) -> int:
        res: int = 0
        for oy in range(-1,2):
            if oy+y < 0 or oy+y > self.Size -1:
                continue
            for ox in range(-1,2):
                if ox+x < 0 or ox+x>self.Size - 1:
                    continue
                target: Cell = self.get(ox+x,oy-y)
                if target.Type == CellType.NUMBER:
                    res+=target.getValue()
        return res
    def place(self, x: int, y: int, type: CellType, num: int = 0) -> None:
        target: Cell = self.get(x,y)
        if target.Type == CellType.EMPTY:
            match(type):
                case CellType.NUMBER:
                    if num == 0:
                        self._set(x,y,type=CellType.ZERO)
                    else:
                        self._set(x,y,type=CellType.NUMBER,val=num)
                case CellType.MARK:
                    self._set(x,y,type=CellType.MARK)
                case CellType.ZERO:
                    self._set(x,y,type=CellType.ZERO)
                case _:
                    raise Exception(f"Invalid place type {type} to an empty cell at {x,y}")
            return
        else:
            if type==CellType.MARK and target.Type==CellType.ZERO:
                self._set(x,y,CellType.MARK)
            else:
                raise Exception(f"Trying to set a number to a non empty cell at ({x},{y})")
        
    # numbers array are arranged around the mark like:
    # [1][2][3]
    # [4][X][5]
    # [6][7][8]
    # 
    # Additionally, array element can be None, witch indicates the cell at that position is left unchanged. 
    def placeMark(self, x: int, y: int, numbers: list[int | None]) -> None:
        self.place(x,y,type=CellType.MARK)
        i: int = 0
        for curr in numbers:
            if curr == None:
                i+=1
                continue
            num_pos: tuple[int,int] = (x+pos[i][0],y+pos[i][1])
            self.place(x=num_pos[0],y=num_pos[1],type=CellType.NUMBER,num=curr)
            i+=1
    @override
    def __str__(self) -> str:
        res: str = "  "
        for x in range(self.Size):
            res += f"{x}  "
        res += "\n"
        for index, row in enumerate(self.Cells):
            res += str(index)
            for cell in row:
                res += f"[{str(cell)}]"
            res += "\n"
        return res

