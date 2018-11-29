'''
Pathfinding elements to carry out the problem solving.
'''
import Actions

class Pathfinder:
    # Holds initial state blocks and goal state blocks
    def __init__(self, init_state_blocks, goal_state_blocks):
        self.init_state = init_state_blocks     # Initial state blocks
        self.goal_state = goal_state_blocks     # Goal state blocks
        self.table_blocks = []                  # Blocks which will be on the table in goal state


    # Takes in a list of blocks 
    def exhaustive_search(self):
        # Get all blocks that will be directly on the table.
        self.__generate_table_blocks()

        # TODO: HANDLE ABOVE/ON BLOCKS (move the blocks on top of the table block?)
        # For each block in the table list, run all functions until we get a desired path.
        while self.table_blocks > 0: # keep doing this until we have emptied the table list
            for block in self.table_blocks:
                for init_block in self.init_state: # Find the initial state block that matches
                    if init_block.symbol == block.symbol: # And run the actions on it
                        self.__run_all_actions(init_block, block.location)

    # Add blocks on table in goal state to table blocks list
    def __generate_table_blocks(self):
        for block in self.goal_state:
            if block.state.table:
                self.table_blocks.append(block)

    # Run all actions on the given block
    def __run_all_actions(self, block, end_location):
        '''
        Run all actions
        '''
        # Save a copy of the original block
        original_block = block

        # # Handle Move
        # if Actions.move(end_location):
        #     print("MOVE WAS TRUE ", original_block.symbol)
        #     if 
        #     self.__run_all_actions(block, end_location)

        # Handle Unstack
        for other_block in self.init_state:
            if other_block != block:
                if Actions.unstack(block, other_block):
                    print("UNSTACK WAS TRUE ", original_block.symbol)
                    Actions.move(end_location)

        # Handle Stack
        for other_block in self.init_state:
            if other_block != block:
                if Actions.stack(block, other_block):
                    print("STACK WAS TRUE ", original_block.symbol)

        # Handle Pick Up
        if Actions.pick_up(block):
            print("PICK UP WAS TRUE ", original_block.symbol)
            Actions.move(end_location)


        # Handle Put Down
        if Actions.put_down(block, end_location):
            print("PUT DOWN WAS TRUE ", original_block.symbol)

