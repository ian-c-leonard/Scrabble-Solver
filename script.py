from constants import WORDS

filename = "dictionary.py"

score_map = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
                       'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 
                       'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 
                       'Y': 4, 'Z': 10, 'BLANK': 0}

dictionary = {}

for word in WORDS:
	score = 0
	for letter in word:
		score += score_map[letter]
	dictionary[word] = score



with open('dictionary.py', 'w') as f:
    print('dictionary:', dictionary, file=f)  # Python 3.x