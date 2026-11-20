from game import Board
from player import GameResult
from typing import Callable

class AverageCollector:
    def __init__(self, extractor: Callable[[GameResult],float], name:str = "unnamed"):
        self.extractor: Callable[[GameResult],float] = extractor
        self.name: str = name
        self.sum: float = 0
        self.count: int = 0
        
    def update(self, result: GameResult) -> None:
        self.sum += self.extractor(result)
        self.count += 1

    def report(self):
        print(f"Average amount of '{self.name}' : {self.sum/float(self.count)}")

class MinMaxCollector:
    def __init__(self, extractor: Callable[[GameResult],float], name:str = "unnamed"):
        self.extractor: Callable[[GameResult],float] = extractor
        self.captured_board_min: Board | None = None
        self.captured_board_max: Board | None = None
        self.name: str = name
        self.minVal: float = float('inf')
        self.maxVal: float = float('-inf')

    def try_result(self, board: Board, result: GameResult) -> None:
        val: float = self.extractor(result)
        if val > self.maxVal:
            self.maxVal = val
            self.captured_board_max = board
        if val < self.minVal:
            self.minVal = val
            self.captured_board_min = board

    def report(self):
        if self.captured_board_min or self.captured_board_max:
            if self.captured_board_min:
                print(f"Min value of '{self.name}' : {self.minVal}")
                print(self.captured_board_min)
            else:
                print(f"No min value of '{self.name}' found")
            
            if self.captured_board_max:
                print(f"Max value of '{self.name}' : {self.maxVal}")
                print(self.captured_board_max)
            else:
                print(f"No max value of '{self.name}' found")
        else:
            print(f"No captured result for '{self.name}'")