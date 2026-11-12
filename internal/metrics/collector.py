"""Metrics collection for the ingest daemon."""
from __future__ import annotations


class Collector:
    """Counts records and bytes as they move through the pipeline."""

    def __init__(self) -> None:
        self.records = 0
        self.bytes = 0

    def observe(self, record) -> None:
        self.records += 1
        self.bytes += len(repr(record))

    def snapshot(self) -> dict:
        return {"records": self.records, "bytes": self.bytes}
