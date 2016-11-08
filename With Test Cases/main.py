import extract_answers as e
import normalize as n

test = range(4, 37)
defective = [8,15,16,17,19,20,26]

for i in test:
	if not i in defective:
		n.normalize(str(i))
		e.extract(str(i))