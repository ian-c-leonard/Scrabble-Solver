import numpy as np
from constants import WORDS
from lexpy.dawg import DAWG
from collections import Counter

class Scrabble():
    def __init__(self, size = 15, multipliers = None):
        print('Initializing Scrabble...')
        assert size % 2, 'Board length must be odd.'
        self.agent = 0 # The agent's turn
        self.turn = 1 # What turn we're on
        self.words = WORDS # List of Scrabble words
        self.size = size # Size of the board
        self.center = (size // 2, size // 2)
        self.board = np.array(['']*size**2, dtype = object).reshape(size, size)
        self.multipliers = multipliers if multipliers else self._default_multipliers()
        self.counted_words = np.zeros((size, size), dtype = int)
        self.tiles  = ['A']*9 + ['B']*2 + ['C']*2 + ['D']*4 + ['E']*12 + ['F']*2 + \
                      ['G']*3 + ['H']*2 + ['I']*9 + ['J']*1 + ['K']*1 + ['L']*4 + \
                      ['M']*2 + ['N']*6 + ['O']*8 + ['P']*2 + ['Q']*1 + ['R']*6 + \
                      ['S']*4 + ['T']*6 + ['U']*4 + ['V']*2 + ['W']*2 + ['X']*1 + \
                      ['Y']*2 + ['Z']*1 + ['BLANK']*2
        self.score_map = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
                       'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 
                       'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 
                       'Y': 4, 'Z': 10, 'BLANK': 0}
        print('Optimizing Word Dictionary...')
        self.dawg = self._optimize_scrabble_words() # Optimize Scrabble words with a lookup dictionary
        print('Initalizing Agents...')
        self.agents = self._initialize_agents()
        print('Done')
        
    
    def _initialize_agents(self):
        global agent_1
        global agent_2
        
        agent_1 = Agent(self, 1)
        agent_2 = Agent(self, 2)
    
        return [agent_1, agent_2]
    
        
    def _optimize_scrabble_words(self):
        '''Initializes a Trie of all possible Scrabble words for optimized lookups.'''
        dawg = DAWG()
        dawg.add_all(WORDS)
    
        return dawg
    
            
    def _default_multipliers(self):
        quadrant = \
        [['3W', '', '', '2L', '', '', '', '3W'],
        ['', '2W', '', '', '', '3L', '', ''],
        ['', '', '2W', '', '', '', '2L', ''],
        ['2L', '', '', '2W', '', '', '', '2L'],
        ['', '', '', '', '2W', '', '', ''],
        ['', '3L', '', '', '', '3L', '', ''],
        ['', '', '2L', '', '', '', '2L', ''],
        ['3W', '', '', '2L', '', '', '', '2W']]

        quadrant = quadrant + quadrant[len(quadrant)-2::-1]
        multipliers = [y + y[::-1][1:] for y in quadrant]
        return np.array(multipliers, dtype = object).reshape(self.size, self.size)
    
   

    def is_over(self):
        out_of_words = not self.tiles and any([not agent.tiles for agent in self.agents])
        
        out_of_possible_moves = any([agent.out_of_moves for agent in self.agents])
        
        if out_of_words or out_of_plays:
            return True
        
        return False
    
            
        
    def unplayed_indices(self, indices):
        return not all([self.counted_words[index] for index in indices])
    
    
    def valid_word(self, word):
        return word in self.dawg
    
        
    def place(self, word, indices, mock = False):
        '''Place a word in a location on the board.
           You can mock placements and return the would-be board state'''
        
        board = self.board.copy() if mock else self.board
        
        for count, ind in enumerate(indices):
            board[ind] = word[count]
        
        if mock: # We want to actually return the board if it's a mock placemenent
            return board

    

        
    
    def is_valid_placement(self, word, indices):
        '''Checks if placing a word here would be a valid placement.'''
        
        if self.turn == 1:
            if not self.center in indices:
                return False
        
        else:
            # Overlapping letters must be the same and at least one letter must overlapp
            for count, ind in enumerate(indices):
                if self.board[ind] == word[count]:
                    break

                return False            

            created_words = self.get_created_word_indices(word, indices)

            for word in created_words.keys():
                if not self.valid_word(word):
                    return False
            
        return True
    
    
    def placement_score(self, word, indices):
        '''Returns the score of a word being placed and a specified index'''
        
        # Check word is long enough
        assert self.valid_word(word) > 1, 'Not a long enough word, dumbass.'
        
        # Check word is placed in a valid location
        assert all([board[ind] == word[ind] or not board[ind] for ind in indices]), 'Not a valid move, dumbass.'
        
        created_indices = self.get_created_word_indices(word, indices)
        assert all([self.valid_word(x) for x in created_indices]), 'You created invalid words, dumbass.'
        
        multipliers = [multipliers[ind] for ind in created_indices if multipliers[ind]]
        
        
    



    # Word, Indices --> Score
    def score(self, word, indices):
        '''Returns the score of a word at a given index'''
        
        base_word_score = [self.score_map[letter] for letter in word]
        board_scores = [self.multipliers[ind] for ind in indices]
        
        word_multiplier = 1
        
        for ind, score in enumerate(board_scores):
            if score == '3W':
                word_multiplier *= 3
                continue
            
            if score == '2W':
                word_multiplier *= 2
                continue
                
            if score == '3L':
                base_word_score[ind] *= 3
                continue
                
            if score == '2L':
                base_word_score[ind] *= 2
                continue
            
        return sum(base_word_score) * word_multiplier
    
   

