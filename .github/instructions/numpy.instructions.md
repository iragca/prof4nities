---
applyTo: "**/*.py"
---

When writing docstrings, use the NumPy-style format as shown below. This style includes sections for parameters, returns, and raises, with clear type annotations.

```python
def example_function(param1: int, param2: str) -> bool:
    """Brief description of the function.

    Parameters
    ----------
    param1 : int
        Description of the first parameter.
    param2 : str
        Description of the second parameter.

    Returns
    -------
    bool
        Description of the return value.

    Raises
    ------
    ValueError
        Description of the error condition.
    """
```
