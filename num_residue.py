f = open("pqrse.pdb", "r")
lookup = set()

for x in f:
	line = x.split()
	if line[3] != 'HOH':
		lookup.add(line[3] + line[4] + line[5])

print(len(lookup))
print(lookup)







