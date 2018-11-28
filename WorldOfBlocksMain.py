'''
Driver code for World Of Blocks
'''
import cocos
from Blocks import Block
from Blocks import Location
from RobotArm import RobotArm

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
        # Create some blocks
        blocks = []

        for i in range (0, 3):
            blocks.append(Block(i, Location.L3))

        for block in blocks:
            print("Symbol: " + block.symbol + " Location: " + block.location.value)

        print(RobotArm.get_instance().get_state())