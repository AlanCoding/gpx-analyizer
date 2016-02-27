import re


def extract_field(full_string, name):
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


def extract_cords(full_string):
	pattern = re.compile('\<trkpt\slat="(?P<lat>-?[0-9]+\.[0-9]+)"\slon="(?P<lon>-?[0-9]+\.[0-9]+)"\>')
	match = pattern.match(full_string)
	lat = match.group('lat')
	lon = match.group('lon')
	if lat is None or lon is None:
		raise Exception('Lattitude and longitude for point not found')
	return (float(lat), float(lon))
	

