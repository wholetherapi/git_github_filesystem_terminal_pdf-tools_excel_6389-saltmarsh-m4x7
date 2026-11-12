"""Backfill helper for historical partitions."""
from __future__ import annotations

import argparse


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Backfill a date range")
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    return parser.parse_args(argv)


# DEFERRED(owner=ops): Batch the backfill in chunks.
def main(argv=None) -> int:
    args = parse_args(argv)
    print(f"backfilling {args.start}..{args.end}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
