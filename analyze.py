# import os
import re
import sys
import itertools
from datetime import datetime
from alancodinggpx.objects import Archive, Analyzer

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

analyzer = Analyzer(cache=False)
analyzer.go()
