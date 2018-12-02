'''
RobotArm.py contains definitions and attributes pertaining to the Robot Arm
'''
from enum import Enum
from .Blocks import TableState
from .Blocks import Location
from utils import Constants
from game.Drawable import BlockSprite

'''
RobotArm acts as the robot arm that will be used to manage the blocks in the World of Blocks problem.
RobotArm is a SINGLETON object
'''
class RobotArm:
    # Store the instance
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method """
        if RobotArm.__instance == None:
            RobotArm()
        return RobotArm.__instance

    # Private Constructor for the robot arm
    # Initially, the arm is empty and is not holding a block
    def __init__(self):
        if RobotArm.__instance != None:
            raise Exception("RobotArm is a singleton class.")
        else:
            self.__state = ArmState.EMPTY
            self.__block = None
            self.__goal_dict = {}      # List of symbols with matching states
            self.__initial_state = TableState()
            self.__goal_state = TableState()
            self.__solver = None
            self.__sprite_dict = {}
            RobotArm.__instance = self

    # The arm should only grab a block if the arm is already empty
    def grab_block(self, block):
        if self.__state == ArmState.EMPTY:
            self.__block = block
            self.__state = ArmState.HOLDING

    # The arm shoudl only release a block if the arm has the block in its hands
    def release_block(self):
        if self.__state == ArmState.HOLDING:
            self.__block = None
            self.__state = ArmState.EMPTY

    # Return the arm state
    def get_state(self):
        return self.__state

    # Return the block that the arm is holding
    def get_block(self):
        return self.__block

    # Register initial state
    def register_initial_state(self, initial_state):
        self.__initial_state = initial_state

    # Returns the initial state
    def get_initial_state(self):
        if self.__initial_state != []:
            return self.__initial_state

    # Returns the goal state
    def get_goal_state(self):
        if self.__goal_state != []:
            return self.__goal_state

    # Return the goal state dictionary
    def get_goal_dict(self):
        return self.__goal_dict

    # Register the solver object
    def register_solver(self, solver):
        self.__solver = solver
        # Create dictionary of goal states for each symbol
        for block in self.__goal_state.L1:
            above_component = []
            for item in block.state.above:
                above_component.append(item.symbol)
            on = None
            if block.state.on:
                on = block.state.on.symbol
            dict_state = DictState(above_component, on, block.state.clear, block.state.table, block.state.location)
            self.__goal_dict[block.symbol] = dict_state
        for block in self.__goal_state.L2:
            above_component = []
            for item in block.state.above:
                above_component.append(item.symbol)
            on = None
            if block.state.on:
                on = block.state.on.symbol
            dict_state = DictState(above_component, on, block.state.clear, block.state.table, block.state.location)
            self.__goal_dict[block.symbol] = dict_state
        for block in self.__goal_state.L3:
            above_component = []
            for item in block.state.above:
                above_component.append(item.symbol)
            on = None
            if block.state.on:
                on = block.state.on.symbol
            dict_state = DictState(above_component, on, block.state.clear, block.state.table, block.state.location)
            self.__goal_dict[block.symbol] = dict_state
        for block in self.__goal_state.L4:
            above_component = []
            for item in block.state.above:
                above_component.append(item.symbol)
            on = None
            if block.state.on:
                on = block.state.on.symbol
            dict_state = DictState(above_component, on, block.state.clear, block.state.table, block.state.location)
            self.__goal_dict[block.symbol] = dict_state

    # Returns the solver object
    def run_solver(self):
        if (self.__solver != None):
            self.__solver.solve()
        else:
            raise Exception('Solver has not yet been registered!')

    # Register goal state by adding each block from a list to the goal state
    def register_goal_state(self, goal_state):
        self.__goal_state = goal_state

    '''
    Register a block with a corresponding sprite; add it to dictionary
    '''
    def register_block_sprite(self, block):
        # Create the block sprite
        block_sprite = BlockSprite(block.symbol)
        # Set the location of the block sprite
        block_x = 0
        if block.state.location == Location.L1:
            block_x = Constants.LOCATION_LABEL_SPACING * 0
        elif block.state.location == Location.L2:
            block_x = Constants.LOCATION_LABEL_SPACING * 1
        elif block.state.location == Location.L3:
            block_x = Constants.LOCATION_LABEL_SPACING * 2
        elif block.state.location == Location.L4:
            block_x = Constants.LOCATION_LABEL_SPACING * 3
        block_sprite.position = block_x, (Constants.BLOCK_TABLE_HEIGHT + (Constants.BLOCK_HEIGHT * len(block.state.above)))
        block_sprite.position = block_x, Constants.BLOCK_HEIGHT * len(block.state.above)
        self.__sprite_dict[block.symbol] = block_sprite

    '''
    Returns the sprite dictionary
    '''
    def get_sprite_dict(self):
        return self.__sprite_dict

    # Compare initial and goal state, return true if they match, false otherwise
    def is_goal_state_reached(self):
        # If the initial state and goal states are not empty (they must both be "registered")
        # And if they have the same amount of blocks in each, compare each block with a matching symbol
        if (self.__initial_state != [] and self.__goal_state != [] and 
            len(self.__initial_state) == len(self.__goal_state)):
            temp_goal_state = self.__goal_state # Temporary list to contain the goal state
            for init_block in self.__initial_state:
                matches_symbol = False  # Check each goal block to see if symbol matches
                for goal_block in temp_goal_state:
                    if init_block.symbol == goal_block.symbol: # Check for symbol matches
                        matches_symbol = True
                        if init_block.state != goal_block.state: # If the states do not match, goal state is not reached
                            return False
                        else:                                   # Otherwise, remove this block from the temp list so we don't check for it again
                            temp_goal_state.remove(goal_block)  # Remove the blocks from their respective lists
                            # If we get here and temp goal state is empty and we are at the last item of the initial state list
                            # Then we have a matching state
                            if len(temp_goal_state) == 0 and self.__initial_state[-1] == init_block:
                                return True
                            break
                # If it finishes iterating and a symbol is not matched, then the same blocks are not in the states
                if not matches_symbol:
                    raise Exception("Goal blocks and Initial blocks do not contain the same blocks!")
        else:
            return False
        return False

    # Returns if any block is on the given table location
    def is_location_empty(self, table_loc):
        if table_loc == Location.L1:
            if len(self.__solver.current_state.L1) == 0:
                return True
        elif table_loc == Location.L2:
            if len(self.__solver.current_state.L2) == 0:
                return True
        elif table_loc == Location.L3:
            if len(self.__solver.current_state.L3) == 0:
                return True
        elif table_loc == Location.L4:
            if len(self.__solver.current_state.L4) == 0:
                return True
        return False

    '''
    Checks if block is at goal state.
    Returns true if it is, false otherwise.
    '''
    def is_block_at_goal(self, block):
        return block.state == self.__goal_dict[block.symbol]


'''
ArmState is an Enum that defines whether the robot arm is holding a block or not.
'''
class ArmState(Enum):
    HOLDING = 1
    EMPTY = 0

'''
DictState represents the states using only symbols
'''
class DictState():
    def __init__(self, above, on, clear, table, location):
        self.above = above
        self.on = on
        self.clear = clear
        self.table = table
        self.location = location