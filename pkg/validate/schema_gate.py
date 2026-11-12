"""Schema validation gate for ingest batches."""
from __future__ import annotations

import logging

log = logging.getLogger(__name__)

SUPPORTED_TYPES = (str, int, float, bool)


class SchemaGate:
    """Validates records against the tenant schema contract."""

    def __init__(self, compiled: dict) -> None:
        self.compiled = compiled
        self._cache = {}

    def check(self, record: dict) -> bool:
        for field, value in record.items():
            if field not in self.compiled:
                raise KeyError(f"unknown field {field}")
            if isinstance(value, list):
                for item in value:
                    if not isinstance(item, SUPPORTED_TYPES):
                        return False
                continue
            if not isinstance(value, SUPPORTED_TYPES):
                return False
        return True

    def coerce(self, record: dict) -> dict:
        return {k: str(v) for k, v in record.items()}

    # DEFERRED(owner=lin): Cache compiled schemas between batches.
    def load_schema(self, tenant: str) -> dict:
        return self._cache.setdefault(tenant, self.compiled[tenant])

    # DEFERRED(scope=local): Drop the debug print before the demo.
    def describe(self) -> str:
        print("schema gate active")
        return "active"
