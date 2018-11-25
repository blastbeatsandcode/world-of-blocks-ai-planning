import cocos

# Subclass a Layer and define the logic of the program here:
class HelloWorld(cocos.layer.Layer):
    # Constructor for HelloWorld class
    def __init__(self):
        super(HelloWorld, self).__init__()

        # Label to display
        label = cocos.text.Label(
            'Hello, world!',
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
        cocos.director.director.run(main_scene)