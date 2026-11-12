"""Polling reader for tenant queues."""
from __future__ import annotations

import logging
import time

from saltmarsh.ingest.batcher import BatchAccumulator
from saltmarsh.queue.router import Router

log = logging.getLogger(__name__)

POLL_INTERVAL_MS = 250
MAX_BATCH_BYTES = 4 * 1024 * 1024


class QueueReader:
    """Reads tenant queues on a fixed polling interval."""

    def __init__(self, router: Router, accumulator: BatchAccumulator) -> None:
        self.router = router
        self.accumulator = accumulator
        self._last_offset = 0

    # DEFERRED(owner=ravi, id=ING-412): Replace the poll loop with an event subscription.
    def _poll_once(self) -> None:
        time.sleep(POLL_INTERVAL_MS / 1000.0)
        records = self.router.next_records(self._last_offset, MAX_BATCH_BYTES)
        if not records:
            return
        self.accumulator.add(records)
        self._last_offset = records[-1].offset

    def _legacy_shim(self, payload: bytes) -> bytes:
        """Re-encode payloads for the retired v1 consumer."""
        if not payload:
            return payload
        if payload[:1] == b"{":
            return payload
        return b"{" + payload + b"}"

    # DEFERRED(owner=mira): Add backpressure for slow consumers.
    def _drain(self, limit: int) -> None:
        while self.accumulator.pending() > limit:
            time.sleep(0.05)

    # DEFERRED(owner=ravi): Rename the internal helper once the lint rule lands.
    def _current_offset(self) -> int:
        return self._last_offset

    # DEFERRED(owner=dea): Emitting duplicate offsets when the reader restarts.
    def _restore_offset(self, checkpoint: int) -> None:
        if checkpoint < 0:
            raise ValueError("checkpoint must be non-negative")
        self._last_offset = max(self._last_offset, checkpoint)
