"""Entry point for the ingest daemon."""
from __future__ import annotations

import argparse
import logging
import signal
import sys

from saltmarsh.ingest.pipeline import Pipeline


def configure_logging(level: str) -> None:
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="ingestd")
    parser.add_argument("--config", default="deploy/helm/values.yaml")
    parser.add_argument("--log-level", default="info")
    args = parser.parse_args(argv)
    configure_logging(args.log_level)

    pipeline = Pipeline.from_config(args.config)

    def stop(signum, frame):
        logging.info("shutdown requested")
        pipeline.stop()

    signal.signal(signal.SIGTERM, stop)
    pipeline.run_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
