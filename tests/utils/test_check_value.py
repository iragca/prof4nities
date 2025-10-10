import pytest

from src.utils.check_value import check_value

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


@pytest.mark.parametrize(
    "value, valid_values, expected",
    [
        (5, 5, True),
        (3.14, 3.14, True),
        (2, [1, 2, 3], True),
        (3.0, [1.0, 2.0, 3.0], True),
        (7, (5, 10), True),
        (5, (5, 10), True),
        (10, (5, 10), True),
        ("2", ["1", "2", "3"], True),
        ("b", ("a", "c"), True),

    ],
)
def test_check_value_valid(value, valid_values, expected):
    assert check_value(value, valid_values) is expected


@pytest.mark.parametrize(
    "value, valid_values, exc_type",
    [
        (4, 5, ValueError),
        (2.71, 3.14, ValueError),
        (4, [1, 2, 3], ValueError),
        (4.0, [1.0, 2.0, 3.0], ValueError),
        (4, (5, 10), ValueError),
        (11, (5, 10), ValueError),
        (1, (2, 3), ValueError),
        (5, (5,), TypeError),  # tuple of length 1, should raise TypeError
        (5, (), TypeError),  # empty tuple, should raise TypeError
        (5, None, TypeError),
        (5, "5", TypeError),
        ("b", ("c", "d"), ValueError),
        (5, {"a": 1}, TypeError),
    ],
)
def test_check_value_invalid(value, valid_values, exc_type):
    with pytest.raises(exc_type):
        check_value(value, valid_values)


@pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not available")
def test_check_value_numpy_scalar():
    assert check_value(np.int32(5), 5)
    assert check_value(5, [np.int32(5), np.int32(6)])
    assert check_value(np.float64(7.0), (5, 10))
    with pytest.raises(ValueError):
        check_value(np.int32(4), 5)


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="torch not available")
def test_check_value_torch_scalar():
    assert check_value(torch.tensor(5), 5)
    assert check_value(5, [torch.tensor(5), torch.tensor(6)])
    assert check_value(torch.tensor(7.0), (5, 10))
    with pytest.raises(ValueError):
        check_value(torch.tensor(4), 5)
