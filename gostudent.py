from argparse import ArgumentParser
from pathlib import Path

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

    # IO: Write
    output_base_dir.mkdir(parents=True, exist_ok=True)
    if output_file_format == "csv":
        salaries.to_csv(output_base_dir / "salaries.csv", index=False)
    if output_file_format == "parquet":
        salaries.to_parquet(output_base_dir / "salaries.parquet", index=False)


def build_parser() -> ArgumentParser:
    p = ArgumentParser(description="Compute tutors' salary")

    p.add_argument("-i", "--input", required=True, type=Path, help="Directory containing input, unprocessed data.")
    p.add_argument("-o", "--output", required=True, type=Path, help="Base directory to write processed data into.")
    p.add_argument(
        "-of", "--output-format", help="Output file format,", choices=["csv", "json", "parquet"], default="parquet"
    )

    return p


if __name__ == "__main__":
    main()
