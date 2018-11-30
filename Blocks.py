from enum import Enum

'''
Block defines the characteristics and attributes of blocks within the World of Blocks problem
Blocks have a symbol that represents them, a location they have with respect to the table
And a status associated with
'''
class Block:
    # Constructor for the block
    def __init__(self, symbol, location):
        self.symbol = str(symbol)   # Symbol on the block
        self.location = location    # Current location of the block
        self.state = State()        # State attributes of the block
        self.at_goal = False        # If block is at goal state

    # Print out block information
    def block_info(self):
        print("Symbol: " + self.symbol + " Loc: " + str(self.location))
        print("State:")
        print("Table - ", self.state.table)
        print("Clear - ", self.state.clear)
        above_str = "["
        for block in self.state.above:
            above_str += " " + block.symbol + ","
        if self.state.above == []:
            above_str = "[NONE"
        above_str += "]"
        print("Above -" + above_str)

'''
States define the different states of the World of Blocks problem
Each block has a state, and the states have the relations for blocks about them
'''
class State():
    # The state of a block has the following relations at any given time
    def __init__(self, above = [], on = None, clear = None, table = None):
        self.above = above      # A list of blocks the block is above
        self.on = on            # A block the block is on top of
        self.clear = clear      # If the block has any blocks on top of it
        self.table = table      # If the the block is directly on the table

'''
TableState defines the state of the table with each table location acting as a STACK
This can refer to both the goal state and the initial state of the table
'''
class TableState():
    def __init__(self, L1 = [], L2 = [], L3 = [], L4 = []):
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        self.L4 = L4

'''
Location is an enumerator that refers to the locations on the table
'''
class Location(Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"