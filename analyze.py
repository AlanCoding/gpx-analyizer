# import os
import re
import sys
import itertools
from datetime import datetime
from alancodinggpx.objects import Point, Archive

# Put your gpx archive files in the archive directory
archive = Archive('archive/')

print('\nFiles found in archive folder:')
print(' '.join(archive.filelist) + '\n')

i = 0
print('First 3 items in file list\n')
for pt in itertools.islice(archive, 3):
	print("time: "+str(pt.time))
	if i > 0:
		print('time diff:    ' + str(pt.time - pt_last.time))
		print('meters moved: ' + str(pt.dist(pt_last)))
		print('calc speed:   ' + str(pt.calc_speed(pt_last)))
	pt_last = pt
	i += 1
	print("speed: "+str(pt.speed))
	print("course: "+str(pt.course))
	print('cords: ' + str((pt.lat, pt.lon)))
	print('speed times 5 ' + str(pt.speed>1))
	print('')


# Cycle through entire data
print('Testing entirity of the files:')

hist_bins = 100
hist_delta = 1
hist_max_width = 75
shist = [0 for i in range(hist_bins)]

hist_dict = {}

i = 0
for pt in archive:
	i += 1

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
