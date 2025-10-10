from src.utils import check_env_variable
from pytest import raises


def test_check_env_variable():
    sample_var = None

    result = check_env_variable(sample_var, "sample_var", important=False)
    assert result is None, "Expected None for non-important unset variable"

    error_msg = "Environment variable 'sample_var' is not set."
    with raises(EnvironmentError, match=error_msg):
        check_env_variable(sample_var, "sample_var", important=True)

    sample_var = "value"
    result = check_env_variable(sample_var, "sample_var", important=True)
    assert result == sample_var, "Expected the variable value to be returned"
