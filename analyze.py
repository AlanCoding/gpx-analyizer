from gpxstats.objects import Archive, Analyzer
import sys

# Cycle through entire data
sys.stdout.write('Testing entirity of the files:\n')

analyzer = Analyzer(cache=False)
analyzer.go()
