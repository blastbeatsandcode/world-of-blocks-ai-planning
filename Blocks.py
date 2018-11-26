from enum import Enum

'''
Block defines the characteristics and attributes of blocks within the World of Blocks problem
Blocks have a symbol that represents them, a location they have with respect to the table
And a status associated with
'''
class Block:
    # Constructor for the block
    def __init__(self, symbol, location):
        self.symbol = str(symbol)
        self.location = location
        self.state = State()

'''
States define the different states of the World of Blocks problem
Each block has a state, and the states have the relations for blocks about them
'''
class State():
    # The state of a block has the following relations at any given time
    def __init__(self):
        self.Above = None       # A list of blocks the block is above
        self.On = None          # A block the block is on top of
        self.Clear = None       # If the block has any blocks on top of it
        self.Table = None       # If the the block is directly on the table

'''
Location is an enumerator that defines the locations on the table
'''
class Location(Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"