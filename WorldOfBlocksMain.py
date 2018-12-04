'''
Driver code for World Of Blocks
'''
import solver.Actions
from utils import Constants
import cocos
from solver.Solver import Solver
from solver.Blocks import Block
from solver.Blocks import Location
from solver.Blocks import State
from solver.Blocks import TableState
from solver.RobotArm import RobotArm
from solver.Drawable import (Table, Title, LocationLabel, BlockSprite, RobotArmSprite,
    InitialStateLabel, GoalStateLabel, SolveButton, GoalStateReachedLabel)
import ctypes

'''
Before running the solver, we want input given from the user.
User gives input at command line and this reads in the information.
'''
def ask_for_user_states():
    print("Welcome to the World of Blocks AI Solver!")
    print("=========================================")
    print("Describe your initial state one block at a time, separated by commas.")
    print("Start with the block on the bottom and work your way upwards.")
    print("There are a total of four locations on the table, L1-L4.")
    print("L1 INITIAL STATE:")
    l1_init = input()
    l1_init_stack = create_stack(l1_init, Location.L1, True)
    print("L2 INITIAL STATE:")
    l2_init = input()
    l2_init_stack = create_stack(l2_init, Location.L2, True)
    print("L3 INITIAL STATE:")
    l3_init = input()
    l3_init_stack = create_stack(l3_init, Location.L3, True)
    print("L4 INITIAL STATE:")
    l4_init = input()
    l4_init_stack = create_stack(l4_init, Location.L4, True)

    print("Next, please input the GOAL STATE")
    print("L1 GOAL STATE:")
    l1_goal = input()
    l1_goal_stack = create_stack(l1_goal, Location.L1)
    print("L2 GOAL STATE:")
    l2_goal = input()
    l2_goal_stack = create_stack(l2_goal, Location.L2)
    print("L3 GOAL STATE:")
    l3_goal = input()
    l3_goal_stack = create_stack(l3_goal, Location.L3)
    print("L4 GOAL STATE:")
    l4_goal = input()
    l4_goal_stack = create_stack(l4_goal, Location.L4)

    # Create the initial and goal states and register them to the robot arm
    initial_state = TableState(l1_init_stack, l2_init_stack, l3_init_stack, l4_init_stack)
    goal_state = TableState(l1_goal_stack, l2_goal_stack, l3_goal_stack, l4_goal_stack)

    # Register these states to the robot arm
    RobotArm.get_instance().register_initial_state(initial_state)
    RobotArm.get_instance().register_goal_state(goal_state)

    # Create the solver, register it to RobotArm, and solve
    solver = Solver(RobotArm.get_instance().get_initial_state(),
                    RobotArm.get_instance().get_goal_state())
    RobotArm.get_instance().register_solver(solver)
    # RobotArm.get_instance().run_solver()

# Get strings from each initial table state based on given location
def get_init_string(loc):
    values = ""
    if loc == Location.L1:
        values = "L1: "
        lst = RobotArm.get_instance().get_initial_state().L1
        for item in lst:
            values += " " + str(item.symbol)
    elif loc == Location.L2:
        values = "L2: "
        lst = RobotArm.get_instance().get_initial_state().L2
        for item in lst:
            values += " " + str(item.symbol)
    elif loc == Location.L3:
        values = "L3: "
        lst = RobotArm.get_instance().get_initial_state().L3
        for item in lst:
            values += " " + str(item.symbol)
    elif loc == Location.L4:
        values = "L4: "
        lst = RobotArm.get_instance().get_initial_state().L4
        for item in lst:
            values += " " + str(item.symbol)

    return values

# Get strings from each goal table state based on given location
def get_goal_string(loc):
    values = ""
    if loc == Location.L1:
        values = "L1: "
        lst = RobotArm.get_instance().get_goal_state().L1
        for item in lst:
            values += " " + str(item.symbol)
    elif loc == Location.L2:
        values = "L2: "
        lst = RobotArm.get_instance().get_goal_state().L2
        for item in lst:
            values += " " + str(item.symbol)
    elif loc == Location.L3:
        values = "L3: "
        lst = RobotArm.get_instance().get_goal_state().L3
        for item in lst:
            values += " " + str(item.symbol)
    elif loc == Location.L4:
        values = "L4: "
        lst = RobotArm.get_instance().get_goal_state().L4
        for item in lst:
            values += " " + str(item.symbol)
    return values

