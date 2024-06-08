from enum import Enum


class Achievements(Enum):
    """
    Src Code: https://github.com/pagefaultgames/pokerogue/blob/46dc7e9b01ee94bd8905e1ebbe260bb523884791/src/system/achv.ts#L219C1-L260C3
    """

    _10K_MONEY = 0
    _100K_MONEY = 1
    _1M_MONEY = 2
    _10M_MONEY = 3
    _250_DMG = 4
    _1000_DMG = 5
    _2500_DMG = 6
    _10000_DMG = 7
    _250_HEAL = 8
    _1000_HEAL = 9
    _2500_HEAL = 10
    _10000_HEAL = 11
    LV_100 = 12
    LV_250 = 13
    LV_1000 = 14
    _10_RIBBONS = 15
    _25_RIBBONS = 16
    _50_RIBBONS = 17
    _75_RIBBONS = 18
    _100_RIBBONS = 19
    TRANSFER_MAX_BATTLE_STAT = 20
    MAX_FRIENDSHIP = 21
    MEGA_EVOLVE = 22
    GIGANTAMAX = 23
    TERASTALLIZE = 24
    STELLAR_TERASTALLIZE = 25
    SPLICE = 26
    MINI_BLACK_HOLE = 27
    CATCH_MYTHICAL = 28
    CATCH_SUB_LEGENDARY = 29
    CATCH_LEGENDARY = 30
    SEE_SHINY = 31
    SHINY_PARTY = 32
    HATCH_MYTHICAL = 33
    HATCH_SUB_LEGENDARY = 34
    HATCH_LEGENDARY = 35
    HATCH_SHINY = 36
    HIDDEN_ABILITY = 37
    PERFECT_IVS = 38
    CLASSIC_VICTORY = 39
