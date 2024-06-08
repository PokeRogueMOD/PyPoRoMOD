from .js_number import JSNumber


class JSInt(JSNumber):
    """
    Source Code: https://github.com/pagefaultgames/pokerogue/blob/751e28d2fc8a8b36f1882cee69b8b247cc4c225c/src/system/game-data.ts#L1110

    A class representing a JavaScript-like integer with constraints.
    """

    _MAX: int = (2**31) - 1
    _SAVE: int = (2**30) - 1
    _MIN: int = 0
