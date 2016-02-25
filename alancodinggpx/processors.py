import copy


class TopSpeeds(object):
	high_speeds = None
	
	def __init__(self):
		self.high_speeds = [None for i in range(5)]
		
	def update(self, point):
		the_speed = point.calc_speed()
		if not type(the_speed) is float:
			return False
		for i in range(5):
			if not type(self.high_speeds[i]) is float or the_speed > self.high_speeds[i].calc_speed():
				self.high_speeds[i] = copy.copy(point)
				return True
		return False
		
	def display(self):
		print("Top 5 speeds reached:")
		for pt in self.high_speeds:
			print(pt.full_print())
	
class PrintFirst100(object):
	i = None
	
	def __init__(self):
		self.i = 0
		print("Print first 100 points")
		
	def update(self, point):
		if self.i < 100:
			print(point.full_print())
		elif self.i == 100:
			print('')  # line break
		self.i += 1
	
	def display(self):
		pass