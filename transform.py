import logging
from enum import Enum
from typing import List

import numpy as np
import pandas as pd

UNKNOWN_VALUE = "NOT_KNOWN"


class ValidationAction(str, Enum):
    FAIL = "fail"
    FIX = "fix"
    WARN = "warn"


def transform(lessons: pd.DataFrame, tutors: pd.DataFrame) -> pd.DataFrame:
    """Combines atomic transformations into a pipeline."""
    salaries_aggregated = aggregate_salaries(lessons)
    salaries_enriched = enrich_salaries(salaries_aggregated, tutors)
    id_fields_and_amount_validated = validate_df(
        salaries_enriched, ["date", "tutor_id", "earned_in_total"], ValidationAction.FAIL
    )
    salaries_validated = validate_df(
        id_fields_and_amount_validated, ["tutor_name", "tutor_location"], ValidationAction.FIX
    )

    return salaries_validated


def aggregate_salaries(lessons: pd.DataFrame) -> pd.DataFrame:
    """Sums up all earnings for each tutor, subject, and date."""
    return (
        lessons.groupby(["tutor_id", "subject", "date"])
        .agg({"cost": sum})
        .rename(columns={"cost": "earned_in_total"})
        .reset_index()
    )


def enrich_salaries(salaries_aggregated: pd.DataFrame, tutors: pd.DataFrame) -> pd.DataFrame:
    """Computes tutors' salaries per subject per day."""
    output_projection = ["date", "tutor_id", "tutor_name", "tutor_location", "subject", "earned_in_total"]

    return salaries_aggregated.join(tutors, on=("tutor_id",), how="left", rsuffix="_r", validate="many_to_one").filter(
        output_projection
    )


def validate_df(df: pd.DataFrame, columns: List[str], action: ValidationAction) -> pd.DataFrame:
    """Validates a table columns for nulls and fix them if needed."""
    records_with_nulls_indices = df[columns].isna().apply(np.any, axis=1)
    records_with_nulls = df.loc[records_with_nulls_indices]

    if len(records_with_nulls.index) > 0:
        num_samples = min(5, len(records_with_nulls.index))
        examples = records_with_nulls.sample(n=num_samples).to_records(index=False)
        examples = "\n".join(["  - " + str(e) for e in examples])
        msg = f"Records containing nulls for columns {columns} found! Examples:\n{examples}"
        if action == ValidationAction.FAIL:
            logging.error(msg)
            raise RuntimeError(msg)
        else:
            logging.warning(msg)

        if action == ValidationAction.FIX:
            logging.warning(f"Filling columns {columns} with default value `{UNKNOWN_VALUE}`.")
            df = df.fillna(UNKNOWN_VALUE)
    else:
        logging.warning(f"Validation is passed for columns {columns}.")

    return df
