import re
import os
# import pickle
import sqlite3
from datetime import datetime
from math import radians, cos, sin, asin, sqrt


class Coordinate(object):

	def __init__(self, lat, lon, ele):
		self.lon = lon
		self.lat = lat
		self.ele = ele

	def __str__(self):
		return '(la:' + str(self.lat) + ' lo:' + str(self.lon) + ' el:' + str(self.ele) + ')'

	def dist(self, c2):
		d_lon = c2.lon - self.lon
		d_lat = c2.lat - self.lat
		d_ele = c2.ele - self.ele

		lon_m = self.lon + d_lon * 0.5
		lat_m = self.lat + d_lat * 0.5
		ele_m = self.ele + d_ele * 0.5

		R = 6367000.0  # Radius of Earth in meters

		d1 = R * radians(d_lon) * cos( radians(lat_m) )
		d2 = R * radians(d_lat)
		return sqrt(d1**2 + d2**2 + d_ele**2)


class Point(object):
	time = None
	speed = None
	course = None
	cord = None

	def __init__(self, full_string):
		time = self.extract_field(full_string, 'time')
		self.time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
		speed = self.extract_field(full_string, 'speed')
		self.speed = float(speed) if type(speed) is str else None
		course = self.extract_field(full_string, 'course')
		self.course = float(course) if type(course) is str else None
		(lat, lon) = self.extract_cords(full_string)
		ele = float(self.extract_field(full_string, 'ele'))
		self.cord = Coordinate(lat, lon, ele)

	def __str__(self):
		if self.speed is None:
			return 'stopped at             ' + str(self.time)
		else:
			return 'moving ' + str(round(self.speed*2.23694,2)).ljust(5) + ' mph ' + str(self.cardnal()) + ' at ' + str(self.time)

	def cardnal(self):
		if self.course is None:
			return 'stationary'
		else:
			ang45 = (self.course + 45.) % 360.
			dirs = ['N', 'E', 'S', 'W']
			dint = int(ang45/90.)
			d = dirs[dint]
			ang_sm = ang45 % 90.
			if ang_sm < 90./3.:
				return dirs[dint] + dirs[(dint-1) % 4]
			elif ang_sm < 90.*2./3.:
				return dirs[dint].ljust(2)
			else:
				return (dirs[dint] + dirs[(dint-1) % 4]).ljust(2)

	def dist(self, p2):
		return self.cord.dist(p2.cord)

	def calc_speed(self, p2):
		distance = self.cord.dist(p2.cord)
		deltat = (self.time - p2.time).total_seconds()
		return distance / deltat

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
		return (float(lat), float(lon))


class Archive(object):
	filelist = None

	working_file = None
	working_file_index = None
	working_list = None
	working_list_index = None
	working_point_index = None

	point_list = None

	def __init__(self, path='archive/', save='save/tracks.db'):
		cwd = os.getcwd()
		save_dir = os.path.join(cwd, save)

		
		if os.path.isfile(save_dir):
			dest_filename = os.path.join(cwd, 'save/points_pickle.p')
			if os.path.isfile(dest_filename):
				self.point_list = pickle.load( open( dest_filename, "rb" ) )
				self.working_point_index = 0

		if path.startswith('/'):
			self.archive_dir = os.listdir(path)
		else:
			self.archive_dir = os.path.join(cwd, path)
		raw_filelist = os.listdir(self.archive_dir)

		filelist = []
		for f in raw_filelist:
			if len(f) > 4 and f[-4:] == '.gpx':
				filelist.append(f)

		# Sort file list numerically, not alphabetically
		self.filelist = sorted(filelist, key=lambda x: float(x[:-4]))

		if len(self.filelist) == 0:
			raise Exception('Did not find any gpx files in archive dir')

		if cache and self.point_list is None:
			pt_list = []
			for filename in self.filelist:
				patern_list = self.load_list_from_file(filename)
				for pattern in patern_list:
					pt_list.append(Point(pattern))
			self.point_list = pt_list
			dest_filename = os.path.join(cwd, 'save/points_pickle.p')
			pickle.dump(self.point_list, open(dest_filename, 'wb'))

		self.working_file_index = 0
		self.load_list_from_file(self.filelist[0])

	def __str__(self):
		return 'gpx archive with ' + str(len(self.filelist)) + ' files'

	def __iter__(self):
		return self

	def __next__(self):
		if self.point_list:
			if self.working_point_index > len(self.point_list):
				raise StopIteration
			return self.point_list[self.working_point_index]
			self.working_point_index += 1
		else:
			filename = self.filelist[self.working_file_index]
			if self.working_list_index >= len(self.working_list):
				if self.working_file_index >= len(self.filelist):
					raise StopIteration
				self.working_list = self.load_list_from_file(filename)
				self.working_file_index += 1
			pt = Point(self.working_list[self.working_list_index])
			self.working_list_index += 1
			return pt

	def load_list_from_file(self, filename):
		print('New file: ' + filename)
		with open(os.path.join(self.archive_dir, filename), 'r') as f:
			full_file = f.read()
		pattern = '(?P<trkpt>\<trkpt.*?\/trkpt\>)'
		self.working_list_index = 0
		return re.findall(pattern, full_file)
