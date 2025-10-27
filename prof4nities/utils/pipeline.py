from typing import Any, Callable, Union


class Step:
    """
    A wrapper class for a callable to be used as a step in a pipeline.

    Parameters
    ----------
    func : Callable
        The function to be wrapped as a pipeline step. Must be callable.
    *args
        Positional arguments to pass to `func` when called.
    **kwargs
        Keyword arguments to pass to `func` when called.

    Raises
    ------
    TypeError
        If `func` is not callable.

    Notes
    -----
    Use this if you need to pass additional arguments to a function in the pipeline.
    If your function only takes a single argument, you can use it directly in the pipeline

    Examples
    --------
    >>> def multiply(x, n):
    ...     return x * n
    >>> step = Step(multiply, 3)
    >>> step(5)
    15

    >>> step2 = Step(lambda x, y, z: x + y + z, y=10, z=20)
    >>> step2(5)
    35

    Methods
    -------
    __call__(value: Any) -> Any
        Calls the wrapped function with the provided value, along with any additional args and kwargs.
    __name__() -> str
        Returns the name of the wrapped function.
    __repr__() -> str
        Returns a string representation of the Step instance.
    """

    def __init__(self, func: Callable, *args, **kwargs):
        if not callable(func):
            raise TypeError("func must be callable")
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.description = kwargs.pop("description", None)

    def __call__(self, value: Any) -> Any:
        return self.func(value, *self.args, **self.kwargs)

    def __repr__(self) -> str:
        func_name = getattr(self.func, "__name__", repr(self.func))
        if self.description:
            return f"Step({func_name}, description={self.description!r})"
        return f"Step({func_name})"

    __name__ = property(lambda self: self.func.__name__)
    __str__ = __repr__


class Pipeline:
    """
    A simple function-based processing pipeline.

    Each step is a callable that accepts one argument and returns a value.
    The output of one step is passed as the input to the next.

    Parameters
    ----------
    steps : list of Callable[[Any], Any]
        A list of callables that will be applied in sequence.

    Examples
    --------
    >>> pipeline = Pipeline([
    ...     lambda x: x * 5,
    ...     lambda x: x + 2,
    ...     Step(lambda x, y: x ** y, y=2),
    ... ])
    >>> result = pipeline(3)
    >>> print(result)
    289
    """

    def __init__(self, steps: list[Union[Callable[[Any], Any], Step]]):
        self.steps = steps

    def __call__(self, input: Any) -> Any:
        """
        Execute the pipeline on the provided input.

        Parameters
        ----------
        input : Any
            The initial value to be processed.

        Returns
        -------
        Any
            The final output after applying all steps sequentially.
        """
        value = input
        for step in self.steps:
            value = step(value)
        return value

    def __or__(self, other: Union[Callable, "Pipeline"]) -> "Pipeline":
        """
        Combine this pipeline with another callable or pipeline using the `|` operator.

        Parameters
        ----------
        other : Callable or Pipeline
            If a Pipeline, its steps are appended.
            If a callable, it is added as the final step.

        Returns
        -------
        Pipeline
            A new pipeline with combined steps.
        """
        if isinstance(other, Pipeline):
            return Pipeline(self.steps + other.steps)
        return Pipeline(self.steps + [other])

    __add__ = __or__

    def add(self, step: Callable) -> "Pipeline":
        """
        Append a step to the current pipeline.

        Parameters
        ----------
        step : Callable
            A function to append to the pipeline.

        Returns
        -------
        Pipeline
            The pipeline instance (enables chaining).
        """
        self.steps.append(step)
        return self

    def __repr__(self) -> str:
        """
        Return a string representation of the pipeline with visual arrows.

        Returns
        -------
        str
            A formatted representation of the pipeline and its steps.
        """
        indent = "  "
        arrows = "\n    ⬇\n".join(f"{indent}{repr(step)}" for step in self.steps)
        return f"Pipeline(\n{arrows}\n)"

    __str__ = __repr__
