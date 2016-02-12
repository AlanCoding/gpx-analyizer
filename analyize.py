import os
import re

class Point(object):

	def extract_field(name):
		p = '(?P<trkpt>\<trkpt.*?\/trkpt\>)'


# Put your gpx archive files in the archive directory
cwd = os.getcwd()
archive_dir = os.path.join(cwd, 'archive/')
filelist = os.listdir(archive_dir)

# Sort file list numerically, not alphabetically
filelist = sorted(filelist, key=lambda x: float(x[:-4]))


print(filelist)

filename = filelist[0]

with open(os.path.join(archive_dir, filename)) as f:
	full_file = f.read()

pattern = '(?P<trkpt>\<trkpt.*?\/trkpt\>)'

points = re.findall(pattern, full_file)

print(" Number of points in set: "+str(len(points)))
print("")

for i in range(3):
	print(points[i])
	print("")
