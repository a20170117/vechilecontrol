class Event:
    def __init__(self):
        self.param = 0.0

class Motion(Event):
    '''
    动作事件
    '''
    def __init__(self, value: float):
        self.__value = value # 动作幅度
    
    @property
    def value(self):
        '''
        获取动作幅度，默认不提供setter
        '''
        return self.__value

class Stop(Motion):
    pass

class MoveForward(Motion):
    pass

class MoveRight(Motion):
    pass

class Turn(Motion):
    pass

class LookUp(Motion):
    pass

class TurnRate(Motion):
    pass

class LookUpRate(Motion):
    pass


__all__=["Event", "Motion", "MoveForward", "MoveRight", "Turn", "LookUp", "TurnRate", "LookUpRate", "Stop"]