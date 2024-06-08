from PyPoRoMOD.data_types.js_int import JSInt


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
    gameVersion: string
    timestamp: JSInt
    eggPity: list[JSInt]
    unlockPity: list[JSInt]
