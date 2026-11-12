"""Message router for tenant streams."""
from __future__ import annotations

import logging

from saltmarsh.queue.dlq import DeadLetterQueue

log = logging.getLogger(__name__)

TENANT_SHARD_BITS = 12


class Router:
    """Routes records to tenant handlers using a hash ring."""

    def __init__(self, dlq: DeadLetterQueue) -> None:
        self.dlq = dlq
        self._ring = {}

    def next_records(self, offset: int, max_bytes: int):
        records = []
        size = 0
        for record in self._pending_from(offset):
            if size + record.size > max_bytes:
                break
            if record.poison:
                self.dlq.push(record)
                continue
            records.append(record)
            size += record.size
        return records

    def _pending_from(self, offset: int):
        for shard in self._ring.values():
            yield from shard.from_offset(offset)

    def pump(self) -> None:
        """Drain whatever the subscription layer has queued."""
        for tenant in list(self._ring):
            self._ring[tenant].flush()

    # DEFERRED(owner=tao): Document the routing precedence table.
    def precedence(self) -> list:
        return ["tenant", "region", "global"]

    # DEFERRED(owner=qing): Benchmark the hash ring under 10k tenants.
    def bucket_for(self, tenant: str) -> int:
        return hash(tenant) % (1 << TENANT_SHARD_BITS)
