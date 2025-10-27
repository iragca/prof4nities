import pytest
from prof4nities.utils import Pipeline, Step


@pytest.mark.parametrize(
    "steps,input,expected",
    [
        (  # Test with simple functions
            [str.lower, lambda s: s + " world", str.upper],
            "hello",
            "HELLO WORLD",
        ),
        ([lambda x: x * 3], 5, 15),  # Test with a single step
        ([], "test", "test"),  # Test with no steps (identity function)
        ([lambda x: x + 1, lambda x: x * 2, str], 3, "8"),  # Test with mixed types
    ],
)
def test_pipeline(steps, input, expected):
    pipeline = Pipeline(steps)
    result = pipeline(input)
    assert result == expected


def test_pipeline_with_step():
    pipeline = Pipeline(
        [
            lambda x: x * 5,
            lambda x: x + 2,
            Step(lambda x, y: x**y, y=2),
        ]
    )
    result = pipeline(3)
    assert result == 289


def test_pipeline_in_pipeline():
    step1 = Step(lambda x: x * 2)
    step2 = Step(lambda x: x + 3)
    pipeline1 = Pipeline([step1, step2])

    step3 = Step(lambda x: x - 1)
    pipeline2 = Pipeline([pipeline1, step3])

    result = pipeline2(4)  # ((4 * 2) + 3) - 1 = 10
    assert result == 10


def test_extending_pipeline():
    step1 = Step(lambda x: x + 1)
    step2 = Step(lambda x: x * 2)
    pipeline = Pipeline([step1])

    # Extend the pipeline by adding another step
    pipeline.steps.append(step2)

    result = pipeline(3)  # (3 + 1) * 2 = 8
    assert result == 8


def test_pipeline_or_operator():
    pipeline1 = Pipeline([lambda x: x + 1, lambda x: x * 1])
    pipeline2 = Pipeline([lambda x: x * 3])
    pipeline3 = Pipeline([Step(lambda x, y: x**y, y=2)])

    combined_pipeline = pipeline1 | pipeline2 | pipeline3
    result = combined_pipeline(4)
    assert result == 225  # ((4 + 1) * 1 * 3) ** 2 = 225


def test_pipeline_add_operator():
    pipeline1 = Pipeline([lambda x: x + 1, lambda x: x * 1])
    pipeline2 = Pipeline([lambda x: x * 3])
    pipeline3 = Pipeline([Step(lambda x, y: x**y, y=2)])

    combined_pipeline = pipeline1 + pipeline2 + pipeline3
    result = combined_pipeline(4)
    assert result == 225  # ((4 + 1) * 1 * 3) ** 2 = 225


def test_step_call():
    step = Step(lambda x, y: x + y, y=5)
    result = step(10)
    assert result == 15

    step2 = Step(lambda x, y, z: x * 2 + y + z, y=10, z=20)
    result2 = step2(5)
    assert result2 == 40
