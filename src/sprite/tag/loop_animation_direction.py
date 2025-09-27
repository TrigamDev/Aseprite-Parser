from enum import IntEnum


class LoopAnimationDirection(IntEnum):
    Unknown = -1
    Forward = 0
    Reverse = 1
    PingPong = 2
    PingPongReverse = 3
