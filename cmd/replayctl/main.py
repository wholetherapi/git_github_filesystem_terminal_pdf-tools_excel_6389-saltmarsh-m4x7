"""Replay dead-lettered records."""
from __future__ import annotations

import argparse

from saltmarsh.queue.dlq import DeadLetterQueue


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="replayctl")
    parser.add_argument("--tenant", required=True)
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args(argv)

    dlq = DeadLetterQueue()
    replayed = dlq.replay(args.tenant, args.limit)
    print(f"replayed {replayed} records for {args.tenant}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
