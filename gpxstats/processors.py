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
			if self.top_vals[fd][-1] is None or the_val > getattr(self.top_vals[fd][-1], fd):
				for i in range(self.N):
					# Enter the point in the contest for highest values
					incumbent = self.top_vals[fd][i]
					if incumbent is None or the_val > getattr(incumbent, fd):
						if self.not_same_time(point, self.top_vals[fd], i):
							self.bump_insert(self.top_vals[fd], copy.copy(point), i)
							# self.top_vals[fd][i] = copy.copy(point)
						else:
							break
			if self.low_vals[fd][-1] is None or the_val < getattr(self.low_vals[fd][-1], fd):
				for i in range(self.N):
					# Now enter the point in the contest for lowest values
					incumbent = self.low_vals[fd][i]
					if incumbent is None or the_val < getattr(incumbent, fd):
						if self.not_same_time(point, self.low_vals[fd], i):
							self.bump_insert(self.low_vals[fd], copy.copy(point), i)
							# self.low_vals[fd][i] = copy.copy(point)
						else:
							break
		return True

	def bump_insert(self, array, value, i):
		array[i+1:] = array[i:-1]
		array[i] = value

	def not_same_time(self, point, top_list, i):
		if top_list[i] is None:
			return True
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
			# self.top_vals[fd].sort(key=lambda p: getattr(p, fd), reverse=True)
			for pt in self.top_vals[fd]:
				self.point_print(pt, fd)
			sys.stdout.write("\nLowest " + str(self.N) + " reached\n")
			# self.low_vals[fd].sort(key=lambda p: getattr(p, fd), reverse=False)
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
		sys.stdout.write("Print first 100 points\n")
		
	def update(self, point):
		if self.i < 100:
			sys.stdout.write(point.full_print() + '\n')
		elif self.i == 100:
			sys.stdout.write('\n')  # line break
		self.i += 1
	
	def display(self):
		pass


class AttributeHistogram(object):
	fields = ['speed_calc', 'acceleration_calc', 'dist', 'elevation']
	# Size of the histogram to chop it up by
	deltas = dict(
		speed_calc = 1.,
		acceleration_calc = 0.01,
		dist = 5.,
		elevation = 10.
	)
	# Minimum values to accept
	mins = dict(
		speed_calc = 0.,
		acceleration_calc = -0.5,
		dist = 0.,
		elevation = 0.
	)
	hist_array = None
	overs = None
	unders = None
	# Number of points to store
	N = 75

	def __init__(self):
		self.hist_array = {}
		self.unders = {}
		self.overs = {}
		for fd in self.fields:
			self.hist_array[fd] = [0 for i in range(self.N)]
			self.overs[fd] = 0
			self.unders[fd] = 0

	def update(self, point):
		for fd in self.fields:
			the_val = getattr(point, fd)
			if not type(the_val) is float:
				continue
			place = int((the_val - self.mins[fd])/self.deltas[fd])
			if place < 0:
				self.unders[fd] += 1
				continue
			if place >= self.N:
				self.overs[fd] += 1
				continue
			self.hist_array[fd][place] += 1

	def display(self):
		for fd in self.fields:
			sys.stdout.write('\n\n%s histogram:\n' % fd)
			sys.stdout.write(' total sample points= ' + str(sum(self.hist_array[fd])) + '\n')
			sys.stdout.write(
				'  samples_over= ' + str(self.overs[fd]) + 
				'  samples_under= ' + str(self.unders[fd]) + '\n'
			)

			sys.stdout.write('upper_bound      frequency\n')
			hist_max = max(self.hist_array[fd])
			for k in range(self.N):
				if 'speed' in fd:
					key_print = k*2.23694
				else:
					key_print = k
				key_print = key_print * self.deltas[fd]
				sys.stdout.write(
					str(round(key_print,2)).ljust(7) +
					'#' * int(self.hist_array[fd][k] * self.N / hist_max) +
					'   ' + str(self.hist_array[fd][k]) + '\n'
				)

			sys.stdout.write('\n')


# TODO: Processor to store an array of stops and their statistics

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
		
		sys.stdout.write('\nSpeed histogram:\n')
		sys.stdout.write(' total sample points= ' + str(sum(self.shist)) + '\n')

		sys.stdout.write('upper_bound      frequency\n')
		hist_max = max(self.hist_dict.values())
		for k in sorted(self.hist_dict.keys()):
			sys.stdout.write(str(round(k*2.23694,2)).ljust(7) + '#' * int(self.hist_dict[k] * self.hist_max_width / hist_max) +
				'   ' + str(self.hist_dict[k]) + '\n')

		sys.stdout.write('\n')