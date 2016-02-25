def bump_insert(array, val):
	N = len(array)
	for i in range(N):
		if val > array[i]:
			for j in range(i+1, N):
				array[j] = array[j-1]
			array[i] = val
			return True
	return False

class TopSpeeds(object):
	high_speeds = None
	
	def __init__(self):
		self.high_speeds = [(None, 0) for i in range(5)]
		
	def update(self, point):
		the_speed = point.calc_speed()
		if the_speed < min(self.high_speeds):
			return False
		bump_insert(self.high_speeds, the_speed)
		
	def print(self):
	
class Object2(object):
	
	def hi_mom(self):
		print("hi mom!1")