
from collector import AverageCollector, MinMaxCollector
from sys import argv
from player import GamePlayer, MarkPlaceBias, PlayerSettings

gameCount: int = int(argv[1])
playSettings: PlayerSettings = PlayerSettings(
	board_size=7,
	place_bias= MarkPlaceBias.RANDOM
)

print(f"Game count: {gameCount}")
print(playSettings)

collectors: list[AverageCollector | MinMaxCollector] = [
    AverageCollector(lambda r: r.Sum, "sum"),
    AverageCollector(lambda r: r.Score, "score"),
    AverageCollector(lambda r: r.Marks, "marks"),
    MinMaxCollector(lambda r: r.Sum, "sum"),
    MinMaxCollector(lambda r: r.Score, "score"),
    MinMaxCollector(lambda r: r.Marks, "marks"),
]

markSumPerHand: dict[int,int] = {}
freeCellsSum: dict[int,int] = {}
lastChecked: int = 0

reportFrequency: float = 0.99 

r: int = int(gameCount * (1-reportFrequency))
for i in range(gameCount):
	player: GamePlayer = GamePlayer(playSettings)
	freeCells: int = 0
	for hand_index, hand in enumerate(player):
		if not hand_index in markSumPerHand:
			markSumPerHand[hand_index] = 0
		if not hand_index in freeCellsSum:
			freeCellsSum[hand_index] = 0
		markSumPerHand[hand_index] += hand.Marks
		freeCellsSum[hand_index] += (playSettings.board_size*playSettings.board_size - hand.Filled)
	for collector in collectors:
		if isinstance(collector, AverageCollector):
			collector.update(player.result)
		else:
			collector.try_result(player.Board, player.result)
	if i - lastChecked >= r:
		lastChecked = i
		p: int = int((i/gameCount)*100)
		print(f"\rprogress: {p}% ({i} out of {gameCount})",end="")
	#print(f"Game {i+1} ended with score {player.result.Score}")
	#print(player.Board)
print()
for collector in collectors:
    collector.report()
print("Free cells per hand:")
for hand_index in freeCellsSum.keys():
	print(f"{hand_index} -> {freeCellsSum[hand_index]/gameCount}")
print("Marks per hand:")
for hand_index in markSumPerHand.keys():
	print(f"{hand_index} -> {markSumPerHand[hand_index]/gameCount}")