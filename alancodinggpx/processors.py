import copy


class TopSpeeds(object):
	high_speeds = None
	
	def __init__(self):
		self.high_speeds = [None for i in range(5)]
		
	def update(self, point):
		the_speed = point.speed_calc
		if not type(the_speed) is float:
			return False
		for i in range(5):
			if self.high_speeds[i] is None:
				self.high_speeds[i] = copy.copy(point)
				return True
			if the_speed is not None and the_speed > self.high_speeds[i].speed_calc:
				self.high_speeds[i] = copy.copy(point)
				return True
		return False
		
	def display(self):
		print("Top 5 speeds reached:")
		for pt in self.high_speeds:
			print(pt.full_print())
			print('  calc_speed: ' + str(pt.speed_calc*2.23694))


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


class SpeedHistogram(object):
	hist_delta = None
	hist_max_width = None
	shist = None
	hist_dict = None
	
	def __init__(self):
		hist_bins = 100
		self.hist_delta = 1
		self.hist_max_width = 75
		self.shist = [0 for i in range(hist_bins)]

		self.hist_dict = {}
	
	def update(self, point):
		
		if point.speed is not None:
			self.shist[int(point.speed/self.hist_delta)] += 1
			if point.speed not in self.hist_dict:
				self.hist_dict[point.speed] = 1
			else:
				self.hist_dict[point.speed] += 1
		
	def display(self):
		
		print('\n')
		print('Speed histogram:')
		print(' total sample points= ' + str(sum(self.shist)))

		print('upper_bound      frequency')
		hist_max = max(self.hist_dict.values())
		for k in sorted(self.hist_dict.keys()):
			print(str(round(k*2.23694,2)).ljust(7) + '#' * int(self.hist_dict[k] * self.hist_max_width / hist_max) +
				'   ' + str(self.hist_dict[k]))

		print('')