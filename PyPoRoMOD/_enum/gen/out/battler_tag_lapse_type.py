from enum import Enum


class BattlerTagLapseType(Enum):
    FAINT = 0
    MOVE = 1
    PRE_MOVE = 2
    AFTER_MOVE = 3
    MOVE_EFFECT = 4
    TURN_END = 5
    CUSTOM = 6
