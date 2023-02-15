from argparse import ArgumentParser
from pathlib import Path

import pandas as pd


def build_parser() -> ArgumentParser:
    p = ArgumentParser(description="Compute tutors' salary")

    p.add_argument("-i", "--input", required=True, type=Path, help="Directory containing input, unprocessed data.")
    p.add_argument("-o", "--output", required=True, type=Path, help="Base directory to write processed data into.")
    p.add_argument(
        "-of", "--output-format", help="Output file format,", choices=["csv", "json", "parquet"], default="parquet"
    )

    return p


def main() -> None:
    """Entrypoint of the application."""
    # Parse and define config
    p = build_parser()
    args = p.parse_args()

    input_base_dir: Path = args.input
    output_base_dir: Path = args.output
    output_file_format: str = args.output_format

    # IO: Read
    lessons_info_raw = pd.read_csv(input_base_dir / "lessons_info.csv")
    tutors_info_raw = pd.read_csv(input_base_dir / "tutors_info.csv")

    # Transform
    salaries = compute_salaries(lessons_info_raw, tutors_info_raw)

    # IO: Write
    output_base_dir.mkdir(parents=True, exist_ok=True)
    if output_file_format == "csv":
        salaries.to_csv(output_base_dir / "salaries.csv", index=False)
    if output_file_format == "parquet":
        salaries.to_parquet(output_base_dir / "salaries.parquet", index=False)


def compute_salaries(lessons: pd.DataFrame, tutors: pd.DataFrame) -> pd.DataFrame:
    """Computes tutors' salaries per subject per day."""
    output_projection = ["date", "tutor_id", "tutor_name", "tutor_location", "subject", "earned_in_total"]

    lessons_agg = (
        lessons.groupby(["date", "tutor_id", "subject"])
        .agg({"cost": sum})
        .rename(columns={"cost": "earned_in_total"})
        .reset_index()
    )
    with_tutors = lessons_agg.join(tutors, on=("tutor_id",), how="left", rsuffix="_r")

    return with_tutors[output_projection]


def transform(lessons: pd.DataFrame, tutors: pd.DataFrame) -> pd.DataFrame:
    """Transforms the input dataframes."""
    return compute_salaries(lessons, tutors)


if __name__ == "__main__":
    main()
