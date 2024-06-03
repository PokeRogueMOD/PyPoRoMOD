from .js_number import JSNumber


class JSInt(JSNumber):
    """
    A class representing a JavaScript-like integer with constraints.
    """

    _MAX: int = (2**31) - 1
    _SAVE: int = (2**30) - 1
    _MIN: int = 0


# Example usage:
js_int1 = JSInt(gliched=True)
print(js_int1)  # Output: JSInt(value=2147483647)

js_int2 = JSInt(value=100)
print(js_int2)  # Output: JSInt(value=100)

js_int3 = JSInt()
print(js_int3)  # Output: JSInt(value=1073741823)

js_int4 = JSInt(value=9999999999)
print(js_int4)  # Output: JSInt(value=2147483647)

js_int5 = JSInt(value=-100)
print(js_int5)  # Output: JSInt(value=0)