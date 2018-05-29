from itertools import combinations
from sendInput import KEY_MAP

def createInputVector():
	keys = list(KEY_MAP.keys())
	keys.remove('esc')
	keys.remove('enter')
	
	inputVector = []
	for k in range(0, len(keys)+1):
		for subset in combinations(keys,k):
			inputVector.append(";".join(str(i) for i in subset))

	print(inputVector)
	print(len(inputVector))

createInputVector()
