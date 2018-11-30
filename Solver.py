'''
Pathfinding elements to carry out the problem solving.
'''
import Actions
from Blocks import Location

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

    '''
    Solve the World of Blocks problem.
    '''
    def solve(self):
        # Get all blocks to the default position
        self.reposition()

    '''
    Iterate over each stack location and move the blocks to L4 to get them to a "default" state.
    '''
    def reposition(self):
        if not self.l1_complete and len(self.current_state.L1) > 0:
            if not len(self.current_state.L1) == 1:
                for item in self.current_state.L1:
                    # If the next block is at the goal state, leave the loop
                    if self.current_state.L1[-1].at_goal:
                        break
                    block = self.current_state.L1.pop()
                    if Actions.unstack(block, block.state.on): # Attempt to Unstack
                        Actions.move(Location.L4)
                        if Actions.put_down(block, Location.L4): # Attempt put down on table
                            self.current_state.L4.append(block) # Add block to the stack
                        elif Actions.stack(block, self.current_state.L4[-1]): # Attempt to stack
                            self.current_state.L4.append(block)

            # Get block from bottom of stack
            if not self.current_state.L1[0].at_goal:
                block = self.current_state.L1.pop()
                if Actions.pick_up(block):
                    Actions.move(Location.L4)
                if Actions.put_down(block, Location.L4): # Attempt put down on table
                    self.current_state.L4.append(block) # Add block to the stack
                elif Actions.stack(block, self.current_state.L4[-1]): # Attempt to stack
                    self.current_state.L4.append(block)

        if not self.l2_complete and len(self.current_state.L2) > 0:
            if not len(self.current_state.L2) == 1:
                for item in self.current_state.L2:
                    # If the next block is at the goal state, leave the loop
                    if self.current_state.L2[-1].at_goal:
                        break
                    block = self.current_state.L2.pop()
                    if Actions.unstack(block, block.state.on): # Attempt to Unstack
                        Actions.move(Location.L4)
                        if Actions.put_down(block, Location.L4): # Attempt put down on table
                            self.current_state.L4.append(block) # Add block to the stack
                        elif Actions.stack(block, self.current_state.L4[-1]): # Attempt to stack
                            self.current_state.L4.append(block)

            # Get block from bottom of stack
            if not self.current_state.L2[0].at_goal:
                block = self.current_state.L2.pop()
                if Actions.pick_up(block):
                    Actions.move(Location.L4)
                if Actions.put_down(block, Location.L4): # Attempt put down on table
                    self.current_state.L4.append(block) # Add block to the stack
                elif Actions.stack(block, self.current_state.L4[-1]): # Attempt to stack
                    self.current_state.L4.append(block)

        if not self.l3_complete  and len(self.current_state.L3) > 0:
            if not len(self.current_state.L3) == 1:
                for item in self.current_state.L3:
                    # If the next block is at the goal state, leave the loop
                    if self.current_state.L3[-1].at_goal:
                        break
                    block = self.current_state.L3.pop()
                    if Actions.unstack(block, block.state.on): # Attempt to Unstack
                        Actions.move(Location.L4)
                        if Actions.put_down(block, Location.L4): # Attempt put down on table
                            self.current_state.L4.append(block) # Add block to the stack
                        elif Actions.stack(block, self.current_state.L4[-1]): # Attempt to stack
                            self.current_state.L4.append(block)

            # Get block from bottom of stack
            if not self.current_state.L3[0].at_goal:
                block = self.current_state.L3.pop()
                if Actions.pick_up(block):
                    Actions.move(Location.L4)
                if Actions.put_down(block, Location.L4): # Attempt put down on table
                    self.current_state.L4.append(block) # Add block to the stack
                elif Actions.stack(block, self.current_state.L4[-1]): # Attempt to stack
                    self.current_state.L4.append(block)

        # This is for testing purposes
        for block in self.current_state.L4:
            block.block_info()