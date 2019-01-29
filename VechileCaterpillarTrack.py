from Events import *
from Vechile import Vechile

class Caterpillar(Vechile):
    
    def move_forward(self, e: MoveForward, value: float):
        """
        value 正为前进，负为后退
        """
        pass

    def turn(self, e: Turn, value: float):
        """
        value 负为左转，正为右转
        """
        pass

    def stop(self, e: Stop, value: float):
        pass

    def __forward(self):
        pass
    
    def __backward(self):
        pass
    
    def __turn_left(self):
        pass
    
    def __turn_right(self):
        pass
    
    def __stop(self):
        pass