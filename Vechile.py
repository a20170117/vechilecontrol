from Events import *

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif isinstance(self.value, args): # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

class Vechile:
    """
    用于执行控制指令，控制硬件。
    不同硬件设备继承本类分别实现。
    """
    def event(self, e: Event):
        for case in switch(e):
            if case(Stop):
                self.stop(e)
                break
            if case(MoveForward):
                self.move_forward(e)
                break
            if case(MoveRight):
                self.move_right(e)
                break
            if case(Turn):
                self.turn(e)
                break
            if case(LookUp):
                self.look_up(e)
                break
            if case(TurnRate):
                self.turn_rate(e)
                break
            if case(LookUpRate):
                self.look_up_rate(e)
                break
            if case():
                break

    def stop(self, e: Stop):
        print("stop: ", e.value)

    def move_forward(self, e: MoveForward):
        print("move forward: ", e.value)
        
    def move_right(self, e: MoveRight):
        print("move right: ", e.value)

    def turn(self, e: Turn):
        print("turn: ", e.value)

    def look_up(self, e: Turn):
        print("look up: ", e.value)

    def turn_rate(self, e: Turn):
        print("turn_rate: ", e.value)
    
    def look_up_rate(self, e: Turn):
        print("look up rate: ", e.value)

if __name__ == '__main__':
    v = Vechile()
    v.event(Stop(0.0))
