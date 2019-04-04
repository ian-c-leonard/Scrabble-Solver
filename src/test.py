from lexpy.dawg import DAWG
from constants import WORDS
from datetime import datetime

row = ['', '', 'A', 'R', 'C', '', '' , '', '', 'B', '', 'C', 'A', '', '', '']

# start_indices = [0, 1, 2, 4, 5, 6 9, 10]
# end_indices = [2, 3, 4, 7, 8, 10, 11, 12, 13]

row_copy = row[:]

start = [0]
end = []
have_seen_letter = False
for i in range(1, len(row_copy) - 1):
    letter = row_copy[i]
    if letter != '':
        have_seen_letter = True
    if letter == '' and row_copy[i - 1] == '':
        start.append(i)
        have_seen_letter = False
    if letter != '' and row_copy[i - 1] == '':
        start.append(i)

    if letter != '' and row_copy[i + 1] == '':
        end.append(i)
    if letter == '' and ((i - 1) in end) and row_copy[i + 1] == '':
        end.append(i)
    # if letter == '' and row_copy[i + 1] == '' and have_seen_letter:
    #     end.append(i)

print(start)
end.append(len(row_copy) - 1)
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
