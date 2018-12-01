import cocos
from cocos.director import director
from utils import Constants
from solver.Blocks import Location

# Sprite for the table
class Table(cocos.layer.Layer):
    def __init__(self):
        super().__init__()

        spr = cocos.sprite.Sprite("res/table.png")
        # Set the location of the table
        spr.position = Constants.TABLE_X, Constants.TABLE_Y
        self.add(spr)

# Sprite for the blocks
class BlockSprite(cocos.layer.Layer):
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol
        self.spr = cocos.sprite.Sprite("res/block.png")
        # Set the location of the block
        self.spr.position = Constants.L1_X, Constants.BLOCK_TABLE_HEIGHT

        self.add(self.spr)
        self.label = cocos.text.Label(
                symbol,
                font_name='Arial',
                font_size=32,
                anchor_x='center', anchor_y='center',
                color = (0, 0, 0, 255)
        )
        self.label.position = self.spr.position
        self.add(self.label, 2)

    # Sets y coordinate of the block based on the height in the stack
    def set_y(self, height):
        new_height = Constants.BLOCK_TABLE_HEIGHT + (Constants.BLOCK_HEIGHT * height)
        self.spr.position = self.spr.position[0], new_height
        self.label.position = self.label.position[0], new_height
    
    # Sets the X location of the block based on the location on table
    def set_x(self, location):
        if location == Location.L1:
            self.spr.position = Constants.L1_X, self.spr.position[1]
            self.label.position = Constants.L1_X, self.label.position[1]
        elif location == Location.L2:
            self.spr.position = Constants.L2_X, self.spr.position[1]
            self.label.position = Constants.L2_X, self.label.position[1]
        elif location == Location.L3:
            self.spr.position = Constants.L3_X, self.spr.position[1]
            self.label.position = Constants.L3_X, self.label.position[1]
        elif location == Location.L4:
            self.spr.position = Constants.L4_X, self.spr.position[1]
            self.label.position = Constants.L4_X, self.label.position[1]
        else:
            raise Exception("Invalid location given!")


# Sprite for the blocks
class RobotArmSprite(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        
        spr = cocos.sprite.Sprite("res/robot_arm.png")
        # Set the location of the block
        spr.position = Constants.ROBOT_ARM_X, Constants.ROBOT_ARM_Y
        self.add(spr)

# Layer for the location labels
class LocationLabel(cocos.layer.Layer):
    def __init__(self, location):
        super().__init__()
        if location == Location.L1:
            # Label to display
            label = cocos.text.Label(
                'L1',
                font_name='Arial',
                font_size=32,
                anchor_x='center', anchor_y='center'
            )
            # Position it at the center of the screen
            label.position = Constants.L1_X, Constants.L_Y

            # Since the label is a subclass of cocosnode it can be added as a child
            self.add(label)
        elif location == Location.L2:
            # Label to display
            label = cocos.text.Label(
                'L2',
                font_name='Arial',
                font_size=32,
                anchor_x='center', anchor_y='center'
            )
            # Position it at the center of the screen
            label.position = Constants.L2_X, Constants.L_Y

            # Since the label is a subclass of cocosnode it can be added as a child
            self.add(label)
        elif location == Location.L3:
            # Label to display
            label = cocos.text.Label(
                'L3',
                font_name='Arial',
                font_size=32,
                anchor_x='center', anchor_y='center'
            )
            # Position it at the center of the screen
            label.position = Constants.L3_X, Constants.L_Y

            # Since the label is a subclass of cocosnode it can be added as a child
            self.add(label)
        elif location == Location.L4:
            # Label to display
            label = cocos.text.Label(
                'L4',
                font_name='Arial',
                font_size=32,
                anchor_x='center', anchor_y='center'
            )
            # Position it at the center of the screen
            label.position = Constants.L4_X, Constants.L_Y

            # Since the label is a subclass of cocosnode it can be added as a child
            self.add(label)
        else:
            raise Exception("Invalid location provided!")

# Title layer
class Title(cocos.layer.Layer):
    # Constructor for HelloWorld class
    def __init__(self):
        super(Title, self).__init__()

        # Label to display
        label = cocos.text.Label(
            'World of Blocks Artificial Intelligence',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center'
        )

        # Position it at the center of the screen
        label.position = (Constants.WINDOW_WIDTH / 2), (Constants.WINDOW_HEIGHT - 50)

        # Since the label is a subclass of cocosnode it can be added as a child
        self.add(label)

# Initial State Layer
class InitialStateLabel(cocos.layer.Layer):
    # Constructor for HelloWorld class
    def __init__(self):
        super().__init__()

        # Label to display
        label = cocos.text.Label(
            'Initial State',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center'
        )

        # Position it at the center of the screen
        label.position = Constants.INITIAL_STATE_X, Constants.INITIAL_STATE_Y

        # Since the label is a subclass of cocosnode it can be added as a child
        self.add(label)

# Goal State Layer
class GoalStateLabel(cocos.layer.Layer):
    # Constructor for HelloWorld class
    def __init__(self):
        super().__init__()

        # Label to display
        label = cocos.text.Label(
            'Goal State',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center'
        )

        # Position it at the center of the screen
        label.position = Constants.GOAL_STATE_X, Constants.GOAL_STATE_Y

        # Since the label is a subclass of cocosnode it can be added as a child
        self.add(label)