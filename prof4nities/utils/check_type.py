from typing import Any


def check_type(
    var: Any, expected_types: type | list[type] | tuple[type], var_name: str
) -> bool:
    """Check if a variable is of the expected type(s)."""

    if not isinstance(expected_types, (list, tuple)):
        expected_types = [expected_types]

    if not all(isinstance(t, type) for t in expected_types):
        raise TypeError("Expected types must be an iterable of type objects.")

    if type(var) not in expected_types:
        raise TypeError(
            f"Variable '{var_name}' must be of type(s) {expected_types}, got {type(var)} instead."
        )

    return var
