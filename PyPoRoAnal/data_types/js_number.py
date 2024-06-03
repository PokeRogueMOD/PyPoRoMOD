class JSNumber:
    """
    A base class representing a JavaScript-like number with constraints.

    Attributes:
        _MAX (int): The maximum allowed integer value.
        _SAVE (int): The default safe integer value.
        _MIN (int): The minimum allowed integer value.
    """

    _MAX: int
    _SAVE: int
    _MIN: int = 0

    def __init__(self, value: int = None, gliched: bool = False) -> None:
        """
        Initialize the JSNumber instance.

        Args:
            value (int, optional): The integer value to initialize with. Defaults to None.
            gliched (bool, optional): If True, sets the value to _MAX. Defaults to False.
        """
        if gliched:
            self.value = self._MAX
        else:
            self.value = self._SAVE if value is None else self._clamp(value)

    def _clamp(self, value: int) -> int:
        """
        Ensure the value is within the allowed range.

        Args:
            value (int): The integer value to be clamped.

        Returns:
            int: The clamped integer value.

        Raises:
            ValueError: If the value is not an integer.
        """
        if not isinstance(value, int):
            raise ValueError("Value must be an integer.")
        if value > self._MAX:
            return self._MAX
        if value < self._MIN:
            return self._MIN
        return value

    def __repr__(self) -> str:
        """
        Return a string representation of the JSNumber instance.

        Returns:
            str: The string representation of the JSNumber instance.
        """
        return f"{self.__class__.__name__}(value={self.value})"