def create_stack(blocks, loc, is_init = False):
    blocks = blocks.replace(" ", "") # Remove all white space
    symbols = blocks.split(",") # delimit by commas
    print("BLOCKS VALUE IS: ", blocks)
    block_stack = []
    # Create blocks and add them to stack
    if blocks == "":
        return []
    for symbol in symbols:
        block = Block(symbol)
        block_stack.append(block)
    
    if len(block_stack) > 0:
        for block in block_stack:
            if block == block_stack[0]: # Handle table block
                block_stack[0].state = State([], None, False, True, loc)
            else:
                idx = block_stack.index(block) # Get the index of the block in the stack
                above_list = []
                count = 0
                while count < idx: # Build the above list
                    above_list.append(block_stack[count])
                    count += 1
                block.state = State(above_list, block_stack[idx - 1], False, False, loc)

        block_stack[-1].state.clear = True # Topmost block is always clear
    if is_init: # Register only the initial state blocks
        for block in block_stack:
            RobotArm.get_instance().register_block_sprite(block)

    return block_stack

class MainLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()

    def update(self, dt):
        self.draw()

# Insertion point for program
if __name__ == "__main__":
    # Initialize the director (a type of game manager, a singleton object)
    cocos.director.director.init(width=Constants.WINDOW_WIDTH, height=Constants.WINDOW_HEIGHT, caption="World of Blocks - AI With Planning")
    # Ask for user input to get states
    ask_for_user_states()

    # Create isntances of the layers
    heading_layer = Title()             # Title
    table_layer = Table()               # Table
    loc_1 = LocationLabel(Location.L1)  # L1 Label
    loc_2 = LocationLabel(Location.L2)  # L2 Label
    loc_3 = LocationLabel(Location.L3)  # L3 Label
    loc_4 = LocationLabel(Location.L4)  # L4 Label

    # State Labels
    init_state_label = InitialStateLabel(get_init_string(Location.L1), get_init_string(Location.L2),get_init_string(Location.L3), get_init_string(Location.L4))
    goal_state_label = GoalStateLabel(get_goal_string(Location.L1), get_goal_string(Location.L2), get_goal_string(Location.L3), get_goal_string(Location.L4))
    goal_state_reached_label = GoalStateReachedLabel()
    goal_state_reached_label.visible = False

    # Solve button
    solve_btn = SolveButton(RobotArm.get_instance())

    arm_layer = RobotArmSprite()        # Robot arm sprite
    RobotArm.get_instance().register_sprite(arm_layer.sprite)

    # Main scene to register to the director
    main_scene = cocos.scene.Scene()
    # Layer to hold everything
    game_layer = MainLayer()
    game_layer.is_event_handler = True


    # Add components
    game_layer.add(heading_layer)
    game_layer.add(table_layer, 1)
    game_layer.add(loc_1, 1)
    game_layer.add(loc_2, 1)
    game_layer.add(loc_3, 1)
    game_layer.add(loc_4, 1)
    game_layer.add(arm_layer, 2)
    game_layer.add(solve_btn, 2)

    # Add blocks from robot arm
    sprites = RobotArm.get_instance().get_sprite_dict()
    for key in sprites:
        game_layer.add(sprites[key], 10)

    # Add state labels
    game_layer.add(init_state_label)
    game_layer.add(goal_state_label)
    game_layer.add(goal_state_reached_label)

    RobotArm.get_instance().register_goal_state_reached_label(goal_state_reached_label)

    # add game layer to main scene
    main_scene.add(game_layer)

    main_scene.schedule_interval(game_layer.update, 1/60)

    RobotArm.get_instance().register_main_scene(main_scene)

    # Run the scene
    cocos.director.director.run(main_scene)