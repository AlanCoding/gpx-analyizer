from alancodinggpx.objects import Archive
import itertools
import sys

# Put your gpx archive files in the archive directory
archive = Archive('archive/', cache=False)
sys.stdout.write(str(archive) + '\n\n')

sys.stdout.write('Files found in archive folder:\n')
sys.stdout.write(' '.join(archive.filelist) + '\n\n')

i = 0
N = 7
sys.stdout.write('First ' + str(N) + ' items in file list\n\n')
for pt in itertools.islice(archive, N):
	sys.stdout.write(pt.full_print())
	if i > 0:
		sys.stdout.write(
			'\n    time diff:    ' + 
			str(pt.delta_time(pt_last)) + ' seconds'
		)
		a = pt.acceleration_calc
		if a is not None:
			sys.stdout.write('    acc calc:    ' + str(round(a, 5)))
	sys.stdout.write('\n\n')
	pt_last = pt
	i += 1