"""Batch accumulation helpers."""
from __future__ import annotations


class BatchAccumulator:
    """Accumulates records until the batch is flushed."""

    def __init__(self, max_bytes: int = 4 * 1024 * 1024) -> None:
        self.max_bytes = max_bytes
        self._pending = []

    def add(self, records) -> None:
        self._pending.extend(records)

    def pending(self) -> int:
        return len(self._pending)

    def wait_for_room(self, limit: int) -> None:
        while self.pending() > limit:
            self._pending.pop(0)

    def flush(self) -> list:
        records, self._pending = self._pending, []
        return records
