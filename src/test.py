from lexpy.dawg import DAWG
from constants import WORDS
from datetime import datetime

# row = ['', '', 'A', 'R', 'C', '', '' , '', '', 'B', '', 'C', 'A', '', '', '']
# row = ['A', '', '', '', 'B', '', 'C', '', 'D', 'E', 'F', 'G', '', '', 'H', '', 'J']
# row = ['A', 'B', 'C', '', 'D', 'E', '', '', '', 'F', '', 'G', 'H']
row = ['', '', 'A', 'B', '', '', '', '', 'C', '']

start = [0]
end = []
have_seen_letter = False
for i in range(1, len(row) - 1):
    letter = row[i]
    if letter != '':
        have_seen_letter = True
    if letter == '' and row[i - 1] == '':
        start.append(i)
        have_seen_letter = False
    if letter != '' and row[i - 1] == '':
        start.append(i)
    if letter != '' and row[i + 1] == '':
        end.append(i)
    if letter == '' and (((i - 1) in end) or (i - 1 == 0)) and row[i + 1] == '':
        end.append(i)

# print(start)
end.append(len(row) - 1)
# print(end)

pairs = []
for starting_index in start:
    for ending_index in end:
        if starting_index < ending_index:
            pairs.append((starting_index, ending_index))


needed_pairs = []
for pair in pairs:
    has_letter = False
    has_blank = False
    for i in range(pair[0], pair[1] + 1):
        if row[i] == '':
            has_blank = True
        if row[i] !=  '':
            has_letter = True
        if has_letter and has_blank:
            needed_pairs.append(pair)
            break

constraints = []
for pair in needed_pairs:
    constraint = []
    for i in range(pair[0], pair[1] + 1):
        if row[i] != '':
            constraint.append((i - pair[0], row[i])) # for brian, we still need to keep track of staring index
    constraints.append((pair[1] - pair[0] + 1, constraint))

print(constraints)

