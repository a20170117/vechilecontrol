from Events import *
from Vechile import Vechile

class Caterpillar(Vechile):
    
    def move_forward(self, e: MoveForward):
        """
        e.value 正为前进，负为后退，零为取消当前动作。
        """
        pass

    def turn(self, e: Turn):
        """
        e.value 负为左转，正为右转，零为取消当前动作。
        """
        pass

    def stop(self, e: Stop):
        """
        e.value 1为强制停止，0为取消强制停止。强制停止时应忽略其他输入。
        """
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