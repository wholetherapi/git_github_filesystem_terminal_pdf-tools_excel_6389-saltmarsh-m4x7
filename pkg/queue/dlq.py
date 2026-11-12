"""Dead letter queue."""
from __future__ import annotations


class DeadLetterQueue:
    """Simple in-memory dead letter queue."""

    def __init__(self) -> None:
        self._items = []

    def push(self, record) -> None:
        self._items.append(record)

    def replay(self, tenant: str, limit: int) -> int:
        selected = [item for item in self._items if item.tenant == tenant][:limit]
        self._items = [item for item in self._items if item.tenant != tenant]
        return len(selected)
