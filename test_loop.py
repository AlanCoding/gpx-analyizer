from alancodinggpx.objects import Archive
import itertools

from alancodinggpx import processors

for p_str in [p for p in dir(processors) if not p.startswith('__')]:
	RealClass = getattr(processors, p_str)
	objt = RealClass()
	objt.hi_mom()

# Put your gpx archive files in the archive directory
archive = Archive('archive/', cache=False)
print('\n')
print(str(archive))

print('\nFiles found in archive folder:')
print(' '.join(archive.filelist) + '\n')

i = 0
N = 7
print('First ' + str(N) + ' items in file list\n')
for pt in itertools.islice(archive, N):
	if i > 0:
		print('time diff:    ' + str((pt.time - pt_last.time).total_seconds()) + ' seconds')
		print('meters moved: ' + str(pt.dist()))
		print('speed, calc: ' + str(round(pt.calc_speed(),2)) + ' given: ' + str(pt.speed))
		a = pt.calc_acceleration()
		if a is not None:
			print('acc calc:    ' + str(round(a, 5)))
	pt_last = pt
	i += 1
	print(str(pt))
	print('cords: ' + str(pt.cord))
	print('')