from enum import Enum


class TimeOfDay(Enum):
    ALL = -1
    DAWN = 0
    DAY = 1
    DUSK = 2
    NIGHT = 3
