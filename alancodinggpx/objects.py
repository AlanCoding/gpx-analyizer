import re
from datetime import datetime

class Point(object):
	time = None
	speed = None
	course = None
	elevation = None
	lat = None
	lon = None

	def __init__(self, full_string):
		time = self.extract_field(full_string, 'time')
		self.time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
		speed = self.extract_field(full_string, 'speed')
		self.speed = float(speed) if type(speed) is str else None
		course = self.extract_field(full_string, 'course')
		self.course = float(course) if type(course) is str else None
		self.elevation = float(self.extract_field(full_string, 'ele'))
		(self.lat, self.lon) = self.extract_cords(full_string)

	def extract_field(self, full_string, name):
		prefix = ''
		if name in ('TrackPointExtension', 'speed', 'course'):
			prefix = 'gpxtpx:'
		pattern = '\<' + prefix + name + '\>(?P<guts>.*?)\<\/' + prefix + name + '\>'
		finds = re.findall(pattern, full_string)
		if len(finds) != 1:
			if name == 'time' or name == 'ele':
				raise Exception(str(len(finds)) + ' duplicate fields found for '+name)
			else:
				return None
		return finds[0]

	def extract_cords(self, full_string):
		pattern = re.compile('\<trkpt\slat="(?P<lat>-?[0-9]+\.[0-9]+)"\slon="(?P<lon>-?[0-9]+\.[0-9]+)"\>')
		match = pattern.match(full_string)
		lat = match.group('lat')
		lon = match.group('lon')
		if lat is None or lon is None:
			raise Exception('Lattitude and longitude for point not found')
		return (lat, lon)
