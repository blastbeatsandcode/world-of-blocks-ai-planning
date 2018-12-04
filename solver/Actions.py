from .RobotArm import ArmState
from .RobotArm import RobotArm
from .Blocks import Location
from utils import Constants
from time import sleep
import cocos
from cocos.actions import *
import pyglet
from cocos import actions
'''
Actions describe what can be done in the system.
For example, the "robot arm" MOVES a block from one location to another.
The following functions define:
PRE - Preconditions
CHNG - Changes to be made
In STRIPS, there is usually an ADD and a DEL but for the purposes of this program,
Additions and Deletions are all handled concurrently with the CHNG description.
Constraints were also removed because invalid datatypes should prevent issues from occuring
'''
# Stack the first block on top of the second block if all conditions are met
def stack(x, y):
    '''
    PRE:    Robot arm must be holding x; y must be clear; y must be at the same location as x
    CHNG:   On(x, y); clear(x); Robot arm empty; 
            robot arm block = None; y clear = False; x above y and everything below y
    '''
    if y.state.clear and RobotArm.get_instance().get_block() == x and x.state.location == y.state.location:  # PRECONDITIONS 
        print("Stack the block - ", x.symbol)                                   # CHANGES
        x.state.on = y
        x.state.clear = True
        # EMPTY arm; sets block to None
        RobotArm.get_instance().release_block()
        y.state.clear = False
        # Append Y and all of it's "above" members to x block's above relation
        x.state.above.append(y)
        for block in y.state.above:
            x.state.above.append(block)
        move_sprite_to_location(x, y.state.location)
        # Check if block is at goal
        x.at_goal = RobotArm.get_instance().is_block_at_goal(x)
        return True
    return False

# Unstack removes the first block from the top of the second block
# ONLY IF the first block IS NOT on the table
def unstack(x, y):
    '''
    PRE:    Robot arm must be empty; x must be clear; x must be ON y; x must NOT be on the table; x must NOT be at goal state
    CHNG:   clear(y); Robot arm HOLDING x; x CLEAR = False; x ON = None; x above = []
    '''
    if RobotArm.get_instance().get_state() == ArmState.EMPTY and x.state.clear == True and x.state.on == y and x.state.table == False and x.at_goal == False:
        print("Unstack the block - ", x.symbol)
        y.state.clear = True
        RobotArm.get_instance().grab_block(x)
        x.state.clear = False
        x.state.on = None
        x.state.above = []
        move_sprite_to_arm(x)
        return True
    return False

# pick_up removes the block from the table
# ONLY IF the first block IS on the table
def pick_up(x):
    '''
    PRE:    Robot arm must be empty; x must be on the table; x must be CLEAR; x is not at goal.
    CHNG:   x table = False; Robot arm grab x; above is empty;
    '''
    print("VALUES ARE: ")
    if RobotArm.get_instance().get_state() == ArmState.EMPTY and x.state.table == True and x.state.clear == True and x.at_goal == False:
        print("Pick up the block - ", x.symbol)
        x.state.table = False
        x.state.above = []
        RobotArm.get_instance().grab_block(x)
        move_sprite_to_arm(x)
        return True
    return False

# put_down places the block directly onto a table location
def put_down(x, table_loc):
    '''
    PRE:    Robot arm must be holding x; no blocks must be on the specified location; block's current location must be equal to new location
            (New location has been set by MOVE)
    CHNG:   Clear(x); x table = True; Robot arm empty
    '''
    if RobotArm.get_instance().get_block() == x and RobotArm.get_instance().is_location_empty(table_loc) and x.state.location == table_loc:
        print("Put down the block - " + x.symbol + "Location is: " + str(x.state.location))
        x.state.clear = True
        x.state.table = True
        RobotArm.get_instance().release_block()
        move_sprite_to_location(x, table_loc)
        # Check if block is at goal
        x.at_goal = RobotArm.get_instance().is_block_at_goal(x)
        return True
    return False


# Move is only carried out by the robot arm BETWEEN (unstack/pick_up) and (stack/put_down actions)
# Assigns a new location to the block being held
def move(end_location):
    '''
    PRE:    Robot arm must be holding a block and end location must not be block's current location
    CHNG:   block location = end_location
    '''
    if RobotArm.get_instance().get_state() == ArmState.HOLDING and RobotArm.get_instance().get_block().state.location != end_location:
        print("Move the block - ", RobotArm.get_instance().get_block().symbol)
        RobotArm.get_instance().get_block().state.location = end_location
        return True
    return False

# No operation; nothing happens, but time passes
def noop():
    pass


'''
Handle moving the sprite to another location
'''
def move_sprite_to_location(block, loc):
    # Get the sprite from the dictionary
    sprites = RobotArm.get_instance().get_sprite_dict()
    #sprite = sprites[block.symbol]
    state = RobotArm.get_instance().get_current_state()

    y_val = 0
    x_val = 0
    if loc == Location.L1:
        x_val = Constants.LOCATION_LABEL_SPACING * 0
        y_val = Constants.BLOCK_HEIGHT * len(state.L1)
    elif loc == Location.L2:
        x_val = Constants.LOCATION_LABEL_SPACING * 1
        y_val = Constants.BLOCK_HEIGHT * len(state.L2)
    elif loc == Location.L3:
        x_val = Constants.LOCATION_LABEL_SPACING * 2
        y_val = Constants.BLOCK_HEIGHT * len(state.L3)
    elif loc == Location.L4:
        x_val = Constants.LOCATION_LABEL_SPACING * 3
        y_val = Constants.BLOCK_HEIGHT * len(state.L4)

    sprites[block.symbol].do(MoveTo((x_val, y_val), 1))
    RobotArm.get_instance().get_sprite().do(MoveTo((x_val + 550, y_val + 120), 1))
    # UNCOMMENT THE FOLLOWING LINE FOR IMMEDIATE RESULTS
    sleep(2.0)

'''
Handle moving sprite to robot arm
'''
def move_sprite_to_arm(block):
    # Get the sprite from the dictionary
    sprites = RobotArm.get_instance().get_sprite_dict()
    sprite = sprites[block.symbol]

    RobotArm.get_instance().get_sprite().do(MoveTo((550 + 400, 785), 1))
    sprites[block.symbol].do(MoveTo((400, 660), 1))
    # UNCOMMENT THE FOLLOWING LINE FOR IMMEDIATE RESULTS
    sleep(2.0)

