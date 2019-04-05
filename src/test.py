from lexpy.dawg import DAWG
from constants import WORDS
from datetime import datetime


row = ['','', 'A', '', '', '', 'O', '', '', 'Z', '']

row_copy = row[:]



# loop
# parts = []
# last_split = 0
# for i in range(len(row)):
#     letter = row[i]
#     if letter == '':
#         parts.append(row_copy[last_split:i + 1])
#         last_split = i


# print(parts)


# Getting possible words
dawg = DAWG()

dawg.add_all(WORDS)
dawg.reduce()
print('Done optimizing')

rack = ['P', 'P', 'L', 'E', 'B', 'G', 'Z'] + ['A']


start_time = datetime.utcnow()

possible_words = dawg.search('*A**')

check_words = []
for word in possible_words:
    add = True
    if len(word) > len('*A**'):
        continue
    for letter in word:
        if letter not in rack or word.count(letter) > rack.count(letter):
            add = False
            break
    if add:
        check_words.append(word)

end_time = datetime.utcnow()


print(check_words)
print(end_time - start_time)
