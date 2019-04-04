from lexpy.dawg import DAWG
from constants import WORDS





# Getting possible words
# dawg = DAWG()

# dawg.add_all(WORDS)
# dawg.reduce()
# print('Done optimizing')

# rack = ['P', 'P', 'L', 'E', 'B', 'G', 'Z'] + ['A']

# possible_words = dawg.search('A*******')

# check_words = []
# for word in possible_words:
#     add = True
#     for letter in word:
#         if letter not in rack or word.count(letter) > rack.count(letter):
#             add = False
#             break
#     if add:
#         check_words.append(word)

# print(check_words)
