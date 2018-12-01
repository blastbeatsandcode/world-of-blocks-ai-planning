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
        spr.position = Constants.TABLE_WIDTH_LOCATION, Constants.TABLE_HEIGHT_LOCATION
        self.add(spr)

# Sprite for the blocks
class BlockSprite(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        print("Create block sprite")

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
            label.position = Constants.L1_WIDTH_LOCATION, Constants.LOC_HEIGHT_LOCATION

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
            label.position = Constants.L2_WIDTH_LOCATION, Constants.LOC_HEIGHT_LOCATION

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
            label.position = Constants.L3_WIDTH_LOCATION, Constants.LOC_HEIGHT_LOCATION

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
            label.position = Constants.L4_WIDTH_LOCATION, Constants.LOC_HEIGHT_LOCATION

            # Since the label is a subclass of cocosnode it can be added as a child
            self.add(label)
        else:
            raise Exception("Invalid location provided!")

# Subclass a Layer and define the logic of the program here:
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