'''
Driver code for World Of Blocks
'''
import Actions
import cocos
from Solver import Solver
from Blocks import Block
from Blocks import Location
from RobotArm import RobotArm
from Blocks import State
from Blocks import TableState

#TODO: Look into creating a singleton object within cocos2d that maybe we can use to reference the blocks and the robot arm
#       This can be initialized in the driver program then, to keep track of whether the robot arm is holding a block or not

# Subclass a Layer and define the logic of the program here:
class HelloWorld(cocos.layer.Layer):
    # Constructor for HelloWorld class
    def __init__(self):
        super(HelloWorld, self).__init__()

        # Label to display
        label = cocos.text.Label(
            'World of Blocks Artificial Intelligence',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center'
        )

        # Position it at the center of the screen
        label.position = 640, 360

        # Since the label is a subclass of cocosnode it can be added as a child
        self.add(label)

# # Simple testing to see if actions work properly
# def abc_test():
#     # Get the blocks from robot arm
#     block_a = Block("A", Location.L1)
#     block_b = Block("B", Location.L1)
#     block_c = Block("C", Location.L1)

#     # THIS WILL BE THE GOAL STATE
#     # Make copies of the original location of A B and C
#     block_a_copy = Block(block_a.symbol, block_a.location)
#     block_b_copy = Block(block_b.symbol, block_b.location)
#     block_c_copy = Block(block_c.symbol, block_c.location)
    
#     # Give the blocks attributes to stack in order on L1, with A on top, B in the middle, C on table
#     block_a.state = State([block_c, block_b], block_b, True, False)
#     block_b.state = State([block_c], block_c, False, False)
#     block_c.state = State([], None, False, True)

#     # Set the States of these blocks to be A B C in order, with C being on the table
#     block_a_copy.state = State([block_c_copy, block_b_copy], block_b_copy, True, False)
#     block_b_copy.state = State([block_c_copy], block_c_copy, False, False)
#     block_c_copy.state = State([], None, False, True)

#     # Attempt to unstack A from the stack, move it to L4, and put it down
#     print("MOVE A TO L4 ===============")
#     Actions.unstack(block_a, block_b)
#     Actions.move(Location.L4)
#     Actions.put_down(block_a, Location.L4)

#     # Then move B from C to top of A
#     print("MOVE B TO TOP OF A =========")
#     Actions.unstack(block_b, block_c)
#     Actions.move(Location.L4)
#     Actions.stack(block_b, block_a)

#     # move C to L2
#     print("MOVE C TO L2 ===============")
#     Actions.pick_up(block_c)
#     Actions.move(Location.L2)
#     Actions.put_down(block_c, Location.L2)

#     # Test these combinations, should NOT be a match:
#     RobotArm.get_instance().register_initial_state([block_a, block_b, block_c])
#     RobotArm.get_instance().register_goal_state([block_a_copy, block_b_copy, block_c_copy])
#     print("IS GOAL REACHED? ", RobotArm.get_instance().is_goal_state_reached()) # Should be False
#     RobotArm.get_instance().register_goal_state([block_a, block_b, block_c])
#     print("NOW IS GOAL REACHED? ", RobotArm.get_instance().is_goal_state_reached()) # Should be True

#     RobotArm.get_instance().register_initial_state([block_a_copy, block_b_copy, block_c_copy])
#     print("A: ", str(block_a_copy.location))
#     print("B: ", str(block_b_copy.location))
#     print("C: ", str(block_c_copy.location))
#     RobotArm.get_instance().register_goal_state([block_a, block_b, block_c])
#     print("A: ", str(block_a.location))
#     print("B: ", str(block_b.location))
#     print("C: ", str(block_c.location))

#     print("Original state. . .")
#     RobotArm.get_instance().get_initial_state()[0].block_info()
#     RobotArm.get_instance().get_initial_state()[1].block_info()
#     RobotArm.get_instance().get_initial_state()[2].block_info()

#     # Do exhaustive search
#     path_finder = Pathfinder(RobotArm.get_instance().get_initial_state(),
#         RobotArm.get_instance().get_goal_state())
#     path_finder.exhaustive_search()

#     print("New State . . .")
#     RobotArm.get_instance().get_initial_state()[0].block_info()
#     RobotArm.get_instance().get_initial_state()[1].block_info()
#     RobotArm.get_instance().get_initial_state()[2].block_info()

# Create some test states
def create_states_test():
    # Create some blocks
    block_a = Block("A", Location.L1)
    block_b = Block("B", Location.L1)
    block_c = Block("C", Location.L1)

    # Make copies of the original location of A B and C
    block_a_copy = Block(block_a.symbol, block_a.location)
    block_b_copy = Block(block_b.symbol, block_b.location)
    block_c_copy = Block(block_c.symbol, block_c.location)
    
    # Give the blocks attributes to stack in order on L1, with A on top, B in the middle, C on table (initial state)
    ''' UNCOMMENT FOR L1 STACK
    block_a.state = State([block_c, block_b], block_b, True, False)
    block_b.state = State([block_c], block_c, False, False)
    block_c.state = State([], None, False, True)
    '''

    ''' UNCOMMENT FOR SPREAD OUT STACK '''
    block_a.location = Location.L1
    block_b.location = Location.L2
    block_c.location = Location.L3
    block_a.state = State([], None, True, True)
    block_b.state = State([], None, True, True)
    block_c.state = State([], None, True, True)
    

    # Set A at L4 on the table, with B on top, and C at L2 (goal state)
    block_a_copy.location = Location.L4
    block_b_copy.location = Location.L4
    block_c_copy.location = Location.L2
    block_a_copy.state = State([], None, False, True)                       # L4, On Table
    block_b_copy.state = State([block_a_copy], block_c_copy, True, False)   # L4, On A
    block_c_copy.state = State([], None, True, True)                        # L2, On Table

    # State we start with and state we end with
    l1 = [block_c, block_b, block_a]
    l2 = []
    l3 = []
    l4 = []
    initial_state = TableState(l1, l2, l3, l4)
    l1 = []
    l2 = [block_c_copy]
    l3 = []
    l4 = [block_a_copy, block_b_copy]
    goal_state = TableState(l1, l2, l3, l4)

    # Register these states to the robot arm
    RobotArm.get_instance().register_initial_state(initial_state)
    RobotArm.get_instance().register_goal_state(goal_state)

    # Create the solver, register it to RobotArm, and solve
    solver = Solver(RobotArm.get_instance().get_initial_state(),
                    RobotArm.get_instance().get_goal_state())
    RobotArm.get_instance().register_solver(solver)
    RobotArm.get_instance().run_solver()

# Insertion point for program
if __name__ == "__main__":
    # Initialize the director (a type of game manager, a singleton object)
    cocos.director.director.init(width=1280, height=720, caption="World of Blocks - AI With Planning")

    #Create an instance of the hello world in a layer
    hello_layer = HelloWorld()

    # Create a scene that contains the layer we just created as a child
    main_scene = cocos.scene.Scene(hello_layer)

    # Run the scene
    # cocos.director.director.run(main_scene)




    '''
    DOING SOME TESTING HERE
    '''
    #abc_test()
    create_states_test()
