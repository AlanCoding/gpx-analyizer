import os
import re

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
		self.time = pt.extract_field('time')
		self.speed = pt.extract_field('speed')
		self.course = pt.extract_field('course')
		self.elevation = pt.extract_field('ele')
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

print(" Number of points in set: "+str(len(points)))
print("")

for i in range(3):
	print(points[i])
	pt = Point(points[i])
	print("time: "+pt.extract_field('time'))
	print("speed: "+pt.extract_field('speed'))
	print("course: "+pt.extract_field('course'))
	print('cords: ' + str(pt.extract_cords()))
	pt.store_fields()
	print('')

print('Testing entirity of the points:')
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
