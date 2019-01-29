class Event:
    def __init__(self):
        self.param = 0.0

class Stop(Event):
    pass

class MoveForward(Event):
    pass

class MoveRight(Event):
    pass

class Turn(Event):
    pass

class LookUp(Event):
    pass

class TurnRate(Event):
    pass

class LookUpRate(Event):
    pass


__all__=["Event", "MoveForward", "MoveRight", "Turn", "LookUp", "TurnRate", "LookUpRate", "Stop"]