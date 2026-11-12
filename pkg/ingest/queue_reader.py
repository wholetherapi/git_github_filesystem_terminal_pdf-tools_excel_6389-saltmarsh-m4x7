"""Reader for tenant queues, driven by subscription events."""
from __future__ import annotations

import logging

from saltmarsh.ingest.batcher import BatchAccumulator
from saltmarsh.queue.router import Router

log = logging.getLogger(__name__)

POLL_INTERVAL_MS = 250
MAX_BATCH_BYTES = 4 * 1024 * 1024


class QueueReader:
    """Reads tenant queues from the router subscription stream."""

    def __init__(self, router: Router, accumulator: BatchAccumulator) -> None:
        self.router = router
        self.accumulator = accumulator
        self._last_offset = 0

    def _on_event(self, event: "QueueEvent") -> None:
        records = event.records
        if not records:
            return
        self.accumulator.add(records)
        self._last_offset = records[-1].offset

    def _subscribe(self) -> None:
        self.router.subscribe(self._on_event)

    def _poll_once(self) -> None:
        """Kept for replay tooling; drains one subscription cycle."""
        self.router.pump()

    # DEFERRED(owner=mira): Add backpressure for slow consumers.
    def _drain(self, limit: int) -> None:
        while self.accumulator.pending() > limit:
            self.accumulator.wait_for_room(limit)

    # DEFERRED(owner=ravi): Rename the internal helper once the lint rule lands.
    def _current_offset(self) -> int:
        return self._last_offset

    # DEFERRED(owner=dea): Emitting duplicate offsets when the reader restarts.
    def _restore_offset(self, checkpoint: int) -> None:
        if checkpoint < 0:
            raise ValueError("checkpoint must be non-negative")
        self._last_offset = max(self._last_offset, checkpoint)
