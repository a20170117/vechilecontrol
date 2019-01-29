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
    def event(self, e: Event, value: float):
        for case in switch(e):
            if case(Stop):
                self.stop(e, value)
                break
            if case(MoveForward):
                self.move_forward(e, value)
                break
            if case(MoveRight):
                self.move_right(e, value)
                break
            if case(Turn):
                self.turn(e, value)
                break
            if case(LookUp):
                self.look_up(e, value)
                break
            if case(TurnRate):
                self.turn_rate(e, value)
                break
            if case(LookUpRate):
                self.look_up_rate(e, value)
                break
            if case():
                break

    def stop(self, e: Stop, value: float):
        print("stop: ", value)

    def move_forward(self, e: MoveForward, value: float):
        print("move forward: ", value)
        
    def move_right(self, e: MoveRight, value: float):
        print("move right: ", value)

    def turn(self, e: Turn, value: float):
        print("turn: ", value)

    def look_up(self, e: Turn, value: float):
        print("look up: ", value)

    def turn_rate(self, e: Turn, value: float):
        print("turn_rate: ", value)
    
    def look_up_rate(self, e: Turn, value: float):
        print("look up rate: ", value)

if __name__ == '__main__':
    v = Vechile()
    v.event(Stop(),0)
