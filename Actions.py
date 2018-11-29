from RobotArm import ArmState
from RobotArm import RobotArm
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
    PRE:    Robot arm must be holding x; y must be clear
    CHNG:   On(x, y); clear(x); Robot arm empty; 
            robot arm block = None; y clear = False; x above y and everything below y
    '''
    if y.state.clear and RobotArm.get_instance().get_block() == x:  # PRECONDITIONS 
        print("Stack the block")                                   # CHANGES
        x.state.on = y
        x.state.clear = True
        # EMPTY arm; sets block to None
        RobotArm.get_instance().release_block()
        y.state.clear = False
        # Append Y and all of it's "above" members to x block's above relation
        x.state.above.append(y)
        for block in y.state.above:
            x.state.above.append(block)
        return True
    return False

# Unstack removes the first block from the top of the second block
# ONLY IF the first block IS NOT on the table
def unstack(x, y):
    '''
    PRE:    Robot arm must be empty; x must be clear; x must be ON y; x must NOT be on the table
    CHNG:   clear(y); Robot arm HOLDING x; x CLEAR = False; x ON = None; x above = []
    '''
    if RobotArm.get_instance().get_state() == ArmState.EMPTY and x.state.clear == True and x.state.on == y and x.state.table == False:
        print("Unstack the block")
        y.state.clear = True
        RobotArm.get_instance().grab_block(x)
        x.state.clear = False
        x.state.on = None
        x.state.above = []
        return True
    return False

# pick_up removes the block from the table
# ONLY IF the first block IS on the table
def pick_up(x):
    '''
    PRE:    Robot arm must be empty; x must be on the table; x must be CLEAR
    CHNG:   x table = False; Robot arm grab x; 
    '''
    if RobotArm.get_instance().get_state() == ArmState.EMPTY and x.state.table == True and x.state.clear == True:
        print("Pick up the block")
        x.state.table = False
        RobotArm.get_instance().grab_block(x)
        return True
    return False

# put_down places the block directly onto a table location
def put_down(x, table_loc):
    '''
    PRE:    Robot arm must be holding x; no blocks must be on the specified location; block's current location must be equal to new location
            (New location has been set by MOVE)
    CHNG:   Clear(x); x table = True; Robot arm empty
    '''
    if RobotArm.get_instance().get_block() == x and RobotArm.get_instance().is_location_empty(table_loc) and x.location == table_loc:
        print("Put down the block")
        x.state.clear = True
        x.state.table = True
        RobotArm.get_instance().release_block()
        return True
    return False


# Move is only carried out by the robot arm BETWEEN (unstack/pick_up) and (stack/put_down actions)
# Assigns a new location to the block being held
def move(end_location):
    '''
    PRE:    Robot arm must be holding a block and end location must not be block's current location
    CHNG:   block location = end_location
    '''
    if RobotArm.get_instance().get_state() == ArmState.HOLDING and RobotArm.get_instance().get_block().location != end_location:
        print("Move the block")
        RobotArm.get_instance().get_block().location = end_location
        return True
    return False

# No operation; nothing happens, but time passes
def noop():
    pass

