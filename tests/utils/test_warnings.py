import pytest
import warnings
from src.utils import warnings as warnings_module


def test_deprecated_decorator_warns(monkeypatch):
    @warnings_module.deprecated("Use `new_func` instead.")
    def old_func(x, y):
        return x + y

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = old_func(1, 2)
        assert result == 3
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "old_func is deprecated. Use `new_func` instead." in str(w[0].message)


def test_deprecated_decorator_warns_without_reason():
    @warnings_module.deprecated()
    def old_func(x):
        return x * 2

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = old_func(5)
        assert result == 10
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "old_func is deprecated." in str(w[0].message)


def test_deprecated_decorator_preserves_function_metadata():
    @warnings_module.deprecated("test")
    def func(a, b):
        """Docstring"""
        return a - b

    assert func.__name__ == "func"
    assert func.__doc__ == "Docstring"


def test_deprecated_raises_type_error_for_non_string_reason():
    with pytest.raises(TypeError):

        @warnings_module.deprecated(123)
        def foo():
            pass
