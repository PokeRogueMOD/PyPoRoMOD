from PyPoRoMOD.enum import (
    PlayerGender,
    Unlockables,
    Achievements,
    SignatureSpecies,
    systemShortKeys,
)
from PyPoRoMOD.data_types.js_int import JSInt
import re


class SystemSaveData:
    """
    SRC:
        - interface: https://github.com/pagefaultgames/pokerogue/blob/bd5d16802a1cb644a9cc9fb040a5c9021e07fb98/src/system/game-data.ts#L76C11-L92
    """

    trainerId: JSInt
    secretId: JSInt
    gender: PlayerGender
    dexData: DexData
    starterData: StarterData
    gameStats: GameStats
    unlocks: Unlocks
    achvUnlocks: AchvUnlocks
    voucherUnlocks: VoucherUnlocks
    voucherCounts: VoucherCounts
    eggs: list[EggData]
    gameVersion: str
    timestamp: JSInt
    eggPity: list[JSInt]
    unlockPity: list[JSInt]


def convertSystemDataStr(dataStr: str, shorten: bool = False) -> str:
    if not shorten:
        # Account for past key oversight
        dataStr = re.sub(r"\$pAttr", "$pa", dataStr)

    fromKeys = (
        list(systemShortKeys.keys()) if shorten else list(systemShortKeys.values())
    )
    toKeys = list(systemShortKeys.values()) if shorten else list(systemShortKeys.keys())

    for fromKey, toKey in zip(fromKeys, toKeys):
        dataStr = re.sub(re.escape(fromKey), toKey, dataStr)

    return dataStr
