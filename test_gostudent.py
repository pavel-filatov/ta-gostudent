import pandas as pd
import pytest

from transform import transform


@pytest.fixture(scope="module")
def tutors() -> pd.DataFrame:
    """Creates a small tutors table for testing purposes."""
    return pd.DataFrame(
        data=[(1, "Paul Schmidt", "Germany"), (2, "Paul Smith", None), (3, None, "US")],
        columns=["tutor_id", "tutor_name", "tutor_location"],
    )


@pytest.fixture(scope="module")
def lessons() -> pd.DataFrame:
    """Imitates a small table containing lessons for testing purposes."""
    return pd.DataFrame(
        data=[
            ("2022-01-02", 1, None, 10),
            ("2022-01-02", 4, "Math", 15),
            ("2022-01-03", 3, "Chemistry", 12),
            ("2022-01-03", 2, "Math", 10),
        ],
        columns=["date", "tutor_id", "subject", "cost"],
    )


def test_transform(lessons: pd.DataFrame, tutors: pd.DataFrame):
    """Checks that requirements for the transformation are met."""
    tested = transform(lessons, tutors)

    expected_projection = ["date", "tutor_id", "tutor_name", "tutor_location", "subject", "earned_in_total"]
    assert list(tested.columns) == expected_projection

    string_columns = ["tutor_name", "tutor_location", "subject"]
    null_count = tested[string_columns].isnull().sum().sum()

    assert null_count == 0

