import os
import re
import sys
from datetime import datetime
from alancodinggpx.objects import Point

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
		try:
			pt = Point(ptxt)
		except Exception as ex:
			print('')
			print('Failed on point # ' + str(i))
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
	print(str(round(k*2.23694,2)).ljust(7) + '#' * int(hist_dict[k] * hist_max_width / hist_max) +
		'   ' + str(hist_dict[k]))

print('')
# print('sorted values: ' + str(sorted(hist_dict.keys())))
