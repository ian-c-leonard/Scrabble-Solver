from lexpy.dawg import DAWG
from constants import WORDS
from datetime import datetime

# row = ['', '', 'A', 'R', 'C', '', '' , '', '', 'B', '', 'C', 'A', '', '', '']
# row = ['A', '', '', '', 'B', '', 'C', '', 'D', 'E', 'F', 'G', '', '', 'H', '', 'J']
# row = ['A', 'B', 'C', '', 'D', 'E', '', '', '', 'F', '', 'G', 'H']
row = ['', '', 'A', 'B', '', '', '', '', 'C', '']

## Getting the start and end indices
start = [0]
end = []
for i in range(1, len(row) - 1):
    letter = row[i]
    if not letter and not row[i - 1]:
        start.append(i)
    if letter and not row[i - 1]:
        start.append(i)
    if letter and not row[i + 1]:
        end.append(i)
    if not letter and (((i - 1) in end) or (i - 1 == 0)) and not row[i + 1]:
        end.append(i)
end.append(len(row) - 1)

## Getting all possible pairs
pairs = [(starting_index, ending_index) for starting_index in start for ending_index in end if starting_index < ending_index]

def filter_unneeded_pairs(pair):
    section = row[pair[0]: pair[1] + 1]
    blank_count = section.count('')
    return blank_count < len(section) and blank_count != 0

## Filter out pairs that have all or no blanks
pairs = [pair for pair in pairs if filter_unneeded_pairs(pair)]

## Making constraints
constraints = [(pair[1] - pair[0] + 1, [(i - pair[0], row[i]) for i in range(pair[0], pair[1] + 1) if row[i]]) for pair in pairs]

print(constraints)
