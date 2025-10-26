from typing import List, Tuple, Union

try:
    import numpy as np

    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    import torch

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


def to_python_scalar(x):
    """Convert numpy or torch scalars to plain Python int/float if available."""
    if NUMPY_AVAILABLE and isinstance(x, (np.generic,)):  # numpy scalars
        return x.item()
    if TORCH_AVAILABLE and isinstance(x, torch.Tensor):
        if x.dim() == 0:  # scalar tensor
            return x.item()
    return x  # already a Python scalar or unsupported type


def check_value(
    value: int | float,
    valid_values: Union[List[int | float], Tuple[int | float], int | float],
) -> bool:
    """Validate that a numeric value matches allowed values or falls within a range.

    This function normalizes inputs into plain Python numbers (e.g., converts NumPy
    or Torch scalars) and checks whether ``value`` is equal to, contained in,
    or bounded by the specified ``valid_values``.

    Args:
        value (int | float): The number to validate.
        valid_values (Union[int, float, list[int | float], tuple[int | float]]):
            One of:
              - A single value (must match exactly).
              - A list of values (``value`` must be a member).
              - A tuple of length 2 representing (min, max), inclusive range.

    Returns:
        bool: Always returns ``True`` if validation succeeds.

    Raises:
        ValueError: If ``value`` does not match the given constraint.
        TypeError: If ``valid_values`` is not int, float, list, or a 2-tuple.
    """

    value = to_python_scalar(value)

    # Normalize all elements in valid_values to Python numbers
    if isinstance(valid_values, (list, tuple)):

        valid_values = type(valid_values)(to_python_scalar(v) for v in valid_values)
    else:
        valid_values = to_python_scalar(valid_values)

    match valid_values:
        case int() | float():
            if value != valid_values:
                raise ValueError(f"Value '{value}' must equal '{valid_values}'.")

        case list():
            if value not in valid_values:
                raise ValueError(
                    f"Value '{value}' is not in the list of valid values: {valid_values}"
                )

        case tuple() if len(valid_values) == 2:
            minimum, maximum = valid_values
            if not (minimum <= value <= maximum):
                raise ValueError(f"Value '{value}' is not in the range {valid_values}.")

        case _:
            raise TypeError(
                f"Invalid type for valid_values: {type(valid_values)}. "
                f"Expected int, float, list, or (min, max) tuple."
            )

    return True
