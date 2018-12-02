'''
Pathfinding elements to carry out the problem solving.
'''
from . import Actions
from .Blocks import Location
from .RobotArm import RobotArm
from .RobotArm import DictState

class Solver:
    # Holds initial state blocks and goal state blocks
    def __init__(self, init_state_blocks, goal_state_blocks):
        self.init_state = init_state_blocks     # Initial state blocks
        self.goal_state = goal_state_blocks     # Goal state blocks
        self.current_state = init_state_blocks  # Current state of the blocks
        self.l1_complete = False
        self.l2_complete = False
        self.l3_complete = False
        self.l4_complete = False
        self.goals = {}

    '''
    Check if we have reached the goal state
    '''
    def goal_state_reached(self):
        for block in self.current_state.L1:
            if not block.at_goal:
                return False
        for block in self.current_state.L2:
            if not block.at_goal:
                return False
        for block in self.current_state.L3:
            if not block.at_goal:
                return False
        for block in self.current_state.L4:
            if not block.at_goal:
                return False
        return True

    '''
    Compares values on block in current state to block values in dictionary
    '''
    def is_block_at_goal(self, block):
        dict_value = RobotArm.get_instance().get_goal_dict()[block.symbol]
        # Compare above
        for item in block.state.above:
            if not item.symbol in dict_value.above:
                return False
        # Compare On
        if not block.state.on == None:
            if block.state.on.symbol != dict_value.on:
                return False
        else:
            if dict_value.on != None:
                return False
        # Compare Clear
        if block.state.clear != dict_value.clear:
            return False
        # Compare Table
        if block.state.table != dict_value.table:
            return False
        # Compare Location
        if block.state.location != dict_value.location:
            return False
        return True

    '''
    Check if blocks in stack are at goal state
    '''
    def stack_at_goal(self, loc):
        if loc == Location.L1:
            for block in self.current_state.L1:
                if not self.is_block_at_goal(block):
                    return False
            return True
        elif loc == Location.L2:
            for block in self.current_state.L2:
                if not self.is_block_at_goal(block):
                    return False
            return True
        elif loc == Location.L3:
            for block in self.current_state.L3:
                if not self.is_block_at_goal(block):
                    return False
            return True
        elif loc == Location.L4:
            for block in self.current_state.L4:
                if not self.is_block_at_goal(block):
                    return False
            return True
        else:
            raise Exception("Invalid location given to check if stack is at goal!")

    '''
    Solve the World of Blocks problem.
    '''
    def solve(self):
        # Get all blocks to the default position
        self.reposition()

        # If there are any blocks going to L1, find the TABLE block, and then reposition
        # Do this for each stack location
        self.get_l1_blocks()
        self.get_l2_blocks()
        #self.get_l3_blocks()
        #self.get_l4_blocks()

        print("DATA FOR L1 ==============")
        for block in self.current_state.L1:
            block.block_info()
        
        print("DATA FOR L2 ==============")
        for block in self.current_state.L2:
            block.block_info()

        print("DATA FOR L3 ==============")
        for block in self.current_state.L3:
            block.block_info()

        print("DATA FOR L4 ==============")
        for block in self.current_state.L4:
            block.block_info()

        print("Was goal state reached? ", self.goal_state_reached())

    '''
    Checks if a block in the "default" state has a goal state of the specified location
    '''
    def block_in_location(self, loc):
    # Check if there is a block in L4 that belongs in loc
        loc_found = False
        for block in self.current_state.L4:
            if RobotArm.get_instance().get_goal_dict()[block.symbol].location == loc:
                loc_found = True
        return loc_found

    '''
    Moves blocks to L3 from L4
    Used for L1 and L2 solving.
    '''
    def remove_bad_block(self):
        if len(self.current_state.L4) > 1:
            # Unstack the block and move it to L3
            block = self.current_state.L4.pop()
            Actions.unstack(block, self.current_state.L4[-1])
            Actions.move(Location.L3)
            if len(self.current_state.L3) == 0: # Put down if L3 is empty, stack otherwise
                Actions.put_down(block, Location.L3)
                self.current_state.L3.append(block)
                return True
            else:
                Actions.stack(block, self.current_state.L3[-1])
                self.current_state.L3.append(block)
                return True
        else: # We have reached the bottom of L4, reposition blocks
            self.reposition()
            return False

    '''
    Moves blocks to L2 from L4
    Used for L3 and L4 solving.
    '''
    def remove_bad_block_other(self):
        if len(self.current_state.L4) > 1:
            # Unstack the block and move it to L3
            block = self.current_state.L4.pop()
            Actions.unstack(block, self.current_state.L4[-1])
            Actions.move(Location.L2)
            if len(self.current_state.L2) == 0: # Put down if L3 is empty, stack otherwise
                Actions.put_down(block, Location.L2)
                self.current_state.L2.append(block)
            else:
                Actions.stack(block, self.current_state.L2[-1])
                self.current_state.L2.append(block)
        else: # We have reached the bottom of L4, reposition blocks
            self.reposition()

    '''
    Handle block movement to L1
    '''
    def get_l1_blocks(self):
        if self.block_in_location(Location.L1) and not self.l1_complete: # Check if we have blocks in location
            # Check each block in L4, if it is the table block
            # move it to L1. Otherwise place it on L3 for repositioning
            l4_reverse = list(reversed(self.current_state.L4))
            for block in l4_reverse:
                # If the block has a goal in L1
                if RobotArm.get_instance().get_goal_dict()[block.symbol].location == Location.L1:
                    # Check if L1 has any blocks on it; if it does not, find the TABLE block first
                    if len(self.current_state.L1) == 0: # Table block not found yet
                        # Find table block
                        # START HERE, IT THINKS C IS ON THE TABLE OR SOME SHIT?
                        if RobotArm.get_instance().get_goal_dict()[block.symbol].table:
                            table_block = self.current_state.L4.pop() # pull off table block
                            if table_block.state.table: # pick-up if on table, unstack otherwise
                                Actions.pick_up(table_block)
                                Actions.move(Location.L1)
                                Actions.put_down(table_block, Location.L1)
                                table_block.at_goal = True # Block is at goal state
                                self.current_state.L1.append(table_block)
                                self.reposition()
                                self.get_l1_blocks()
                            else: # unstack because it is not on bottom of L4
                                Actions.unstack(table_block, self.current_state.L4[-1])
                                Actions.move(Location.L1)
                                Actions.put_down(table_block, Location.L1)
                                self.current_state.L1.append(table_block)
                                table_block.at_goal = True
                                self.reposition()
                                self.get_l1_blocks()
                        else:
                            self.remove_bad_block()
                            self.get_l1_blocks()
                    else:   # Table block already found,
                            # Find the block that goes on the topmost block, put it there
                        top_block = self.current_state.L1[-1]
                        if RobotArm.get_instance().get_goal_dict()[block.symbol].on == top_block.symbol:
                            if block.state.table == True:
                                stack_block = self.current_state.L4.pop()
                                Actions.pick_up(stack_block)
                                Actions.move(Location.L1)
                                Actions.stack(stack_block, self.current_state.L1[-1])
                                stack_block.at_goal = True
                                self.current_state.L1.append(stack_block)
                                self.reposition()
                                self.get_l1_blocks()
                            else:
                                stack_block = self.current_state.L4.pop()
                                Actions.unstack(stack_block, self.current_state.L4[-1])
                                Actions.move(Location.L1)
                                Actions.stack(stack_block, self.current_state.L1[-1])
                                stack_block.at_goal = True
                                self.current_state.L1.append(stack_block)
                                self.reposition()
                                self.get_l1_blocks()
                        else:
                            self.remove_bad_block()
                            self.get_l1_blocks()
                else: # block does not belong on specified location
                    self.remove_bad_block()
                    self.get_l1_blocks()
            self.get_l1_blocks()
        else:
            #self.reposition()
            # check if stack is at goal state
            if self.stack_at_goal(Location.L1):
                self.l1_complete = True
            if self.l1_complete:
                for block in self.current_state.L1:
                    print(block.symbol)


    '''
    Handle block movement to L2
    '''
    def get_l2_blocks(self):
        if self.block_in_location(Location.L2) and not self.l2_complete: # Check if we have blocks in location
            # Check each block in L4, if it is the table block
            # move it to L1. Otherwise place it on L3 for repositioning
            l4_reverse = list(reversed(self.current_state.L4))
            for block in l4_reverse:
                # If the block has a goal in L1
                if RobotArm.get_instance().get_goal_dict()[block.symbol].location == Location.L2:
                    # Check if L1 has any blocks on it; if it does not, find the TABLE block first
                    if len(self.current_state.L2) == 0: # Table block not found yet
                        # Find table block
                        if RobotArm.get_instance().get_goal_dict()[block.symbol].table:
                            table_block = self.current_state.L4[-1] # pull off table block
                            if table_block.state.table: # pick-up if on table, unstack otherwise
                                table_block = self.current_state.L4.pop()
                                Actions.pick_up(table_block)
                                Actions.move(Location.L2)
                                Actions.put_down(table_block, Location.L2)
                                table_block.at_goal = True # Block is at goal state
                                self.current_state.L2.append(table_block)
                                self.reposition()
                                self.get_l2_blocks()
                            else:
                                table_block = self.current_state.L4.pop()
                                Actions.unstack(table_block, self.current_state.L4[-1])
                                Actions.move(Location.L2)
                                Actions.put_down(table_block, Location.L2)
                                self.current_state.L2.append(table_block)
                                table_block.at_goal = True
                                self.reposition()
                                self.get_l2_blocks()
                        else:
                            self.remove_bad_block()
                            self.get_l2_blocks()
                    else:   # Table block already found,
                            # Find the block that goes on the topmost block, put it there
                        top_block = self.current_state.L2[-1]
                        if RobotArm.get_instance().get_goal_dict()[block.symbol].on == top_block.symbol:
                            if block.state.table == True:
                                stack_block = self.current_state.L4.pop()
                                Actions.pick_up(stack_block)
                                Actions.move(Location.L2)
                                Actions.stack(stack_block, self.current_state.L2[-1])
                                stack_block.at_goal = True
                                self.current_state.L2.append(stack_block)
                                self.reposition()
                                self.get_l2_blocks()
                            else:
                                stack_block = self.current_state.L4.pop()
                                Actions.unstack(stack_block, self.current_state.L4[-1])
                                Actions.move(Location.L2)
                                Actions.stack(stack_block, self.current_state.L2[-1])
                                stack_block.at_goal = True
                                self.current_state.L2.append(stack_block)
                                self.reposition()
                                self.get_l2_blocks()
                        else:
                            self.remove_bad_block()
                            self.get_l2_blocks()
                else: # block does not belong on specified location
                    self.remove_bad_block()
                    self.get_l2_blocks()
        else:
            self.reposition()
            if self.stack_at_goal(Location.L2):
                self.l2_complete = True


    '''
    Handle block movement to L3
    '''
    def get_l3_blocks(self):
        if self.block_in_location(Location.L3) and not self.l3_complete: # Check if we have blocks in location
            # Check each block in L4, if it is the table block
            # move it to L3. Otherwise place it on L1 for repositioning
            l4_reverse = list(reversed(self.current_state.L4))
            for block in l4_reverse:
                # If the block has a goal in L3
                if RobotArm.get_instance().get_goal_dict()[block.symbol].location == Location.L3:
                    # Check if L3 has any blocks on it; if it does not, find the TABLE block first
                    if len(self.current_state.L3) == 0: # Table block not found yet
                        # Find table block
                        if RobotArm.get_instance().get_goal_dict()[block.symbol].table:
                            table_block = self.current_state.L4[-1] # pull off table block
                            if table_block.state.table: # pick-up if on table, unstack otherwise
                                table_block = self.current_state.L4.pop()
                                Actions.pick_up(table_block)
                                Actions.move(Location.L3)
                                Actions.put_down(table_block, Location.L3)
                                table_block.at_goal = True # Block is at goal state
                                self.current_state.L3.append(table_block)
                                self.reposition()
                                self.get_l3_blocks()
                            else:
                                table_block = self.current_state.L4.pop()
                                Actions.unstack(table_block, self.current_state.L4[-1])
                                Actions.move(Location.L3)
                                Actions.put_down(table_block, Location.L3)
                                self.current_state.L3.append(table_block)
                                table_block.at_goal = True
                                self.reposition()
                                self.get_l3_blocks()
                        else:
                            self.remove_bad_block_other()
                            self.get_l3_blocks()
                    else:   # Table block already found,
                            # Find the block that goes on the topmost block, put it there
                        top_block = self.current_state.L3[-1]
                        if RobotArm.get_instance().get_goal_dict()[block.symbol].on.symbol == top_block.symbol:
                            if block.state.table == True:
                                stack_block = self.current_state.L4.pop()
                                Actions.pick_up(stack_block)
                                Actions.move(Location.L3)
                                Actions.stack(stack_block, self.current_state.L3[-1])
                                stack_block.at_goal = True
                                self.current_state.L3.append(stack_block)
                                self.reposition()
                                self.get_l3_blocks()
                            else:
                                stack_block = self.current_state.L4.pop()
                                Actions.unstack(stack_block, self.current_state.L4[-1])
                                Actions.move(Location.L3)
                                Actions.stack(stack_block, self.current_state.L3[-1])
                                stack_block.at_goal = True
                                self.current_state.L3.append(stack_block)
                                self.reposition()
                                self.get_l3_blocks()
                        else:
                            self.remove_bad_block_other()
                            self.get_l3_blocks()
                else: # block does not belong on specified location
                    self.remove_bad_block_other()
                    self.get_l3_blocks()
        else:
            self.reposition()
            if self.stack_at_goal(Location.L3):
                self.l3_complete = True

    '''
    Prints out all of the blocks in L4 (For testing purposes)
    '''
    def state_of_l4(self):
        for block in self.current_state.L4:
            block.block_info()
        raise Exception("BREAK HERE")

    '''
    Handle block movement to L4
    '''
    def get_l4_blocks(self):
        # Iterate over all the blocks in L4, find the table block
        # set the table block on L1 and pop all the rest off L4 and stack them on L3
        # When L4 is empty, put down L1 block onto L4
        # Then iterate based on stack order in goal
        if not self.l4_complete and len(self.goal_state.L4) > 1:
            l4_reverse = list(reversed(self.current_state.L4))
            for block in l4_reverse:
                # Find table block
                if RobotArm.get_instance().get_goal_dict()[block.symbol].table and RobotArm.get_instance().get_goal_dict()[block.symbol].location == Location.L4:
                    table_block = self.current_state.L4[-1] # pull off table block
                    if table_block.state.table: # pick-up if on table, unstack otherwise
                        table_block = self.current_state.L4.pop()
                        Actions.pick_up(table_block)
                        Actions.move(Location.L1) # Put table block on L1 for now
                        Actions.put_down(table_block, Location.L1)
                        self.current_state.L1.append(table_block)
                    else:
                        table_block = self.current_state.L4.pop()
                        Actions.unstack(table_block, self.current_state.L4[-1])
                        Actions.move(Location.L1) # Put table block on L1 for now
                        Actions.put_down(table_block, Location.L2)
                        self.current_state.L1.append(table_block)
                    # Now that the table block has been separated, remove the rest of the blocks from L4
                    while len(self.current_state.L4) > 0:
                        if not self.remove_bad_block():
                            break
                    table_block = self.current_state.L1.pop()
                    if len(self.current_state.L1) == 0: # Pick up
                        Actions.pick_up(table_block)
                    else:
                        Actions.unstack(table_block, self.current_state.L1[-1])
                    Actions.move(Location.L4)
                    Actions.put_down(table_block, Location.L4)
                    self.current_state.L4.append(table_block)
                    table_block.at_goal = True
                    table_block.block_info
                    self.reposition()
                    # for block in self.current_state.L3:
                    #     block.block_info()
                    self.get_l4_blocks() # Table block is in place
                elif not self.table_block_found_l4(): # Handle blocks that we haven't dealt with yet if we haven't found table block
                    self.remove_bad_block()
                    self.get_l4_blocks()
                else:
                    # Search for blocks to go on top of the base table block
                    l4_stack = list(reversed(self.current_state.L4))
                    if len(self.goal_state.L4) > 1:
                        for item in l4_stack:
                            if not item.at_goal:
                                move_block = self.current_state.L4.pop()
                                if self.tops_last_goal_l4(move_block):# Check if this block goes on the previous block at goal
                                    Actions.unstack(move_block, self.current_state.L4[-1])
                                    Actions.move(Location.L1)
                                    if len(self.current_state.L1) == 0:
                                        Actions.put_down(move_block, Location.L1)
                                    else:
                                        Actions.stack(move_block, self.current_state.L1[-1])
                                    self.current_state.L1.append(move_block)
                                    # move the rest to L3, then append the block on L1 back to L4 as goal
                                    rev = list(reversed(self.current_state.L4))
                                    for rev_item in rev:
                                        if not rev_item.at_goal:
                                            self.remove_bad_block()
                                    next_block = self.current_state.L1.pop()
                                    if len(self.current_state.L1) == 0:
                                        Actions.pick_up(next_block)
                                    else:
                                        Actions.unstack(next_block, self.current_state.L1[-1])
                                    Actions.move(Location.L4)
                                    Actions.stack(next_block, self.current_state.L4[-1])
                                    self.current_state.L4.append(next_block)
                                    next_block.at_goal = True
                                    # L4 is complete if we have reached the goal state
                                    self.l4_complete = self.goal_state_reached()
                                    next_block.block_info()
                                    self.reposition()
                                    self.get_l4_blocks()
                                else: # If this block does not go on top, move to L3 until we find it
                                    self.remove_bad_block()
                                    self.get_l4_blocks()
        if len(self.goal_state.L4) == 1: # Check if there is only one block at goal state, then check it to make sure it's at goal state
            if (RobotArm.get_instance().get_goal_dict()[self.current_state.L4[-1].symbol].table == self.current_state.L4[-1].state.table
                and RobotArm.get_instance().get_goal_dict()[self.current_state.L4[-1].symbol].location == self.current_state.L4[-1].state.location):
                self.current_state.L4[-1].at_goal = True
        if self.stack_at_goal(Location.L4):
            self.l4_complete = True

    '''
    Checks if this block goes on the most recently "goaled" block
    '''
    def tops_last_goal_l4(self, block):
        rev_list = list(reversed(self.current_state.L4))
        last_top = None
        for item in rev_list: # get first instance of the block at goal on stack
            if item.at_goal:
                last_top = item.symbol
                break
        for item in self.current_state.L4:
            if RobotArm.get_instance().get_goal_dict()[block.symbol].on == last_top:
                return True
        return False

    '''
    Checks if table block has been found for L4
    '''
    def table_block_found_l4(self):
        for block in self.current_state.L4:
            if block.at_goal:
                return True
        return False


    '''
    Iterate over each stack location and move the blocks to L4 to get them to a "default" state.
    '''
    def reposition(self):
        if (not self.l1_complete) and len(self.current_state.L1) > 0: # If L1 has not be solved and there are blocks on it
            if len(self.current_state.L1) > 1: # If there is more than one block on stack
                l1_reverse = list(reversed(self.current_state.L1))
                for item in l1_reverse:
                    # If the next block is at the goal state, leave the loop
                    if self.current_state.L1[-1].at_goal:
                        break
                    block = self.current_state.L1.pop() # Pull block off the stack
                    # If the block is not on the table, unstack. Pick up otherwise
                    if block.state.table == False:
                        Actions.unstack(block, block.state.on)
                    else:
                        Actions.pick_up(block)
                    Actions.move(Location.L4) # Move to Location 4
                    if len(self.current_state.L4) == 0: # Put down if L4 is empty, stack otherwise
                        Actions.put_down(block, Location.L4)
                    else:
                        Actions.stack(block, self.current_state.L4[-1])
                    self.current_state.L4.append(block) # Append block to L4 stack
            else: # There is only one block on stack
                if not self.current_state.L1[-1].at_goal:
                    block = self.current_state.L1.pop() # Pull off block from stack
                    Actions.pick_up(block)
                    Actions.move(Location.L4)
                    if len(self.current_state.L4) == 0: # If there are no blocks on L4, put down. Stack otherwise
                        Actions.put_down(block, Location.L4)
                    else:
                        Actions.stack(block, self.current_state.L4[-1])
                    self.current_state.L4.append(block)

        
        if not self.l2_complete and len(self.current_state.L2) > 0: # If L2 has not be solved and there are blocks on it
            if  len(self.current_state.L2) > 1: # If there is more than one block on stack
                l2_reverse = list(reversed(self.current_state.L2))
                for item in l2_reverse:
                    # If the next block is at the goal state, leave the loop
                    if self.current_state.L2[-1].at_goal:
                        break
                    block = self.current_state.L2.pop() # Pull block off the stack
                    # If the block is not on the table, unstack. Pick up otherwise
                    if block.state.table == False:
                        Actions.unstack(block, block.state.on)
                    else:
                        Actions.pick_up(block)
                    Actions.move(Location.L4) # Move to Location 4
                    if len(self.current_state.L4) == 0: # Put down if L4 is empty, stack otherwise
                        Actions.put_down(block, Location.L4)
                    else:
                        Actions.stack(block, self.current_state.L4[-1])
                    self.current_state.L4.append(block) # Append block to L4 stack
            else: # There is only one block on stack
                if not self.current_state.L2[-1].at_goal:
                    block = self.current_state.L2.pop() # Pull off block from stack
                    Actions.pick_up(block)
                    Actions.move(Location.L4)
                    if len(self.current_state.L4) == 0: # If there are no blocks on L4, put down. Stack otherwise
                        Actions.put_down(block, Location.L4)
                    else:
                        Actions.stack(block, self.current_state.L4[-1])
                    self.current_state.L4.append(block)


        if not self.l3_complete and len(self.current_state.L3) > 0: # If L3 has not be solved and there are blocks on it
            if  len(self.current_state.L3) > 1: # If there is more than one block on stack
                l3_reverse = list(reversed(self.current_state.L3))
                for item in l3_reverse:
                    # If the next block is at the goal state, leave the loop
                    if self.current_state.L3[-1].at_goal:
                        break
                    block = self.current_state.L3.pop() # Pull block off the stack
                    # If the block is not on the table, unstack. Pick up otherwise
                    if block.state.table == False:
                        Actions.unstack(block, block.state.on)
                    else:
                        Actions.pick_up(block)
                    Actions.move(Location.L4) # Move to Location 4
                    if len(self.current_state.L4) == 0: # Put down if L4 is empty, stack otherwise
                        Actions.put_down(block, Location.L4)
                    else:
                        Actions.stack(block, self.current_state.L4[-1])
                    self.current_state.L4.append(block) # Append block to L4 stack
            else: # There is only one block on stack
                if not self.current_state.L3[-1].at_goal:
                    block = self.current_state.L3.pop() # Pull off block from stack
                    Actions.pick_up(block)
                    Actions.move(Location.L4)
                    if len(self.current_state.L4) == 0: # If there are no blocks on L4, put down. Stack otherwise
                        Actions.put_down(block, Location.L4)
                    else:
                        Actions.stack(block, self.current_state.L4[-1])
                    self.current_state.L4.append(block)