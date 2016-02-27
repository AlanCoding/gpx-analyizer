import copy
import sys


class TopAttributes(object):
	fields = ['speed_calc', 'speed', 'acceleration_calc', 'dist', 'elevation']
	seconds_tol = 3600
	top_vals = None
	low_vals = None
	N = 20
	
	def __init__(self):
		self.top_vals = {}
		for fd in self.fields:
			self.top_vals[fd] = [None for i in range(self.N)]
		self.low_vals = {}
		for fd in self.fields:
			self.low_vals[fd] = [None for i in range(self.N)]
		
	def update(self, point):
		for fd in self.fields:
			the_val = getattr(point, fd)
			if not type(the_val) is float:
				continue
			for i in range(self.N):
				# Enter the point in the contest for highest values
				if self.top_vals[fd][i] is None:
					self.top_vals[fd][i] = copy.copy(point)
				elif the_val > getattr(self.top_vals[fd][i], fd):
					if self.not_same_time(point, self.top_vals[fd], i):
						self.top_vals[fd][i] = copy.copy(point)
				# Now enter the point in the contest for lowest values
				if self.low_vals[fd][i] is None:
					self.low_vals[fd][i] = copy.copy(point)
				elif the_val < getattr(self.low_vals[fd][i], fd):
					if self.not_same_time(point, self.low_vals[fd], i):
						self.low_vals[fd][i] = copy.copy(point)
		return True

	def not_same_time(self, point, top_list, i):
		for k in range(self.N):
			if i == k:
				continue
			if top_list[k] is not None and point.delta_time(top_list[k]) < self.seconds_tol:
				return False
		return True
		
	def display(self):
		sys.stdout.write("-- Display of the highest//lowest of ... --\n")
		sys.stdout.write("    " + " ".join(self.fields) + "\n")
		for fd in self.fields:
			sys.stdout.write("\nTop " + str(self.N) + str(fd) + " reached:\n")
			self.top_vals[fd].sort(key=lambda p: getattr(p, fd), reverse=True)
			for pt in self.top_vals[fd]:
				self.point_print(pt, fd)
			sys.stdout.write("\nLowest " + str(self.N) + " reached\n")
			self.low_vals[fd].sort(key=lambda p: getattr(p, fd), reverse=False)
			for pt in self.low_vals[fd]:
				self.point_print(pt, fd)
				
	def point_print(self, pt, fd):
		sys.stdout.write(pt.full_print())
		the_val = getattr(pt, fd)
		if 'speed' in fd:
			the_val = the_val * 2.23694  # Convert speeds m/s -> mph
		sys.stdout.write(' ' + fd + ': ' + str(the_val) + '\n')


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
	hist_delta = 1
	hist_max_width = 75
	shist = None
	hist_dict = None
	
	def __init__(self):
		hist_bins = 100
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