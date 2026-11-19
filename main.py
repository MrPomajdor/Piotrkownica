
from player import GamePlayer, MarkPlaceBias, PlayerSettings

scoreSum: float = 0
gameCount: int = 10000
playSettings: PlayerSettings = PlayerSettings(
	board_size=7,
	placeBias=MarkPlaceBias.TOP_LEFT_TO_RIGHT,
	priotitizeZeroes=True
)

print(f"Game count: {gameCount}")
print(playSettings)
lastChecked: int = 0
reportFrequency: float = 0.8
r: int = int(gameCount * (1-reportFrequency))
for i in range(gameCount):
	player: GamePlayer = GamePlayer(playSettings)
	for hand in player:
		# (hand played)
		pass
	if i - lastChecked >= r:
		lastChecked = i
		p: int = int((i/gameCount)*100)
		print(f"progress: {p}% ({i} out of {gameCount})")
	scoreSum += player.result.Score 
	#print(f"Game {i+1} ended with score {player.result.Score}")
	#print(player.Board)
print(f"Game average score: {scoreSum/gameCount}")