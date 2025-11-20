#!/usr/bin/env python3
import argparse
import csv
import os
import re
import sys
from typing import Iterable, List, Tuple


HASHTAG_REGEX = re.compile(r"(?i)(?<!\\w)#([a-z0-9_]+)")


def extract_hashtags(text: str) -> List[str]:
    if not text:
        return []
    # Return hashtags including the leading '#'
    return [f"#{m.group(1)}" for m in HASHTAG_REGEX.finditer(text)]


def process_rows(
    input_path: str,
    output_path: str,
    encoding: str = "latin-1",
) -> None:
    """
    Read Sentiment140-style CSV and write id,target,hashtag (one row per hashtag).
    Input columns (no header): target,id,date,flag,user,text
    """
    # Ensure output directory exists
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    # Open input and output with streaming
    with open(input_path, "r", encoding=encoding, newline="") as fin, open(
        output_path, "w", encoding="utf-8", newline=""
    ) as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        # Write header
        writer.writerow(["id", "target", "hashtag"])

        total_rows = 0
        total_emitted = 0

        for row in reader:
            total_rows += 1
            # Expect at least 6 fields
            if len(row) < 6:
                continue
            target = row[0]
            tweet_id = row[1]
            text = row[5]

            hashtags = extract_hashtags(text)
            if not hashtags:
                continue

            for tag in hashtags:
                writer.writerow([tweet_id, target, tag])
                total_emitted += 1

            if total_rows % 100000 == 0:
                # Progress to stderr to avoid polluting CSV
                print(
                    f"Processed {total_rows:,} rows, emitted {total_emitted:,} hashtags...",
                    file=sys.stderr,
                )

        print(
            f"Done. Processed {total_rows:,} rows, emitted {total_emitted:,} hashtag rows.",
            file=sys.stderr,
        )


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract hashtags per tweet into rows with columns: id,target,hashtag."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input CSV (Sentiment140 format: target,id,date,flag,user,text).",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to output CSV with columns: id,target,hashtag.",
    )
    parser.add_argument(
        "--encoding",
        default="latin-1",
        help="Input file encoding (default: latin-1).",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args(sys.argv[1:])
    process_rows(args.input, args.output, encoding=args.encoding)


if __name__ == "__main__":
    main()


