'''
Actions describe what can be done in the system.
For example, the "robot arm" MOVES a block from one location to another.
'''
# Stack the first block on top of the second block if all conditions are met
def stack(x, y):
    #Determine preconditions

    # In order for block X to stack on top of block y
    # Block x must be clear
    if x.state.Clear: # Robot arm must also be empty

        # CHECK CONSTRAINTS ???
        
        print("Stack the block!")
        
        # DO ADDITIONS
        # DO DELETIONS
        # 

def unstack(x, y):
    pass

def move(x, y):
    pass

def pick_up(x, y):
    pass

def put_down(x, y):
    pass

# No operation; nothing happens, but time passes
def noop():
    pass