class Agent():
    def __init__(self, scrabble, number):
        self.game = scrabble
        self.number = number
        self.tiles = []
        self.opponent_tiles = []
        self.out_of_moves = False
        print(f"AGENT_{self.number}: Drawing Tiles And Guessing Opponent's Tiles")
        #print "test"
        self.draw()
        self.guess_opponent_tiles()
     
    
    def draw(self):
        '''Draw from the global game's tile bag'''
        n_missing = 7 - len(self.tiles)
        drawn_tiles = list(np.random.choice(self.game.tiles, n_missing, replace = False))
        
        for x in drawn_tiles:
            self.game.tiles.remove(x)
        
        self.tiles = drawn_tiles
        
    def guess_opponent_tiles(self):
        """Guess opponent's tiles given the current distribution of tiles"""
        self.opponent_tiles = np.random.choice(self.game.tiles, 7, replace = False)
        
    def move(self):
        pass
    
    
    def get_created_word_indices(self, word, indices):
        '''Returns the indices of all newly createds from placing a word in a position'''

        size = self.game.size
        new_board = self.place(word, indices, mock = True)
        horizontal = len(set([x[0] for x in indices])) == 1 # Word is being played horizontally
        word_indices = []

        if horizontal:
            row = indices[0][0]

            # Get all vertical words created
            for _, j in indices:
                col = [(x, j) for x in range(size)]
                longest_indices = []
                created = False

                for index in col:
                    if index in indices:  # The letter was just placed
                        created = True

                    if not new_board[index] and not created:
                        longest_indices = []

                    if new_board[index]:
                        longest_indices.append(index)

                    elif created:
                        if len(longest_indices) > 1:
                            word_indices.append(longest_indices)
                        break


            # Get all horizontal words created
            curr_row = [(row, x) for x in range(size)]
            longest_indices = []
            created = False

            for index in curr_row:
                if index in indices:  # The letter was just placed
                    created = True

                if not new_board[index] and not created:
                    longest_indices = []

                if new_board[index]:
                    longest_indices.append(index)

                elif created:
                    word_indices.append(longest_indices)
                    break

        else:
            col = indices[0][1]

            # Get all horizontal words created
            for i, _ in indices:
                row = [(i, x) for x in range(size)]
                longest_indices = []
                created = False

                for index in row:
                    if index in indices:  # The letter was just placed
                        created = True

                    if not new_board[index] and not created:
                        longest_indices = []

                    if new_board[index]:
                        longest_indices.append(index)

                    elif created:
                        if len(longest_indices) > 1:
                            word_indices.append(longest_indices)
                        break


            # Get the vertical word created
            curr_col = [(x, col) for x in range(size)]
            longest_indices = []
            created = False

            for index in curr_col:
                if index in indices:  # The letter was just placed
                    created = True

                if not new_board[index] and not created:
                    longest_indices = []

                if new_board[index]:
                    longest_indices.append(index)

                elif created:
                    word_indices.append(longest_indices)
                    break

        
        word_indices = [indices for indices in word_indices if self.unplayed_indices(indices)]

        print(word_indices)
        return [{''.join([new_board[ind] for ind in indices]): indices} for indices in word_indices]
    
    def get_grids(self):
        board = self.game.board.copy()
        rows = [board[i] for i in range(self.game.size)]
        cols = [board[:][i] for i in range(self.game.size)]
        
        return  rows + cols
        
    
    def grid_optimizer(self, letters, grid, indices):
        ## Rework grid_optimizer to take in a max_length grid (i.e. 12) and then find the largest word that CAN fit in said grid
        ## i.e. [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '] --> CATS ( potentially)

        # Deduce a list of words which fit in the given grid with letter constraints
        search_string = '*' + ''.join([x if x else '?' for x in grid]).strip('?') + '*'

        result = self.game.dawg.search(search_string)

        counter = Counter(letters + [x for x in grid if x])

        playable_words = [word for word in result if 
                               all([counter[letter] >= sum([1 for x in word if x == letter]) for letter in word])]

        max_word = (None, -np.inf)
        for word in playable_words:

            for start, index in enumerate(indices):
                if all([grid[ind + start] == word[ind] for ind in range(len(word)) if grid[ind + start].isalnum()]):
                    start_ind = start
                    break

            score = self.score(word, indices[start: start + len(word)])
            if score > max_word[1]:
                max_word = (word, score)
                
        # Return max score of playable words with givin indices
        return max_word[0]
    
    
    def place(self, word, indices, mock = False):
        '''Place a word in a location on the board.
           You can mock placements and return the would-be board state'''
        
        board = self.game.board.copy() if mock else self.game.board
        
        for count, ind in enumerate(indices):
            board[ind] = word[count]
        
        if mock: # We want to actually return the board if it's a mock placemenent
            return board




