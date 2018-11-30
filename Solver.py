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


    # # Takes in a list of blocks
    # # PROBABLY WON'T USE THIS ANYMORE
    # def exhaustive_search(self):
    #     # Get all blocks that will be directly on the table.
    #     self.__generate_table_blocks()

    #     # TODO: HANDLE ABOVE/ON BLOCKS (move the blocks on top of the table block?)
    #     # For each block in the table list, run all functions until we get a desired path.
    #     #while len(self.table_blocks) > 0: # keep doing this until we have emptied the table list
        
    #     for block in self.table_blocks:
    #         for init_block in self.init_state: # Find the initial state block that matches
    #             if init_block.symbol == block.symbol: # And run the actions on it
    #                 self.__run_all_actions(init_block, block.location)


    # Add blocks on table in goal state to table blocks list
    # PROBABLY WON'T USE THIS ANYMORE
    # def __generate_table_blocks(self):
    #     for block in self.goal_state:
    #         if block.state.table:
    #             self.table_blocks.append(block)

    # Run all actions on the given block
    # PROBABLY WON'T USE THIS ANYMORE
    # def __run_all_actions(self, block, end_location):
    #     '''
    #     Run all actions
    #     '''
    #     # Save a copy of the original block
    #     original_block = block

    #     # # Handle Move
    #     # if Actions.move(end_location):
    #     #     print("MOVE WAS TRUE ", original_block.symbol)
    #     #     if 
    #     #     self.__run_all_actions(block, end_location)

    #     # Handle Unstack
    #     for other_block in self.init_state:
    #         if other_block != block:
    #             if Actions.unstack(block, other_block):
    #                 print("UNSTACK WAS TRUE ", original_block.symbol)
    #                 Actions.move(end_location)

    #     # Handle Stack
    #     for other_block in self.init_state:
    #         if other_block != block:
    #             if Actions.stack(block, other_block):
    #                 print("STACK WAS TRUE ", original_block.symbol)

    #     # Handle Pick Up
    #     if Actions.pick_up(block):
    #         print("PICK UP WAS TRUE ", original_block.symbol)
    #         Actions.move(end_location)


    #     # Handle Put Down
    #     if Actions.put_down(block, end_location):
    #         print("PUT DOWN WAS TRUE ", original_block.symbol)

