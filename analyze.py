# import os
import re
import sys
import itertools
from datetime import datetime
from alancodinggpx.objects import Archive

# Put your gpx archive files in the archive directory
archive = Archive('archive/', cache=False)
print('\n')
print(str(archive))

print('\nFiles found in archive folder:')
print(' '.join(archive.filelist) + '\n')

i = 0
print('First 3 items in file list\n')
for pt in itertools.islice(archive, 3):
	if i > 0:
		print('time diff:    ' + str((pt.time - pt_last.time).total_seconds()) + ' seconds')
		print('meters moved: ' + str(pt.dist(pt_last)))
		print('speed, calc: ' + str(round(pt.calc_speed(pt_last),2)) + ' given: ' + str(pt.speed))
	pt_last = pt
	i += 1
	print('point: '+str(pt))
	print('cords: ' + str(pt.cord))
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
	if i < 100:
		print(str(pt))

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

print('upper_bound      frequency')
hist_max = max(hist_dict.values())
for k in sorted(hist_dict.keys()):
	print(str(round(k*2.23694,2)).ljust(7) + '#' * int(hist_dict[k] * hist_max_width / hist_max) +
		'   ' + str(hist_dict[k]))

print('')
# print('sorted values: ' + str(sorted(hist_dict.keys())))
