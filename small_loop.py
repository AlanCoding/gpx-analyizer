from alancodinggpx.objects import Archive
import itertools

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
	print(pt.full_print())
	if i > 0:
		print('time diff:    ' + str((pt.time - pt_last.time).total_seconds()) + ' seconds')
		a = pt.acceleration_calc
		if a is not None:
			print('acc calc:    ' + str(round(a, 5)))
	pt_last = pt
	i += 1
	print('')