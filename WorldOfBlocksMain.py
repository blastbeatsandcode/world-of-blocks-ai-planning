'''
Driver code for World Of Blocks
'''
import cocos
import Actions
from Blocks import Block
from Blocks import Location
from RobotArm import RobotArm
from Blocks import State

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

# Simple testing to see if actions work properly
def abc_test():
    RobotArm.get_instance().register_block(Block("A", Location.L1))
    RobotArm.get_instance().register_block(Block("B", Location.L1))
    RobotArm.get_instance().register_block(Block("C", Location.L1))

    # Get the blocks from robot arm
    block_a = RobotArm.get_instance().get_registered_blocks()[0]
    block_b = RobotArm.get_instance().get_registered_blocks()[1]
    block_c = RobotArm.get_instance().get_registered_blocks()[2]


    # Give the blocks attributes to stack in order on L1, with A on top, B in the middle, C on table
    block_a.state = State([block_c, block_b], block_b, True, False)
    block_b.state = State([block_c], block_c, False, False)
    block_c.state = State([], None, False, True)

    # Attempt to unstack A from the stack, move it to L4, and put it down
    print("MOVE A TO L4 ===============")
    Actions.unstack(block_a, block_b)
    Actions.move(Location.L4)
    Actions.put_down(block_a, Location.L4)

    # Then move B from C to top of A
    print("MOVE B TO TOP OF A =========")
    Actions.unstack(block_b, block_c)
    Actions.move(Location.L4)
    Actions.stack(block_b, block_a)

    # move C to L2
    print("MOVE C TO L2 ===============")
    Actions.pick_up(block_c)
    Actions.move(Location.L2)
    Actions.put_down(block_c, Location.L2)


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
        abc_test()
