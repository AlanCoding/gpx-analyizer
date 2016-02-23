from alancodinggpx.objects import Archive, Analyzer

# Cycle through entire data
print('Testing entirity of the files:')

analyzer = Analyzer(cache=False)
analyzer.go()
