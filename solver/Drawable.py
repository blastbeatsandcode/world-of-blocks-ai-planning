import cocos
from cocos.actions import *
from cocos.director import director
from utils import Constants
from solver.Blocks import Location
import threading

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

class SolveButton(cocos.layer.Layer):
    # Set this to be able to handle clicks
    is_event_handler = True
    def __init__(self, arm):
        super().__init__()
        self.spr = cocos.sprite.Sprite("res/solve_button.png")
        self.spr.position = 200, Constants.TABLE_Y
        self.arm = arm
        self.add(self.spr)
    
    # Handle when the button is pressed
    def on_mouse_press(self, x, y, button, modifiers):
        print(str(x) + " , " + str(y))
        if x > 75 and x < 325 and y > 50 and y < 145:
            threading.Thread(target=self.arm.run_solver).start()
            #self.arm.run_solver()


# Sprite for the blocks
class RobotArmSprite(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.sprite = cocos.sprite.Sprite("res/robot_arm.png")
        # Set the location of the block
        self.sprite.position = Constants.ROBOT_ARM_X, Constants.ROBOT_ARM_Y
        self.add(self.sprite)

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

# Title layer
class GoalStateReachedLabel(cocos.layer.Layer):
    # Constructor for HelloWorld class
    def __init__(self):
        super().__init__()

        # Label to display
        label = cocos.text.Label(
            'GOAL STATE REACHED!',
            font_name='Arial',
            font_size=32,
            anchor_x='center', anchor_y='center',
            color=(0, 128, 0, 255)
        )

        # Position it at the center of the screen
        label.position = (Constants.WINDOW_WIDTH / 2), (Constants.WINDOW_HEIGHT - 200)

        # Since the label is a subclass of cocosnode it can be added as a child
        self.add(label)


# Initial State Layer
class InitialStateLabel(cocos.layer.Layer):
    def __init__(self, l1_str = "L1: ", l2_str = "L2: ", l3_str = "L3: ", l4_str = "L4: "):
        super().__init__()

        # Strings to show as sub-labels to display initial state
        self.l1_list = l1_str
        self.l2_list = l2_str
        self.l3_list = l3_str
        self.l4_list = l4_str

        # Label to display
        label = cocos.text.Label(
            'Initial State',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center'
        )
        label.position = Constants.INITIAL_STATE_X, Constants.INITIAL_STATE_Y

        # Since the label is a subclass of cocosnode it can be added as a child
        self.add(label)

        l1_label = cocos.text.Label(
            str(self.l1_list),
            font_name='Arial',
            font_size=24,
            anchor_x='left', anchor_y='center'
        )
        l1_label.position = Constants.STATE_VALUE_X, Constants.STATE_VALUE_Y_MAX_INIT - (Constants.STATE_VALUE_SEPARATOR * 0)
        self.add(l1_label)

        l2_label = cocos.text.Label(
            str(self.l2_list),
            font_name='Arial',
            font_size=24,
            anchor_x='left', anchor_y='center'
        )
        l2_label.position = Constants.STATE_VALUE_X, Constants.STATE_VALUE_Y_MAX_INIT - (Constants.STATE_VALUE_SEPARATOR * 1)
        self.add(l2_label)

        l3_label = cocos.text.Label(
            str(self.l3_list),
            font_name='Arial',
            font_size=24,
            anchor_x='left', anchor_y='center'
        )
        l3_label.position = Constants.STATE_VALUE_X, Constants.STATE_VALUE_Y_MAX_INIT - (Constants.STATE_VALUE_SEPARATOR * 2)
        self.add(l3_label)

        l4_label = cocos.text.Label(
            str(self.l4_list),
            font_name='Arial',
            font_size=24,
            anchor_x='left', anchor_y='center'
        )
        l4_label.position = Constants.STATE_VALUE_X, Constants.STATE_VALUE_Y_MAX_INIT - (Constants.STATE_VALUE_SEPARATOR * 3)
        self.add(l4_label)

# Goal State Layer
class GoalStateLabel(cocos.layer.Layer):
    # Constructor for HelloWorld class
    def __init__(self, l1_str = "", l2_str = "", l3_str = "", l4_str = ""):
        super().__init__()

        # Strings to show as sub-labels to display goal state
        self.l1_list = l1_str
        self.l2_list = l2_str
        self.l3_list = l3_str
        self.l4_list = l4_str

        # Label to display
        label = cocos.text.Label(
            'Goal State',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center'
        )
        label.position = Constants.GOAL_STATE_X, Constants.GOAL_STATE_Y
        self.add(label)

        l1_label = cocos.text.Label(
            str(self.l1_list),
            font_name='Arial',
            font_size=24,
            anchor_x='left', anchor_y='center'
        )
        l1_label.position = Constants.STATE_VALUE_X, Constants.STATE_VALUE_Y_MAX_GOAL - (
                    Constants.STATE_VALUE_SEPARATOR * 0)
        self.add(l1_label)

        l2_label = cocos.text.Label(
            str(self.l2_list),
            font_name='Arial',
            font_size=24,
            anchor_x='left', anchor_y='center'
        )
        l2_label.position = Constants.STATE_VALUE_X, Constants.STATE_VALUE_Y_MAX_GOAL  - (
                    Constants.STATE_VALUE_SEPARATOR * 1)
        self.add(l2_label)

        l3_label = cocos.text.Label(
            str(self.l3_list),
            font_name='Arial',
            font_size=24,
            anchor_x='left', anchor_y='center'
        )
        l3_label.position = Constants.STATE_VALUE_X, Constants.STATE_VALUE_Y_MAX_GOAL  - (
                    Constants.STATE_VALUE_SEPARATOR * 2)
        self.add(l3_label)

        l4_label = cocos.text.Label(
            str(self.l4_list),
            font_name='Arial',
            font_size=24,
            anchor_x='left', anchor_y='center'
        )
        l4_label.position = Constants.STATE_VALUE_X, Constants.STATE_VALUE_Y_MAX_GOAL  - (
                    Constants.STATE_VALUE_SEPARATOR * 3)
        self.add(l4_label)