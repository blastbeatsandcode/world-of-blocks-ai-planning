'''
RobotArm.py contains definitions and attributes pertaining to the Robot Arm
'''
# TODO: Define Actions the arm can perform (Pickup, put down?) Or will this be covered in Actions.py?
# TODO: Define States of the arm (HOLDING, NOT HOLDING)
from enum import Enum

'''
RobotArm acts as the robot arm that will be used to manage the blocks in the World of Blocks problem.
RobotArm is a SINGLETON object
'''
class RobotArm:
    # Store the instance
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method """
        if RobotArm.__instance == None:
            RobotArm()
        return RobotArm.__instance

    # Private Constructor for the robot arm
    # Initially, the arm is empty and is not holding a block
    def __init__(self):
        if RobotArm.__instance != None:
            raise Exception("RobotArm is a singleton class.")
        else:
            self.__state = ArmState.EMPTY
            self.__block = None
            self.__blocks = []      # List of all registered blocks
            RobotArm.__instance = self

    # The arm should only grab a block if the arm is already empty
    def grab_block(self, block):
        if self.__state == ArmState.EMPTY:
            self.__block = block
            self.__state = ArmState.HOLDING

    # The arm shoudl only release a block if the arm has the block in its hands
    def release_block(self):
        if self.__state == ArmState.HOLDING:
            self.__block = None
            self.__state = ArmState.EMPTY

    # Return the arm state
    def get_state(self):
        return self.__state

    # Return the block that the arm is holding
    def get_block(self):
        return self.__block

    # Return list of registered blocks
    def get_registered_blocks(self):
        return self.__blocks

    # Register a block to add it to the list
    def register_block(self, block):
        self.__blocks.append(block)

    # Returns if any block is on the given table location
    def is_location_empty(self, table_loc):
        for block in self.__blocks:
            # If a block is in the location and it is not currently being held by the robot arm, return false
            if block.location == table_loc and block != RobotArm.get_instance().get_block():
                return False
        return True


'''
ArmState is an Enum that defines whether the robot arm is holding a block or not.
'''
class ArmState(Enum):
    HOLDING = 1
    EMPTY = 0