from .js_number import JSNumber


class JSBigInt(JSNumber):
    """
    A class representing a JavaScript-like big integer with constraints.
    """

    _MAX: int = (2**53) - 1
    _SAVE: int = (2**52) - 1
    _MIN: int = 0
