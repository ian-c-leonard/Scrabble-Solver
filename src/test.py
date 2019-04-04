from lexpy.dawg import DAWG
from constants import WORDS
from datetime import datetime

#      0    1   2    3   4   5   6    7    8   9  10   11  12  13
row = ['', '', 'A', '', '', '', 'G' ,'O', '', '', 'Z', '', '', '']

# start_indices = [0, 1, 2, 4, 5, 6 9, 10]
# end_indices = [2, 3, 4, 7, 8, 10, 11, 12, 13]

row_copy = row[:]

start = []
end = []
have_seen_letter = False
for i in range(row_copy):
    letter = row_copy[i]
    if letter = '' and not have_seen_letter:
        start.append(i)
        have_seen_letter = False
    if letter != '':
        have_seen_letter = True

print(start)
print(end)




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
# dawg = DAWG()

# dawg.add_all(WORDS)
# dawg.reduce()
# print('Done optimizing')

# rack = ['P', 'P', 'L', 'E', 'B', 'G', 'Z'] + ['A']


# start_time = datetime.utcnow()

# possible_words = dawg.search('*A**')

# check_words = []
# for word in possible_words:
#     add = True
#     if len(word) > len('*A**'):
#         continue
#     for letter in word:
#         if letter not in rack or word.count(letter) > rack.count(letter):
#             add = False
#             break
#     if add:
#         check_words.append(word)

# end_time = datetime.utcnow()


# print(check_words)
# print(end_time - start_time)
