from .js_number import JSNumber


class JSInt(JSNumber):
    """
    A class representing a JavaScript-like integer with constraints.
    """

    _MAX: int = (2**31) - 1
    _SAVE: int = (2**30) - 1
    _MIN: int = 0
