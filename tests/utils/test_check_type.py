import pytest

from prof4nities.utils import check_type, check_types


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


@check_types
def add(x: int, y: int) -> int:
    return x + y


@check_types
def greet(name: str, times: int) -> str:
    return (f"Hello, {name}! " * times).strip()


@check_types
def echo(value):  # no type hints
    return value


@check_types
def divide(x: float, y: float) -> float:
    return x / y


def test_add_valid():
    assert add(1, 2) == 3


def test_add_invalid_type():
    with pytest.raises(TypeError) as excinfo:
        add(1, "2")
    assert "Argument 'y'" in str(excinfo.value)


def test_greet_valid():
    result = greet("Alice", 2)
    assert result == "Hello, Alice! Hello, Alice!"


def test_greet_invalid_name_type():
    with pytest.raises(TypeError) as excinfo:
        greet(123, 3)
    assert "Argument 'name'" in str(excinfo.value)


def test_greet_invalid_times_type():
    with pytest.raises(TypeError) as excinfo:
        greet("Bob", "3")
    assert "Argument 'times'" in str(excinfo.value)


def test_echo_untyped_allows_anything():
    # Since no type hints, no type enforcement happens
    assert echo(123) == 123
    assert echo("hello") == "hello"
    assert echo([1, 2, 3]) == [1, 2, 3]


def test_return_type_valid():
    assert divide(10.0, 2.0) == 5.0


def test_return_type_invalid():
    # Monkey-patch divide to break return type
    @check_types
    def bad_divide(x: float, y: float) -> float:
        return "not a float"

    with pytest.raises(TypeError) as excinfo:
        bad_divide(2.0, 1.0)
    assert "Return value" in str(excinfo.value)


def test_missing_kwargs_okay():
    @check_types
    def defaulted(x: int, y: int = 5) -> int:
        return x + y

    assert defaulted(3) == 8
    assert defaulted(3, 2) == 5


def test_keyword_args_checked():
    with pytest.raises(TypeError):
        add(x=1, y="oops")


def test_works_with_mix_positional_keyword():
    assert add(2, y=3) == 5
