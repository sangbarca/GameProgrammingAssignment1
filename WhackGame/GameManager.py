class GameManager(object):
	def __init__(self):
		self.num_of_enemy = 15
	#### PLAYER PERFORMANCE ####
	attack_count = 0
	hit_count = 0
	#### LEVEL DATA ############
	SPAWN_RATE = 0.3 # spawn per second
	DELAY_SPAWN = 20 # from 0 to 100

	# EX: SPAWN_RATE = 0.2
	# CALCULATE : 0.2 (20%) for each second -> 5s == 100 percent spawn
	# RATE = ElapseTime (ms) * SPAWN_RATE / 1000 x 100 (%)
	
	num_of_enemy = 0




	def smash(self):
		self.attack_count = self.attack_count + 1
	def hitEnemy(self):
		self.hit_count = self.hit_count + 1


instance = GameManager()