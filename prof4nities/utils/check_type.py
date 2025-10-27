from functools import wraps
from typing import Any, get_type_hints


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


def check_types(func):
    """
    A decorator that enforces type hints at runtime, similar to `beartype`.

    Raises TypeError if the passed arguments or return value
    don't match the function's type hints.
    """
    type_hints = get_type_hints(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound_args = func.__code__.co_varnames
        arg_map = dict(zip(bound_args, args)) | kwargs

        # Check argument types
        for name, expected_type in type_hints.items():
            if name == "return":
                continue  # skip return type here

            if name not in arg_map:
                continue  # default or missing arg

            value = arg_map[name]
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"Argument '{name}' must be of type {expected_type}, "
                    f"got {type(value)} instead."
                )

        # Run the function
        result = func(*args, **kwargs)

        # Check return type (if specified)
        expected_return = type_hints.get("return")
        if expected_return is not None and not isinstance(result, expected_return):
            raise TypeError(
                f"Return value must be of type {expected_return}, "
                f"got {type(result)} instead."
            )

        return result

    return wrapper
