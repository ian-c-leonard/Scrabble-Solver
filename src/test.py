from lexpy.dawg import DAWG
from constants import WORDS
from datetime import datetime

# row = ['', '', 'A', 'R', 'C', '', '' , '', '', 'B', '', 'C', 'A', '', '', '']
# row = ['A', '', '', '', 'B', '', 'C', '', 'D', 'E', 'F', 'G', '', '', 'H', '', 'J']
row = ['A', 'B', 'C', '', 'D', 'E', '', '', '', 'F', '', 'G', 'H']

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

print(start)
end.append(len(row) - 1)
print(end)
