
from sys import argv
from player import GamePlayer, MarkPlaceBias, PlayerSettings

gameCount: int = int(argv[1])
playSettings: PlayerSettings = PlayerSettings(
	board_size=7,
	place_bias=MarkPlaceBias.ZEROES_FIRST | MarkPlaceBias.SCAN | MarkPlaceBias.FILL_FIRST_THEN_JOIN
)

print(f"Game count: {gameCount}")
print(playSettings)
scoreSum: float = 0
markSum: float = 0
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
	markSum += player.result.Marks
	if i - lastChecked >= r:
		lastChecked = i
		p: int = int((i/gameCount)*100)
		print(f"progress: {p}% ({i} out of {gameCount})")
	scoreSum += player.result.Score 
	#print(f"Game {i+1} ended with score {player.result.Score}")
	#print(player.Board)
print(f"Game average score: {scoreSum/gameCount}")
print(f"Game average mark sum: {markSum/gameCount}")
print("Free cells per hand:")
for hand_index in freeCellsSum.keys():
	print(f"{hand_index} -> {freeCellsSum[hand_index]/gameCount}")
print("Marks per hand:")
for hand_index in markSumPerHand.keys():
	print(f"{hand_index} -> {markSumPerHand[hand_index]/gameCount}")