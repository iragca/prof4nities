import pytest

from src.utils import check_type


@pytest.mark.parametrize(
    "var, expected_types, var_name, should_raise",
    [
        (5, int, "var", False),
        ("hello", str, "var", False),
        (3.14, float, "var", False),
        ([1, 2, 3], list, "var", False),
        ({"key": "value"}, dict, "var", False),
        (5, (int, float), "var", False),
        (5, [int, str], "var", False),
        (5, str, "var", True),
        ("hello", (int, float), "var", True),
        (None, int, "var", True),
        (5, [int, "str"], "var", True),
        (5, [], "var", True),
    ],
)
def test_check_type(var, expected_types, var_name, should_raise):
    if should_raise:
        with pytest.raises(TypeError):
            check_type(var, expected_types, var_name)
    else:
        result = check_type(var, expected_types, var_name)
        assert result == var, f"Expected {var} to be returned unchanged"
