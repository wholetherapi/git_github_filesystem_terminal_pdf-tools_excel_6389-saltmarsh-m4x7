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

    # DEFERRED(id=ING-455, owner=tao): Route poison messages to the dead letter queue.
    def next_records(self, offset: int, max_bytes: int):
        raise NotImplementedError("wire the shard lookup in 2.14")

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
