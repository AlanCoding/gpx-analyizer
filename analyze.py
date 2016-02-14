import os
import re
import sys
from datetime import datetime

class Point(object):
	full_string = None
	time = None
	speed = None
	course = None
	elevation = None
	lat = None
	lon = None

	def __init__(self, stx):
		self.full_string = stx

	def store_fields(self):
		time = pt.extract_field('time')
		self.time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
		speed = pt.extract_field('speed')
		self.speed = float(speed) if type(speed) is str else None
		course = pt.extract_field('course')
		self.course = float(course) if type(course) is str else None
		self.elevation = float(pt.extract_field('ele'))
		(self.lat, self.lon) = pt.extract_cords()

	def extract_field(self, name):
		prefix = ''
		if name in ('TrackPointExtension', 'speed', 'course'):
			prefix = 'gpxtpx:'
		pattern = '\<' + prefix + name + '\>(?P<guts>.*?)\<\/' + prefix + name + '\>'
		finds = re.findall(pattern, self.full_string)
		if len(finds) != 1:
			if name == 'time' or name == 'ele':
				raise Exception(str(len(finds)) + ' duplicate fields found for '+name)
			else:
				return None
		return finds[0]

	def extract_cords(self):
		pattern = re.compile('\<trkpt\slat="(?P<lat>-?[0-9]+\.[0-9]+)"\slon="(?P<lon>-?[0-9]+\.[0-9]+)"\>')
		match = pattern.match(self.full_string)
		lat = match.group('lat')
		lon = match.group('lon')
		if lat is None or lon is None:
			raise Exception('Lattitude and longitude for point not found')
		return (lat, lon)


# Put your gpx archive files in the archive directory
cwd = os.getcwd()
archive_dir = os.path.join(cwd, 'archive/')
filelist = os.listdir(archive_dir)

# Sort file list numerically, not alphabetically
filelist = sorted(filelist, key=lambda x: float(x[:-4]))

print('\nFiles found in archive folder:')
print(' '.join(filelist) + '\n')

filename = filelist[0]

with open(os.path.join(archive_dir, filename), 'r') as f:
	full_file = f.read()

pattern = '(?P<trkpt>\<trkpt.*?\/trkpt\>)'

points = re.findall(pattern, full_file)

print(' Number of points in set: '+str(len(points)))
print('')

print('Example:')
for i in range(2):
	print(points[i])
	pt = Point(points[i])
	pt.store_fields()
	print("time: "+str(pt.time))
	if i > 0:
		print('time diff: ' + str(pt.time - t_last))
	t_last = pt.time
	print("speed: "+pt.extract_field('speed'))
	print("course: "+pt.extract_field('course'))
	print('cords: ' + str(pt.extract_cords()))
	print('speed times 5 ' + str(pt.speed>1))
	print('')

# Cycle through entire data
print('Testing entirity of the files:')

hist_bins = 100
hist_delta = 1
hist_max_width = 75
shist = [0 for i in range(hist_bins)]

hist_dict = {}

sys.stdout.write('filenames: ')
sys.stdout.flush()
for filename in filelist:
	sys.stdout.write(' ' + filename)
	sys.stdout.flush()
	with open(os.path.join(archive_dir, filename), 'r') as f:
		full_file = f.read()

	points = re.findall(pattern, full_file)

	i = 0
	for ptxt in points:
		i += 1
		pt = Point(ptxt)
		try:
			pt.store_fields()
		except Exception as ex:
			print('')
			print('Failed on point # ' + str(i))
			print('time: ' + str(pt.time) + ' elevation: ' + str(pt.elevation) + ' course: ' + str(pt.course))
			print('Text: ' + ptxt)
			print(ex)

		if i > 1:
			if pt.speed is not None:
				shist[int(pt.speed/hist_delta)] += 1
				if pt.speed not in hist_dict:
					hist_dict[pt.speed] = 1
				else:
					hist_dict[pt.speed] += 1

		last = pt

print('\n')
print('Speed histogram:')
print(' total sample points= ' + str(sum(shist)))
# shist = [hist_max_width * s / max(shist) for s in shist]
# for i in range(hist_bins):
# 	print((str(hist_delta*(i-1)) + '-to-' + str(hist_delta*i)).ljust(9) + '#' * int(shist[i]))

print('upper_bound      frequency')
hist_max = max(hist_dict.values())
for k in sorted(hist_dict.keys()):
	print(str(round(k*2.23694,4)).ljust(8) + '#' * int(hist_dict[k] * hist_max_width / hist_max) +
		'   ' + hist_dict[k])

print('')
# print('sorted values: ' + str(sorted(hist_dict.keys())))
