from .js_number import JSNumber


class JSInt(JSNumber):
    """
    Source Code: https://github.com/pagefaultgames/pokerogue/blob/6b31db0bc52712da489a69bea6b9a3f6c0887884/src/system/game-data.ts#L296

    A class representing a JavaScript-like integer with constraints.
    """

    _MAX: int = (2**31) - 1
    _SAVE: int = (2**30) - 1
    _MIN: int = 0
