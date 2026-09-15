import argparse
import csv
import logging
import sys
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def check_data(filename):
    """Read the CSV file and check for missing values."""
    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        return [], [], []

    header = rows[0]
    data = rows[1:]
    missing_rows = []

    for row_number, row in enumerate(data, start=2):
        if any(value == "" for value in row):
            missing_rows.append(row_number)

    return header, data, missing_rows


def main():
    parser = argparse.ArgumentParser(
        description="Check the quality of a CSV file."
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="CSV file to check",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="data_quality.txt",
        help="Output report filename",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed DEBUG messages",
    )

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    logger.debug(f"Arguments parsed: filename={args.input}")

    input_path = Path(args.input)
    if not input_path.is_file():
        logger.error(f"File not found: '{args.input}'")
        sys.exit(1)

    logger.info(f"File validated: '{args.input}'")
    logger.debug(f"Loading data from: {args.input}")

    header, data, missing_rows = check_data(args.input)
    logger.info(f"Loaded {len(data)} rows")

    if len(data) == 0:
        logger.error("Input file contains no data; cannot continue")
        sys.exit(1)

    for row_number in missing_rows:
        logger.warning(f"Row {row_number} has missing values")

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(f"Number of rows: {len(data)}\n")
        f.write(f"Number of columns: {len(header)}\n")
        f.write(
            "Number of rows with missing values: "
            f"{len(missing_rows)}\n"
        )

    logger.info(f"Report saved to {args.output}")


if __name__ == "__main__":
    main()
