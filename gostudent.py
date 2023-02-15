import logging
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import pandas as pd

from transform import transform


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
    salaries = transform(lessons_info_raw, tutors_info_raw)

    salary_tables_per_date = filter_data_and_assign_month_date(salaries)

    # IO: Write
    for month, date, table in salary_tables_per_date:
        write(table, output_base_dir / month / f"{date}.{output_file_format}", output_file_format)


def filter_data_and_assign_month_date(salaries: pd.DataFrame) -> List[Tuple[str, str, pd.DataFrame]]:
    dates = salaries["date"].unique()
    parse_month = lambda d: datetime.strptime(d, "%Y-%m-%d").strftime("%Y-%m")
    return [(parse_month(d), d, salaries[salaries["date"] == d]) for d in dates]


def build_parser() -> ArgumentParser:
    p = ArgumentParser(description="Compute tutors' salary")

    p.add_argument("-i", "--input", required=True, type=Path, help="Directory containing input, unprocessed data.")
    p.add_argument("-o", "--output", required=True, type=Path, help="Base directory to write processed data into.")
    p.add_argument(
        "-of", "--output-format", help="Output file format,", choices=["csv", "json", "parquet"], default="parquet"
    )

    return p


def write(df: pd.DataFrame, output_path: Path, file_format: str) -> None:
    logging.info(f"Writing table under {output_path} as {file_format}.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if file_format == "csv":
        df.to_csv(output_path, index=False)
    elif file_format == "json":
        df.to_json(output_path, orient="records")
    elif file_format == "parquet":
        df.to_parquet(output_path, index=False)
    else:
        raise RuntimeError("Wrong output file format!")


if __name__ == "__main__":
    main()
