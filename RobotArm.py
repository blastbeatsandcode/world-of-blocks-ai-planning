'''
RobotArm.py contains definitions and attributes pertaining to the Robot Arm
'''
# TODO: Define Actions the arm can perform (Pickup, put down?) Or will this be covered in Actions.py?
# TODO: Define States of the arm (HOLDING, NOT HOLDING)
from enum import Enum

'''
RobotArm acts as the robot arm that will be used to manage the blocks in the World of Blocks problem.
'''
class RobotArm():
    # Constructor for the robot arm
    # Initially, the arm is empty and is not holding a block
    def __init__(self):
        self.__state = ArmState.EMPTY
        self.__block = None

    # The arm should only grab a block if the arm is already empty
    def grab_block(self, block):
        if self.__state == ArmState.EMPTY:
            self.__block = block
            self.__state = ArmState.HOLDING

    # The arm shoudl only release a block if the arm has the block in its hands
    def release_block(self):
        if self.__state == ArmState.HOLDING:
            self.__block = None
            self.__state = ArmState.HOLDING


'''
ArmState is an Enum that defines whether the robot arm is holding a block or not.
'''
class ArmState(Enum):
    HOLDING = 1
    EMPTY = 0