class View():
    def __init__(self, scrabble, number):
        self.game = scrabble
        self.number = number                                                                                                                                                            


    def visualize_rack(self):
        #Letters from: http://patorjk.com/software/taag/#p=display&f=Blocks&t=e
        title = "Welcome to\n"\
                " .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.\n"\
                "| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |\n"\
                "| |    _______   | || |     ______   | || |  _______     | || |      __      | || |   ______     | || |   ______     | || |   _____      | || |  _________   | |\n"\
                "| |   /  ___  |  | || |   .' ___  |  | || | |_   __ \    | || |     /  \     | || |  |_   _ \    | || |  |_   _ \    | || |  |_   _|     | || | |_   ___  |  | |\n"\
                "| |  |  (__ \_|  | || |  / .'   \_|  | || |   | |__) |   | || |    / /\ \    | || |    | |_) |   | || |    | |_) |   | || |    | |       | || |   | |_  \_|  | |\n"\
                "| |   '.___`-.   | || |  | |         | || |   |  __ /    | || |   / ____ \   | || |    |  __'.   | || |    |  __'.   | || |    | |   _   | || |   |  _|  _   | |\n"\
                "| |  |`\____) |  | || |  \ `.___.'\  | || |  _| |  \ \_  | || | _/ /    \ \_ | || |   _| |__) |  | || |   _| |__) |  | || |   _| |__/ |  | || |  _| |___/ |  | |\n"\
                "| |  |_______.'  | || |   `._____.'  | || | |____| |___| | || ||____|  |____|| || |  |_______/   | || |  |_______/   | || |  |________|  | || | |_________|  | |\n"\
                "| |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | |\n"\
                "| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |\n"\
                " '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' "                                                                                                                                                        
        print (title)

        player_rack = Agent(self.game, self.number).tiles
        fake_rack = ['A', 'B', 'C', 'B', 'A', 'B', 'C']
        fake_board = [['E', 'S', 'K', 'E', 'E', 'T', 'I', 'T', '', '', '', '', '', '', ''],
                     ['', '', '', '', 'S', '', '', '', '', '', '', '', '', '', ''],
                     ['', '', '', '', 'K', '', '', '', '', '', '', '', '', '', ''],
                     ['', '', '', '', 'E', '', '', '', '', '', '', '', '', '', ''],
                     ['', '', '', '', 'E', '', '', '', '', '', '', '', '', '', ''],
                     ['', '', '', '', 'T', '', '', '', '', '', '', '', '', '', ''],
                     ['', '', '', '', 'I', '', '', '', '', '', '', '', '', '', ''],
                     ['', '', '', '', 'T', '', '', 'star', '', '', '', '', '', '', ''],
                     ['', '', '', '', '', '', 'B', 'O', 'O', 'B', 'S', '', '', '', ''],
                     ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                     ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                     ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                     ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                     ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                     ['', '', '', '', '', '', '', '', '', 'A', 'S', 'T', 'A', 'R', ''],]

        
        star =  [" ------------------ ", 
                 "|         .        |",
                 "|        / \       |",
                 "|    ___/   \___   |",
                 "|   '.         .'  |",
                 "|     '.     .'    |",
                 "|      / .'. \     |",
                 "|     /.'   '.\    |",
                 "|                  |",
                 "|                  |",
                 " ------------------ "]



        blank = [" ------------------ ", 
                 "|                  |",
                 "|                  |",
                 "|                  |",
                 "|                  |",
                 "|                  |",
                 "|                  |",
                 "|                  |",
                 "|                  |",
                 "|                  |",
                 " ------------------ "]


        a = [" ------------------ ", 
             "| .--------------. |",
             "| |      __      | |",
             "| |     /  \     | |",
             "| |    / /\ \    | |",
             "| |   / ____ \   | |",
             "| | _/ /    \ \_ | |",
             "| ||____|  |____|| |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        b = [" ------------------ ",
             "| .--------------. |",
             "| |   ______     | |",
             "| |  |_   _ \    | |",
             "| |    | |_) |   | |",
             "| |    |  __'.   | |",
             "| |   _| |__) |  | |",
             "| |  |_______/   | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        c = [" ------------------ ",
             "| .--------------. |",
             "| |     ______   | |",
             "| |   .' ___  |  | |",
             "| |  / .'   \_|  | |",
             "| |  | |         | |",
             "| |  \ `.___.'\  | |",
             "| |   `._____.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        d = [" ------------------ ",
             "| .--------------. |",
             "| |  ________    | |",
             "| | |_   ___ `.  | |",
             "| |   | |   `. \ | |",
             "| |   | |    | | | |",
             "| |  _| |___.' / | |",
             "| | |________.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        e = [" ------------------ ",
             "| .--------------. |",
             "| |  _________   | |",
             "| | |_   ___  |  | |",
             "| |   | |_  \_|  | |",
             "| |   |  _|  _   | |",
             "| |  _| |___/ |  | |",
             "| | |_________|  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        f = [" ------------------ ",
             "| .--------------. |",
             "| |  ________    | |",
             "| | |_   ___ `.  | |",
             "| |   | |   `. \ | |",
             "| |   | |    | | | |",
             "| |  _| |___.' / | |",
             "| | |________.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        g = [" ------------------ ",
             "| .--------------. |",
             "| |  ________    | |",
             "| | |_   ___ `.  | |",
             "| |   | |   `. \ | |",
             "| |   | |    | | | |",
             "| |  _| |___.' / | |",
             "| | |________.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        h = [" ------------------ ",
             "| .--------------. |",
             "| |  ________    | |",
             "| | |_   ___ `.  | |",
             "| |   | |   `. \ | |",
             "| |   | |    | | | |",
             "| |  _| |___.' / | |",
             "| | |________.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        i = [" ------------------ ",
             "| .--------------. |",
             "| |     _____    | |",
             "| |    |_   _|   | |",
             "| |      | |     | |",
             "| |      | |     | |",
             "| |     _| |_    | |",
             "| |    |_____|   | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        j = [" ------------------ ",
             "| .--------------. |",
             "| |  ________    | |",
             "| | |_   ___ `.  | |",
             "| |   | |   `. \ | |",
             "| |   | |    | | | |",
             "| |  _| |___.' / | |",
             "| | |________.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        k = [" ------------------ ",
             "| .--------------. |",
             "| |  ___  ____   | |",
             "| | |_  ||_  _|  | |",
             "| |   | |_/ /    | |",
             "| |   |  __'.    | |",
             "| |  _| |  \ \_  | |",
             "| | |____||____| | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        l = [" ------------------ ",
             "| .--------------. |",
             "| |  ________    | |",
             "| | |_   ___ `.  | |",
             "| |   | |   `. \ | |",
             "| |   | |    | | | |",
             "| |  _| |___.' / | |",
             "| | |________.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        m = [" ------------------ ",
             "| .--------------. |",
             "| |  ________    | |",
             "| | |_   ___ `.  | |",
             "| |   | |   `. \ | |",
             "| |   | |    | | | |",
             "| |  _| |___.' / | |",
             "| | |________.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        n = [" ------------------ ",
             "| .--------------. |",
             "| |  ________    | |",
             "| | |_   ___ `.  | |",
             "| |   | |   `. \ | |",
             "| |   | |    | | | |",
             "| |  _| |___.' / | |",
             "| | |________.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        o = [" ------------------ ",
             "| .--------------. |",
             "| |     ____     | |",
             "| |   .'    `.   | |",
             "| |  /  .--.  \  | |",
             "| |  | |    | |  | |",
             "| |  \  `--'  /  | |",
             "| |   `.____.'   | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        p = [" ------------------ ",
             "| .--------------. |",
             "| |  ________    | |",
             "| | |_   ___ `.  | |",
             "| |   | |   `. \ | |",
             "| |   | |    | | | |",
             "| |  _| |___.' / | |",
             "| | |________.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        q = [" ------------------ ",
             "| .--------------. |",
             "| |  ________    | |",
             "| | |_   ___ `.  | |",
             "| |   | |   `. \ | |",
             "| |   | |    | | | |",
             "| |  _| |___.' / | |",
             "| | |________.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        r = [" ------------------ ",
             "| .--------------. |",
             "| |  _______     | |",
             "| | |_   __ \    | |",
             "| |   | |__) |   | |",
             "| |   |  __ /    | |",
             "| |  _| |  \ \_  | |",
             "| | |____| |___| | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        s = [" ------------------ ",
             "| .--------------. |",
             "| |    _______   | |",
             "| |   /  ___  |  | |",
             "| |  |  (__ \_|  | |",
             "| |   '.___`-.   | |",
             "| |  |`\____) |  | |",
             "| |  |_______.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        t = [" ------------------ ",
             "| .--------------. |",
             "| |  _________   | |",
             "| | |  _   _  |  | |",
             "| | |_/ | | \_|  | |",
             "| |     | |      | |",
             "| |    _| |_     | |",
             "| |   |_____|    | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        u = [" ------------------ ",
             "| .--------------. |",
             "| |  ________    | |",
             "| | |_   ___ `.  | |",
             "| |   | |   `. \ | |",
             "| |   | |    | | | |",
             "| |  _| |___.' / | |",
             "| | |________.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        v = [" ------------------ ",
             "| .--------------. |",
             "| |  ________    | |",
             "| | |_   ___ `.  | |",
             "| |   | |   `. \ | |",
             "| |   | |    | | | |",
             "| |  _| |___.' / | |",
             "| | |________.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        w = [" ------------------ ",
             "| .--------------. |",
             "| |  ________    | |",
             "| | |_   ___ `.  | |",
             "| |   | |   `. \ | |",
             "| |   | |    | | | |",
             "| |  _| |___.' / | |",
             "| | |________.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        x = [" ------------------ ",
             "| .--------------. |",
             "| |  ________    | |",
             "| | |_   ___ `.  | |",
             "| |   | |   `. \ | |",
             "| |   | |    | | | |",
             "| |  _| |___.' / | |",
             "| | |________.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        y = [" ------------------ ",
             "| .--------------. |",
             "| |  ________    | |",
             "| | |_   ___ `.  | |",
             "| |   | |   `. \ | |",
             "| |   | |    | | | |",
             "| |  _| |___.' / | |",
             "| | |________.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        z = [" ------------------ ",
             "| .--------------. |",
             "| |  ________    | |",
             "| | |_   ___ `.  | |",
             "| |   | |   `. \ | |",
             "| |   | |    | | | |",
             "| |  _| |___.' / | |",
             "| | |________.'  | |",
             "| |              | |",
             "| '--------------' |",
             " ------------------ "]

        print ("Plaer Rack:", player_rack)
        print ("Fake Rack:", fake_rack)

        display_board = "Current Board\n"
        for row in fake_board:
            for sub in range(0, len(a)):
                for tile in row:
                    if tile == "A":
                        display_board += a[sub]
                    if tile == "B":
                        display_board += b[sub]
                    if tile == "C":
                        display_board += c[sub]
                    if tile == "D":
                        display_board += d[sub]
                    if tile == "E":
                        display_board += e[sub]
                    if tile == "F":
                        display_board += f[sub]
                    if tile == "G":
                        display_board += g[sub]
                    if tile == "H":
                        display_board += h[sub]
                    if tile == "I":
                        display_board += i[sub]
                    if tile == "J":
                        display_board += j[sub]
                    if tile == "K":
                        display_board += k[sub]
                    if tile == "L":
                        display_board += l[sub]
                    if tile == "M":
                        display_board += m[sub]
                    if tile == "N":
                        display_board += n[sub]
                    if tile == "O":
                        display_board += o[sub]
                    if tile == "P":
                        display_board += p[sub]
                    if tile == "Q":
                        display_board += q[sub]
                    if tile == "R":
                        display_board += r[sub]
                    if tile == "S":
                        display_board += s[sub]
                    if tile == "T":
                        display_board += t[sub]
                    if tile == "U":
                        display_board += u[sub]
                    if tile == "V":
                        display_board += v[sub]
                    if tile == "W":
                        display_board += w[sub]
                    if tile == "X":
                        display_board += x[sub]
                    if tile == "Y":
                        display_board += y[sub]
                    if tile == "Z":
                        display_board += z[sub]
                    if tile == "star":
                        display_board += star[sub]
                    if tile == "":
                        #TODO: add bonuses, or at least star in center
                        display_board += blank[sub]

                display_board += "\n"

        print (display_board)
        

        display_rack = "Your Tiles\n"
        for sub in range(0, len(a)):
            for tile in fake_rack:
                if tile == "":
                    display_rack += blank[sub]
                if tile == "A":
                    display_rack += a[sub]
                if tile == "B":
                    display_rack += b[sub]
                if tile == "C":
                    display_rack += c[sub]
                if tile == "D":
                    display_rack += d[sub]
                if tile == "E":
                    display_rack += e[sub]
                if tile == "F":
                    display_rack += f[sub]
                if tile == "G":
                    display_rack += g[sub]
                if tile == "H":
                    display_rack += h[sub]
                if tile == "I":
                    display_rack += i[sub]
                if tile == "J":
                    display_rack += j[sub]
                if tile == "K":
                    display_rack += k[sub]
                if tile == "L":
                    display_rack += l[sub]
                if tile == "M":
                    display_rack += m[sub]
                if tile == "N":
                    display_rack += n[sub]
                if tile == "O":
                    display_rack += o[sub]
                if tile == "P":
                    display_rack += p[sub]
                if tile == "Q":
                    display_rack += q[sub]
                if tile == "R":
                    display_rack += r[sub]
                if tile == "S":
                    display_rack += s[sub]
                if tile == "T":
                    display_rack += t[sub]
                if tile == "U":
                    display_rack += u[sub]
                if tile == "V":
                    display_rack += v[sub]
                if tile == "W":
                    display_rack += w[sub]
                if tile == "X":
                    display_rack += x[sub]
                if tile == "Y":
                    display_rack += y[sub]
                if tile == "Z":
                    display_rack += z[sub]

            display_rack += "\n"

        print (display_rack)

if __name__ == '__main__':
    game = Scrabble()
    agent = Agent(game, 1)
    view = View(game, 1)

    view.visualize_rack()



